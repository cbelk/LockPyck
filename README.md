![lockpyck_logo_new](https://cloud.githubusercontent.com/assets/14338983/14766519/b20ca312-09db-11e6-8557-aed94e0eb972.jpeg)

#LockPyck is a pure python password cracker powered by probabilistic context free grammars.

LockPyck uses probabilistic context free grammars to try to better model how users create their passwords. It's inspired by
the awesome techniques described in Matthew Weir's Doctoral Dissertation. This project started as a fun way to get better
acquainted with Python after going through the Violent Python book and stumbling across Weir's paper, and then became the
senior project for my CS degree. I haved released it under the GNU GPLv3 in the hopes that others may find it useful. I am
not responsible for how you use this tool or the consequnces of those actions.

LockPyck is completely standalone and requires no installation. It is written for the Python 2.x branch. The psutil module
is required for the courtesyCheck function which is used to throttle the program if memory usage gets too high. psutil
can be retrieved through a package manager like pip and installed in a virtualenv. All developement and testing on my part 
has only been done on linux boxes, but I used modules that claimed support for Windows as well.

##LockPyck has two main phases:

###Learning phase

In the learning phase, plaintext passwords are analyzed to create sequences, terminals, and associated frequencies. The
passwords are obtained from the file passed in through the command line flag (file should have one password per line). 
They are read in and processed in batches of 2,000,000 to try and take it easy on the memory.

The first step is to determine the sequence of the password. In the sequences, letters are represented by 'L', digits
by 'D', special characters by 'S' and whitespace by 'W'. Sequences are represented as list where each two consecutive 
items are grouped so the first item in the group is the character type representation and the second item is the count
of consecutive characters of that type. For example, the password '123password321' would generate the sequence 
['D', 3, 'L', 8, 'D', 3]. A pool of worker processes is used at this step to generate the sequences.

After the sequence is generated, the parts of the password corresponding to each non-terminal is isolated and stored
in a list value of the terminal dictionary. For example using the password above, the D3 (non-terminal) key of the
terminal dictionary would have the list [..., 123, 321, ...] as a value (... represents other terminals in the list).
The sequence dictionary (string version of sequence as key, frequency as value) and the ndbd dicitonary (string version
of sequence as key, list version as value) are also updated.

After these dictionaries have been updated with all of the sequences from the password batch, the sequence and ndbd
dictionaries are merged with their stale counterparts (ie Seq.freak and NDBD.freak) if they exist and then pickled
back out to their respective files. Then the terminal dictionary is processed by creating a frequency dictionary for
each terminal list, merging that dictionary  with its stale counterpart if it exist, and pickling it to its respective
file. Continuing the example from above, the list with the terminals belonging to D3 [..., 123, 321, ...] would create
the dictionary {..., 123:freq, 321:freq, ...} (freq represents the frequency for that terminal). This dictionary would
be merged with the pickled dictionary at D3.freak if one exists and pickled out to the D3.freak freaksheet. A pool of
worker processes is used at this step to generate the frequency dicitonaries and update the appropriate freaksheets.

The idea behind using freaksheets was to keep from having to analyze the same list before each run, since some lists
can be very long. Pickling was used for faster access to the already processed data.

###Cracking phase

The cracking phase is where as the name suggest, the actual cracking takes place.
