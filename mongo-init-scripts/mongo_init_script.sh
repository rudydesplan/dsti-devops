#!/bin/bash

# create a user with read and write access to the avocado_db database
mongo -- "$MONGO_INITDB_DATABASE" <<EOF
    db.createUser({
        user: "$MONGO_INITDB_USERNAME",
        pwd: "$MONGO_INITDB_PASSWORD",
        roles: [{
            role: "dbOwner",
            db: "$MONGO_INITDB_DATABASE"
        }]
    })
EOF
