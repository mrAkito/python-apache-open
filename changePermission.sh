#!/bin/bash

FILE_PATH=$1

DEST_DIR="/var/www/html"

APACHE_USER="apache"

if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR"
fi

if [ -f "$FILE_PATH" ]; then
    DEST_FILE="$DEST_DIR/$(basename $FILE_PATH)"
    mv "$FILE_PATH" "$DEST_DIR"
    chown $APACHE_USER:$APACHE_USER "$DEST_FILE"
    echo "File moved to $DEST_DIR"
else
    echo "File not found: $FILE_PATH"
    exit 1
fi


