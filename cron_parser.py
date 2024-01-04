# Description: Parses a cron expression and expands each field to show the times at which it will run.
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
for i in range(min(len(output_fields), len(cron_fields))):
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
   
