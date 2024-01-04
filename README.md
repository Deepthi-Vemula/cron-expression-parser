 The file parser.py is used to execute the program. The program takes two arguments, the first argument is the cron expression and the second argument is the command. The program parses the cron expression and prints the output in the format specified in the problem statement. The program is written in Python 3.6. The input is in the following format.
 
         ~$ your-program "d"

 Simple example of how the program is executed:
 
         ~$ python3 cron_parser.py "*/15 0 1,15 * 1-5 find"

The output of the program is as follows:
    
        minute         0 15 30 45
        hour           0
        day of month   1 15
        month          1 2 3 4 5 6 7 8 9 10 11 12
        day of week    1 2 3 4 5
        command        find
