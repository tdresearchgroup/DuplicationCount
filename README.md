# DuplicationCount
This program is designed to find cases of duplication in code.
It does this at two scales: within individual files and throughout entire directories:
get_file_duplicates and get_dir_duplicates, respectively.

There are two key parameters to both scales: line_trim and count_trim
In the example statement in the main function, they are set at 30 and 5 respectively.
Setting the line_trim to 30 means that any line of code with fewer than 30 characters 
(excluding any leading or trailing whitespace) will be ignored.
This is useful in discarding common short statements such as "else:".
Setting the count_trim to 5 means that a line must be duplicated at least 5 times before it is flagged.
This is useful since it helps focus on which lines are the most duplicated. 
Setting this number to 0 will flag every line of code above the line_trim.

get_file_duplicates only returns a dictionary where the keys are lines of code and the values are the number of duplications for each key.

get_dir_duplicates returns a similar dictionary and has the option of outputing it to a csv file.
The main distinction between the two dictionaries is that get_dir_duplicates includes all the filenames where the line of code was found.
