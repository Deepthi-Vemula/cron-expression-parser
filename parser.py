""" Write a command line application or script which parses a cron string and expands each field to show the times at which it will run. You may use whichever language you feel most comfortable with.
Please do not use existing cron parser libraries for this exercise. Whilst it’s generally a good idea to use pre-built libraries, we want to assess your ability to create your own!
You should only consider the standard cron format with five time fields (minute, hour, day of month, month, and day of week) plus a command, and you do not need to handle the special time strings such as "@yearly". The input will be on a single line.
The cron string will be passed to your application as a single argument.
~$ your-program "d"
The output should be formatted as a table with the field name taking the first 14 columns and
the times as a space-separated list following it. For example, the following input argument:
Should yield the following output:
   */15 0 1,15 * 1-5 /usr/bin/find
 
minute 0 15 30 45
hour 0
day of month 1 15
month 1 2 3 4 5 6 7 8 9 10 11 12
day of week 1 2345
command /usr/bin/find
You should spend no more than three hours on this exercise. If you do not have time to handle all possible cron strings then an app which handles a subset of them correctly is better than one which does not run or produces incorrect results. You will be asked to extend the solution with additional features in the interview, so please have your development environment ready in the way you like it, ready for screen sharing.
You should see your project reviewer as a new team member you are handling the project over to. Provide everything you feel would be relevant for them to ramp up quickly, such as
tests, a README and instructions for how to run your project in a clean OS X/Linux environment. """

import sys
import calendar

def parseField(field, min_value, max_value, month=None):
    if field == '*':
        return list(range(min_value, max_value + 1))
    elif field.isdigit():
        return [int(field)]
    elif field.startswith('*/'):
        step = int(field[2:])
        return list(range(min_value, max_value + 1, step))
    elif ',' in field:
        values = [int(value) for value in field.split(',')]
        return values
    elif '-' in field:
        start, end = map(int, field.split('-'))
        return list(range(start, end + 1))
    elif field == 'L':
        # Last day of the month
        if month is not None:
            return [calendar.monthrange(2000, month)[1]]
        else:
            return []
    else:
        return []

# Take input from the command line and split into cron expression
cron_fields = sys.argv[1].split()

# Split into output fields
output_fields = ['minute', 'hour', 'day of month', 'month', 'day of week', 'command']

# Input validation
if len(cron_fields) != len(output_fields):
    print("Error: Invalid number of fields in the cron expression.")
    sys.exit(1)

# Traverse through each field, compute the value, and print
for i in range(len(output_fields)):
    cron_field = cron_fields[i]
    output_field = output_fields[i]
    # Parse the cron field and print the output
    if output_field == 'command':
        print(output_field, cron_field)
    elif output_field == 'day of month':
        # Determine the month (assuming it's the previous field)
        month_field = cron_fields[3] if len(cron_fields) > 3 else None
        month_value = int(month_field) if month_field and month_field.isdigit() else None
        values = parseField(cron_field, 1, calendar.monthrange(2000, month_value)[1] if month_value else 31, month_value)
        print(output_field, ' '.join(map(str, values)))
    else:
        values = parseField(cron_field, 0, 59) if output_field == 'minute' else \
                 (parseField(cron_field, 0, 23) if output_field == 'hour' else \
                 (parseField(cron_field, 1, 12) if output_field == 'month' else \
                 (parseField(cron_field, 0, 6) if output_field == 'day of week' else [])))
        print(output_field, ' '.join(map(str, values)))
   
