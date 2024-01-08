# Description: Parses a cron expression and expands each field to show the times at which it will run.
import sys
import calendar


def parseField(field, min_value, max_value, month=None):
    global curr_year
    if field == '*':
        return list(range(min_value, max_value + 1))
    elif field.isdigit():
        val = int(field)
        if min_value <= val <= max_value:
            return [val]
        else:
            print("Error: Invalid value in the cron expression.")
            sys.exit(1)
    elif field.startswith('*/'):
        step = int(field[2:])
        if step == 0 or step > max_value:
            print("Error: Invalid step value in the cron expression.")
            sys.exit(1)
        return list(range(min_value, max_value + 1, step))
    elif ',' in field:
        values = [int(value) for value in field.split(',')]
        for value in values:
            if value < min_value or value > max_value:
                print("Error: Invalid value in the cron expression.")
                sys.exit(1)
        return values
    elif '-' in field:
        start, end = map(int, field.split('-'))
        if start < min_value or end > max_value:
            print("Error: Invalid value in the cron expression.")
            sys.exit(1)
        return list(range(start, end + 1))

    else:
        return []


def getLastDayOfMonth(month):
    # check if month is a number
    if month.isdigit():
        return calendar.monthrange(curr_year, int(month))[1]
    else:
        return 31


# Take input from the command line and split into cron expression
cron_fields = sys.argv[1].split()
curr_year = 2024
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
    else:
        values = parseField(cron_field, 0, 59) if output_field == 'minute' else \
            (parseField(cron_field, 0, 23) if output_field == 'hour' else (parseField(cron_field, 1, getLastDayOfMonth(cron_fields[3])) if output_field == 'day of month' else (parseField(cron_field, 1, 12) if output_field == 'month' else (parseField(cron_field, 0, 6) if output_field == 'day of week' else []))))
        print(output_field, ' '.join(map(str, values)))

