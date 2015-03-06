# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2015 Dominic Antonacci dominic.antonacci@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import Libraries
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
import os.path
import unicodedata

def open_title_author_csv(file_name):
# Opens the title/author csv file for editing by the program. If necessary,
# it will be created with the proper headers. The CSV file is designed to
# interface with the CSV file standards for Readerware 3.0 importing.
#
# Usage
# file = open_title_author_csv(file_name)
#
# Inputs
# file_name: a string containing the file name
#
# Outputs
# file: the file object returned by open(file_name)


    # Create the csv file if it doesn't already exist
    if(not os.path.isfile(file_name)):
        csv_file = open(file_name,'w') #open file
        csv_file.write('"Title","Author","Call_Number"\n')
    else:
        csv_file = open(file_name,'a') # Set line buffering
        
    return csv_file
        
        
def open_isbn_csv(file_name):
# Opens the ISBN csv file for editing by the program. If necessary,
# it will be created with the proper headers. The CSV file is designed to
# interface with the CSV file standards for Readerware 3.0 importing.
#
# Usage
# file = open_title_author_csv(file_name)
#
# Inputs
# file_name: a string containing the file name
#
# Outputs
# file: the file object returned by open(file_name)   
     
    # Create the csv file if it doesn't already exist
    if(not os.path.isfile(file_name)):
        csv_file = open(file_name,'w', 1) #open file, and set to line buffering
        csv_file.write('"ISBN","Call_Number"\n')
    else:
        csv_file = open(file_name,'a', 1) # Set line buffering
        
    return csv_file

    

def get_url_segment(name):
# Returns a URL segment to use when searching the classify.oclc.org website
# This creates a simple access point to modify the URLs if necessary
# in the future
#
# Usage
# url_segment = get_url_segment(name)
#
# Inputs
# name: the name of the URL segment you want
#
# Outputs
# url_segment: the segment corresponding to the name

    url_dict = {}
    #Beginning of URL to search by ISBN
    url_dict['isbn_search_beg'] = "http://classify.oclc.org/classify2/"\
              "ClassifyDemo?search-standnum-txt="
              
    # Beginning of URL to search by title/author    
    url_dict['title_search_beg'] = "http://classify.oclc.org/classify2/" \
              "ClassifyDemo?search-title-txt="
     
    # Middle of URL to search by title/author         
    url_dict['title_search_mid'] = "&search-author-txt="
    
    # Shared part of all internal links that are books to explore    
    url_dict['search_url'] = "/classify2/ClassifyDemo?wi="
    
    # Base URL to add to the internal searches
    url_dict['base_url'] = "http://classify.oclc.org"
    
    # Return the requested one
    if(name not in url_dict):
        raise ValueError(name+ ' is not a valid URL segment to look for')
        
        
    return url_dict[name]

def validate_ISBN(input_string):
# Checks the given input string to see if it is an ISBN number. 
# Returns a boolean
#
# Usage
# validate_ISBN(input_string) # returns boolean
#
# Inputs
# input_string: the string to test
#
# Outputs
# boolean if it is a ISBN
 
    # Verify the ISBN using regex
    # The first regex checks for an ISBN10 number, which has 10 digits
    # the last digit can be an x.
    # The second regex checks for an ISBN13 number, with 13 digits and no
    # special characters
    if(bool(re.search(r'^\d{9}[\d|X]$', input_string, re.IGNORECASE)) or
       bool(re.search(r'^\d{13}$', input_string)) ):
           return True
        
    print "    ERROR: ISBN is not valid. " \
               "It should contain 10 or 13 characters."
    print "           Please try again."
    return False
    
def get_classify_info(page):
# Attempts to parse a classify.oclc.org webpage and scrape the title,
# author, and LC Classification. If it fails, it will return empty
# strings for each of these values.
#
# Usage
# title, author, LCC = get_classify_info(page)
#
# Inputs
# page: The page returned by requests.get
#
# Outputs
# title: a string containing the title.
# author: a string containing the author.
# LCC: a string containing the LCC classification.
# All of these will be blank if the webpage doesn't contain this information

    # Convert the HTML file into an organized array
    soup = BeautifulSoup(page.text)

    text = soup.get_text()
    data =  filter(None,text.split('\n'))
    
    # Search for the title, author, and LCC
    try:
        data = data[data.index("Summary"):-1]
    except ValueError:
        return '','',''
    
    try:
        i_title = data.index("Title:")+1
        title = data[i_title]
    except ValueError:
        title = ''
        
    try:
        i_author = data.index("Author:")+1
        author = data[i_author]
    except ValueError:
        author = ''
        
    try:
        i_lcc = data.index("LCC:")+5
        lcc = data[i_lcc]
    except ValueError:
        lcc = ''

    # Return the data
    return title, author, lcc
    
