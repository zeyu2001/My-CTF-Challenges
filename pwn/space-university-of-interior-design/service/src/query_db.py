#!/usr/bin/python3
import os
import tempfile
import argparse


def query_db(row):
    
    if not row:
        row = 'FirstName'

    sql = f".open /home/jared/chinook.db\nSELECT {row} FROM employees;"
    os.system(f'echo "{sql}" | /usr/bin/sqlite3')

    print("Done!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--row", help="Row to query")
    args = parser.parse_args()

    query_db(args.row)
