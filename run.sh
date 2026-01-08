set -e
#!/bin/sh

# This script is for creating db, tables with correspondent values

# create db, tables
python create_table.py
# create values and send to db
python seed.py