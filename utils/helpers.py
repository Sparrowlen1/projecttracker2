from datetime import datetime
from prettytable import PrettyTable
from dateutil import parser

def validate_email(email):
    return '@' in email and '.' in email

def format_date(date_string):
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime('%Y-%m-%d')
    except:
        return date_string

def display_table(title, headers, rows):
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
    print(f"\nhowdyt! {title}")
    print(table)

def generate_id(prefix, existing_ids):
    counter = 1
    while f"{prefix}{counter}" in existing_ids:
        counter += 1
    return f"{prefix}{counter}"