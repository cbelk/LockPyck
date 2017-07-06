![lockpyck_logo_new](https://cloud.githubusercontent.com/assets/14338983/14766519/b20ca312-09db-11e6-8557-aed94e0eb972.jpeg)

# LockPyck is a pure python password cracker powered by probabilistic context free grammars.

LockPyck uses probabilistic context free grammars to try to better model how users create their passwords. It's inspired by
the awesome techniques described in Matthew Weir's Doctoral Dissertation. This project started as a fun way to get better
acquainted with Python after going through the Violent Python book and stumbling across Weir's paper, and then became the
senior project for my CS degree. I haved released it under the GNU GPLv3 in the hopes that others may find it useful. I am
not responsible for how you use this tool or the consequnces of those actions.

LockPyck is completely standalone and requires no installation. It is written for the Python 2.x branch. The psutil module
is required for the courtesyCheck function which is used to throttle the program if memory usage gets too high. psutil
can be retrieved through a package manager like pip and installed in a virtualenv. All developement and testing on my part 
has only been done on linux boxes.

## LockPyck has two main phases:

### Learning phase

In the learning phase, plaintext passwords are analyzed to create sequences, terminals, and associated frequencies. The
passwords are obtained from the file passed in through the command line flag (file should have one password per line). 
They are read in and processed in batches of 2,000,000 to try and take it easy on the memory.

The first step is to determine the sequence of the password. In the sequences, letters are represented by 'L', digits
by 'D', special characters by 'S' and whitespace by 'W'. Sequences are represented as list where each two consecutive 
items are grouped so the first item in the group is the character type representation and the second item is the count
of consecutive characters of that type. For example, the password '123password321' would generate the sequence 
['D', 3, 'L', 8, 'D', 3]. The two grouped elements (eg D3) is referred to as a non-terminal. A pool of worker processes 
is used at this step to generate the sequences.

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

### Cracking phase

The cracking phase is where, as the name suggest, the actual cracking takes place. The freaksheets created during
the learning phase will now be used to generate password guesses in a probabilistic order. The hashes to be cracked
should be stored in a file (one hash per line), and the absolute path to the file passed in via the -c flag.

When the cracking phase starts, the following two daemons are fired up:

#### notdbd
The notdbd daemon is responsible for generating the pre-terminals and adding them to the queue to be consumed by
the pycks. Pre-terminals are basically non-terminal strings that have only one non-terminal. Continuing with our
example, 123passwordD3 would be a non-terminal that would produce our password (assuming '321' has been learned
before). The way notdbd generates pre-terminals is to hold the last non-terminal in the sequence as the non-
terminal in the pre-terminal. Preterminals are represented as list, so our pre-terminal above would be ['123password', 'D3'].

The notdbd function first retrieves the sequences in a list sorted by descending frequencies. Then for each sequence,
it removes the last non-terminal, and uses the other non-terminals to generate a list of lists to represent the sets.
Each of these lists in the list is sorted by descending frequencies as well. For example, the sequence D3L8D3 would 
produce a list whose first value would be a list containing all of the elements from D3.freak in descending order of
frequencies, and whose second value would be a list containing all of the elements from L8.freak also in descending
order. This list of lists along with the non-terminal would be passed to the cartesianPreterms function.

The cartesianPreterms algorithm is used to generate the actual pre-terminals and add them to the queue. As it generates
each element of the cartesian product, it appends the non-terminal which produces a pre-terminal. This is then added
to the queue for the pycks to consume. The reason I wrote my own cartesian product function is because the built-in
function generates all elements before returning them as a list of tuples. Given that these sets can get very large,
having the entire cartesian product generated before they could be turned into pre-terminals and consumed resulted
in the RAM being flooded and many forced reboots.

#### hash_man
The hash_man daemon is responsible for managing the list of hashes to be cracked and successful cracks. Successful
cracks are added to a queue to be consumed by hash_man. When it gets successes, it first prints them to screen and 
writes them to the cracked file. The cracked passwords are then feed through the learning process and the appropriate
freaksheets are updated. When all of the hashes have been cracked, hash_man informs the other processes so they can
begin terminating.

#### super_pyck
The super_pyck sub-driver is used to drive the pycking process. It retrieves the pre-terminals from the queue and
prepares the work that it will pass to a pool of workers running the pyck's cutTheKey function. Each worker
retrieves a list containing the elements from the freaksheet associated with the non-terminal in the pre-terminal
sorted in descending order. It then begins to plug these elements into the pre-terminal to generate a password
guess which is then hashed and compared to the list of hashes to be cracked. Successful cracks are returned to
super_pyck which adds them to the queue for hash_man to consume.

*Throttling is used in the notdbd and super_pyck functions to prevent memory flooding.*

#### Poisoning
A poison pill approach is used for communication between the processes. Both queue (the pre-terminal queue) and 
poison_queue are used for poisoning. The poisoning rules are:

-   hash_man can poison super_pyck and notdbd by placing poison pills in the poison_queue. This is done when all
    of the hashes have been cracked. All processes terminate upon receiving this pill.

-   notdbd can poison super_pyck by placing a poison pill in the pre-terminal queue. This is done when all pre-
    terminals have been generated.

-   super_pyck can poison hash_man by placing a poison pill in the poison_queue. This is done after getting poisoned
    by notdbd and passing any remaining successes to hash_man. hash_man will check the success queue one last time
    after getting poisoned.
