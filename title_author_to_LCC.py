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


#Number of links to search through
link_limit = 5

# Open or create CSV file for editing
while(1):
    try:
        csv_file = open_isbn_csv("TitleAuthorLCC.csv")
        break
    except IOError:
        print 'ERROR: Unable to open CSV file. '\
        'Check to see if it is open in another program or if you '\
        'have permissions to modify it. \nPress enter to continue.'
        raw_input()
    
# Main Loop
while(1):
    
    # Request an title and author from the user, and clean it up
    title = raw_input("\nEnter title: ")
    author = raw_input("Enter author: ")
    
    # Check if we should be done
    if(title == "exit"):
        break
        
    # Try to get the book's information
    title, author, lcc = search_classify(title, author, link_limit)
    
    # Check if we actually got the book's information
    if(not validate_info(title, author, lcc)):
        print("    ERROR: Title and author did not return any results.")
        print("           Try again, or set aside for later processing.")
        continue
        
    # Save the information to the CSV file
    write_title_author_csv(title, author, lcc, csv_file)
    
csv_file.close()
