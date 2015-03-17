# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2015 Dominic Antonacci

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from BookToLCC import *

# Number of links to search through before giving up
link_limit = 5

while(1):
    try:
        title_csv = open_title_author_csv("TitleAuthorLCC.csv")
        isbn_csv = open_isbn_csv("ISBNsLCC.csv")
        break
    except IOError:
        print 'ERROR: Unable to open CSV file. '\
        'Check to see if it is open in another program or if you '\
        'have permissions to modify it. \nPress enter to continue.'
        raw_input()
    
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
    title, author, lcc = search_classify(ISBN, link_limit)
    
    # If the information is valid, save the info and continue
    if(validate_info(title, author, lcc)):
        # Save the information to the CSV file
        num_copies = get_num_copies()
        for _ in xrange(num_copies):
            write_isbn_csv(ISBN, lcc, isbn_csv)
        continue
    else:
        print "    ISBN did not return any results. Try the title and author."
        
    # Otherwise, prompt for title and author
    title = raw_input("\nEnter title: ")
    author = raw_input("Enter author: ")
    
    # Check if we should exit the program
    if(title == "exit"):
        break    
    
    title, author, lcc = search_classify(title, author, link_limit)
    
    # Check if we actually got the book's information
    if(not validate_info(title, author, lcc)):
        print("    ERROR: Title and author did not return any results.")
        print("           Try again, or set aside for later processing.") 
        continue
    if(validate_info(title, author, lcc)):
        num_copies = get_num_copies()
        for _ in xrange(num_copies):
            write_title_author_csv(title, author, lcc, title_csv);
        continue
    
    
    else:
        print("    ERROR: Title and author did not return any results.")
        print("           Try again, or set aside for later processing.") 
    
isbn_csv.close()
title_csv.close()

