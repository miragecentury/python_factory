#!/usr/bin/env bash

# Delete all database except admin, local and config

# Get all databases
databases=$(mongosh --quiet --eval "db.getMongo().getDBNames()" --json | jq -r '.[]')

# Loop through all databases
for db in $databases
do
    # Skip admin, local and config databases
    if [ "$db" != "admin" ] && [ "$db" != "local" ] && [ "$db" != "config" ]
    then
        # Drop database
        mongosh $db --eval "db.dropDatabase()"
    fi
done
