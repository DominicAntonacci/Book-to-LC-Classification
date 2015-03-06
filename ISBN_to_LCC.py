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

csv_file = open_isbn_csv("ISBNsLCC.csv")
    
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
    title, author, lcc = search_classify(ISBN, 5)
    
    # Check if the information was actually written
    if(not validate_info(title, author, lcc)):
        print("    ERROR: ISBN did not return any results.")
        print("           Try again, or set aside for later processing.")
        continue
        
    # Save the information to the CSV file
    csv_file.write('"'+ISBN+'","'+lcc+'"\n')
    csv_file.flush() #Force writing to the file (rather than buffering)
    
csv_file.close()
