#!/usr/bin/bash

filename="$1"
while read -r line; do
    name="$line"
    rm "$name"
done < "$filename"
