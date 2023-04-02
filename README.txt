This is a mini proposal for a 106AP assignment probably after students have learned tuples and dictionaries

This project actually started with me trying to get a friend with an android into a blue imessage groupchat.
It turns out that on macs, all imessages are stored in a SQL database in your user folder. I did some digging around,
and it turns out that with a little magic you can access that database programmatically and pull out the text info.

The idea for the assignment is that we provide a database file with some example texts and the wrapper file to get the data,
and students write a few functions to manipulate it:

1. format_message: given a tuple representing message info, create a string that displays the info in pretty form
2. response time: given a list of tuples representing a text conversation,
 use the metadata (date and is_sent properties) to calculate the average response time between two people
3. search: given a dictionary representing a series of text conversations,
  pull out messages containing a certain keyword with a couple messages of surrounding context
4. a main function where students implement a couple keyword arguments to either print
  (a) all texts in a given date range
  (b) all texts matching search function
  (c) response time in a given conversation


Techincal info:
*main files to look at are assignment_dependency_wrappers.py and solution.py

assignment depends on macmessage library (included in zip)
which depends on pandas library (must be installed with pip)

Files:
assignment_dependency_wrappers.py
wrappers to convert data from macmessage library into a simpler form for students

starter.py
starter code

solution.py
solution code
Note - while assignment wise should use provided data, this should work on a real mac