def get_classify_search_links(page):
# Gets all links for books to search through on a classify.oclc.org
# webpage. It assumes that books will start on the 8th link
# (found through empirical testing) and will be an internal link,
# beginning with /classify2/ClassifyDemo?wi=
#
# Usage
# links = get_classify_search_links(soup)
#
# Inputs
# page: The output of responses.get(url)
#
# Outputs
# links: an array of strings, each string is a link to a search result

    # The constant part of an internal classify search link
    search_url = get_url_segment('search_url')
    
    # Extract all the hyperlinks from the webpage
    a_tags = BeautifulSoup(page.text, parse_only=SoupStrainer('a'))
    links = []
    for link in a_tags.find_all('a'):
        href = link.get('href')
        # If they match the URL for a search result, add them to the list
        if(search_url in href):
            links.append(href)
            
    return links
    
def user_validation(title,author,lcc):
# Requests the user to validate the search's results. Returns a boolean
# based off the users response.
#
# Usage
# user_validation(title, author, lcc) #Returns number
#
# Inputs:
# title: string for the title to display
# author: string for the author to display
# lcc: string for the LC classification to display
#
# Outputs
# True if user validates the info, false otherwise

    # Convert any unicode characters from title and author to ascii
    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
    author = unicodedata.normalize('NFKD', author).encode('ascii', 'ignore')
    
    # Display the titlem author and LCC
    print("\n    Title: "+title)
    print("\n    Author: "+author)
    print("\n    LC Classification: "+lcc) 
    
    # Ask user if it is correct, and give directions
    print("\nPress enter if this information is correct")
    print "Type n if the information is not correct"
    query = raw_input("\n    Is this correct? ")
    
    query = query.lower()
    # Read user input, and act on it
    if(query != "" and query != 'y' and query != 'yes'):
        print "    User indicated incorrect data. Data was not saved.\n"
        return False
    
    return True
    
def validate_info(title, author, lcc):
# Attempts to validate the data returned by a search.
# It currently ensures that a title exists, and that 
# lcc has more than 3 characters in it. The author is not checked.
#
# Usage
# validate_info(title, author, lcc) # returns boolean
#
# Inputs
# title: a string containing the title
# author: a string containing the author
# lcc: a string containing the LC Classification
#
# Outputs
# boolean: true if it appears to be a valid LCC, false otherwise

    return len(title)!=0 and len(lcc)>3
    
def title_author_search_url(title, author):
# Generates a search URL for classify.oclc.org from the title and author.
# An example URL is below
# http://classify.oclc.org/classify2/ClassifyDemo?search-title-txt=a%20b%20c&
# search-author-txt=d%20e%20f&startRec=0
#
# Usage
# url = title_author_search_url(title, author)
#
# Inputs
# title: string containing the title of the book
# author: string containing the author of the book
#
# Outputs
# url: string containing the URL
    
    # Constant parts of the URL    
    beg_url = get_url_segment('title_search_beg')
    middle_url = get_url_segment('title_search_mid')
    
    # Convert the title and author spaces to be %20
    title = title.replace(' ', '%20')
    author = author.replace(' ', '%20')
    
    return beg_url + title + middle_url + author

def isbn_search_url(isbn):
# Generates a search URL for classify.oclc.org from the isbn.
#
# Usage
# url = isbn_search_url(isbn)
#
# Inputs
# isbn: a string contain
#
# Outputs
# url: string containing the URL
    
    # Constant parts of the URL   
    
    return get_url_segment('isbn_search_beg') + isbn
    
def search_classify(*args):
# Searches classify.oclc.org for the specified ISBN or title and author.
# If it is not found, then the title, author and LCC will be blank.
#
# Usage
# title, author, lcc = search_classify(ISBN, link_limit)
# title, author, lcc = search_classify(title, author, link_limit)
#
# Inputs:
# ISBN: a string containing the ISBN
# title: a string containing the title
# author: a string containing the author
# link_limit: the number of links to search through before giving up
#             A value of -1 will search through all links.
#
# Outputs:
# title: string containing the title of the book
# author: string containing the author of the book
# lcc: string containing the LC classification of the book

    # Figure out which case we have, ISBN or title/author
    # and generate the URL
    if(len(args) == 2): # ISBN case
        ISBN = args[0]
        link_limit = args[1]
        url = isbn_search_url(ISBN)
        
    elif(len(args) == 3):
        title = args[0]
        author = args[1]
        link_limit = args[2]
        url = title_author_search_url(title, author)
    else:
        raise TypeError("Invalid number of arguments for search_classify")
        
    try: 
        page = requests.get(url)
    except requests.ConnectionError:
        print "    ERROR: Unable to access website. "\
                   "Check your internet connection."
        return '','',''

    # Attempt to get the book's information
    title, author, lcc = get_classify_info(page)

    # If I have the information, simply print that
    if(validate_info(title, author, lcc)):
        if(user_validation(title, author, lcc)):  
            return title, author, lcc
        
    # Otherwise, get the links
    links = get_classify_search_links(page)

    # Cycle through each link, searching for a valid pag014e 
    # The number of links is limited in case many links are returned
    for link in links[:link_limit]:
        
        url = get_url_segment('base_url') + link
        page = requests.get(url)
        title, author, lcc = get_classify_info(page)
        if(validate_info(title, author, lcc)):
            if(user_validation(title, author, lcc)):
                return title, author, lcc
                
        print "Searching for other options..."
            
    # If I reach here, no valid box was found, return error
    return '','',''