Book to LC Classification

What is it?
-----------
These programs (and library) make it easy to find a book's Library of
Congress Classification (LCC). The Library of Congress cataloging system is
used in many major university libraries and is commonly used book lover's
collections. 
For more information about the system, visit www.loc.gov/catdir/cpso/lcc.html

The two written programs are also designed to create CSV files to add to a
book database (specifically Readerware 3.0, but many others would likely
work). See below for more information.

ISBN_to_LCC.py - This program accepts an ISBN as an input and will search for
a matching LCC through www.classify.oclc.org

title_author_to_LCC.py - This program asks for a title and author for a book
and will search for a matching LCC through www.classify.oclc.org

Installing
----------
This program uses Python 2.7 as well as a few additional libraries. All the
libraries are included with Anaconda Python
(https://store.continuum.io/cshop/anaconda)

If you do not wish to install Anaconda, the libraries necessary are
bs4 (www.crummy.com/software/BeautifulSoup/
requests (docs.python-requests.org/)

Running the two included programs is simple, simply enter the directory in the
terminal and type
python (prog_name).py

Interface with Readerware 3.0
-----------------------------

Readerware 3.0 (www.readerware.com) is commercial software designed to keep
track of a library of books. To build the library, it is possible to import
CSV files with various fields. The two prewritten programs automatically
generate CSV files that will interface with Readerware 3.0.

Currently, Readerware does not support importing information from
classify.oclc.org, meaning that while it supports LCC, it is difficult to
identify the proper call numbers. In addition, Readerware does not currenlty
have a system to quickly display the LCC for you to write down when labeling
individual books. This software helps solve that problem.

After importing one of the CSV files, it is important to run an Auto-update to
fill out the missing information. This program purposely leaves out all
unnecessary information because classify.oclc.org can sometimes give
long/non-ideal search results. Readerware does a better job of parsing other
websites.

License
-------

This software is licensed with the MIT License. For more information, see
License.txt

Author
------

Dominic Antonacci (dominic.antonacci@gmail.com)
