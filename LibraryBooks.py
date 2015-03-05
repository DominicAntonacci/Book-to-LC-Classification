# Libraries to import
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
import os.path
import unicodedata
#from colorama import init, Fore, Back
#init(autoreset=True)

# User-defined functions

# Checks the given input string to see if it is an ISBN number. Returns true if it is, false if not
# This verifies that it is a 10 or 13 digit number
#
# Usage
# validate_ISBN(input_string) # returns boolean
#
# Inputs
# input_string: the string to test
#
# Outputs
# boolean if it is a ISBN
def validate_ISBN(input_string):
    
    # Verify the ISBN using regex
    if(bool(isbn10.search(input_string)) or bool(isbn13.search(input_string))):
        return True
        
    print "    ERROR: ISBN is not valid. It should contain 10 or 13 characters."
    print "           Please try again."
    return False
    if(not ISBN.isdigit()):
        print("    ERROR: ISBN contains non-numeric characters. Please try again.")
        return False

    # Verify that the text is 10 or 13 characters long
    if(len(ISBN) != 10 and len(ISBN) != 13):
        print("    ERROR: ISBN length is not valid. It should be 10 or 13 digits long. Please try again.")
        return False
    
    return True


def get_HTML_text(url):
# Takes a given URL and converts it to a list of strings, where each element is the text in a field
# Returns a list of strings with each element containing the text in a
# HTML field
#
# Usage
# data = get_HTML_text(url)
#
# Inputs:
# url - a string URL to access
# 
# Outputs:
# data - the resulting list of strings

    # Get and parse the URL
    page = requests.get(url)
    soup = BeautifulSoup(page.text)

    # Convert the text into a nice list of fields
    text = soup.get_text()
    return filter(None,text.split('\n'))

def get_classify_info(page):
# Attempts to parse a classify.oclc.org webpage and scrape the title,
# author, and LC Classification. If it fails, it will return empty
# strings for each of these values.
#
# Usage
# title, author, LCC = get_classify_info(page)
#
# Inputs
# page: The array of strings returned by get_HTML_text
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


def search_classify(ISBN):
# Searches classify.oclc.org for the specified ISBN. If it is not
# found, then the title, author and LCC will be blank.
#
#
# Usage
# title, author, lcc = search_classify(ISBN)
#
# Inputs:
# ISBN: a string containing the ISBN
#
# Outputs:
# title: string containing the title of the book
# author: string containing the author of the book
# lcc: string containing the LC classification of the book

    # Generate the URL and get webpage
    url = cl_url_beg + ISBN + cl_url_end
    try: 
        page = requests.get(url)
    except requests.ConnectionError:
        print "    ERROR: Unable to access website. Check your internet connection."
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
        
        url = base_url+link
        page = requests.get(url)
        title, author, lcc = get_classify_info(page)
        if(validate_info(title, author, lcc)):
            if(user_validation(title, author, lcc)):
                return title, author, lcc
                
        print "Searching for other options..."
            
    # If I reach here, no valid box was found, return error
    return '','',''

#-----------------------------------------------------------------------------

# Parameters

# Base URL of site, used when going to internal links
base_url = "http://classify.oclc.org"

# Beginning and end of the classify.oclc.org search terms
cl_url_beg = "http://classify.oclc.org/classify2/ClassifyDemo?search-standnum-txt="
cl_url_end = "&startRec=0"

# String to distinguish search results from other hyperlinks
search_url = "/classify2/ClassifyDemo?wi="

# Name of the CSV file to save results to
csv_file_name = "ISBNsLCC.csv"

# Regex to limit an ISBN to have only the digits 0-9
isbn10 = re.compile(r'^\d{9}[\d|X]$', re.IGNORECASE)
isbn13 = re.compile(r'^\d{13}$')

# Limit for the number of links allowed to search through
link_limit = 5 # -1 means there is no limit

# Create the csv file if it doesn't already exist
if(not os.path.isfile(csv_file_name)):
    csv_file = open(csv_file_name,'w', 1) #open file, and set to line buffering
    csv_file.write('"ISBN","Call_Number"\n')
else:
    csv_file = open(csv_file_name,'a', 1) # Set line buffering
    
# Main Loop
while(1):
    
    # Request an ISBN number from the user, and clean it up
    ISBN = raw_input("\nEnter ISBN: ")
    ISBN = ''.join(ISBN.split()) #Remove all whitespace
    ISBN = ISBN.replace("-","") #Remove all hyphens
    
    # Check if we should be done
    if(ISBN == "exit"):
        break

    # Verify the ISBN has a valid format, if not, break
    if(not validate_ISBN(ISBN)):
        continue
        
    # Try to get the book's information
    title, author, lcc = search_classify(ISBN)
    
    # Check if the information was actually written
    if(not validate_info(title, author, lcc)):
        print("    ERROR: ISBN did not return any results.")
        print("           Try again, or set aside for later processing.")
        continue
        
    # Save the information to the CSV file
    csv_file.write('"'+ISBN+'","'+lcc+'"\n')
    csv_file.flush() #Force writing to the file (rather than buffering)
    
csv_file.close()
