#!/bin/bash

# Check if a filename was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 filename.abc"
    exit 1
fi

# Extract the key from the K: line
key=$(grep "^K:" "$1" | cut -d':' -f2 | tr -d ' ')

# Define semitone distances from C
declare -A distances=(
    ["C"]=0  ["C#"]=1  ["Db"]=1
    ["D"]=2  ["D#"]=3  ["Eb"]=3
    ["E"]=4
    ["F"]=5  ["F#"]=6  ["Gb"]=6
    ["G"]=7  ["G#"]=8  ["Ab"]=8
    ["A"]=9  ["A#"]=10 ["Bb"]=10
    ["B"]=11
)

# Get the base key (first character)
basekey=${key:0:1}
# Check for sharp/flat in the key
if [[ $key =~ [b#] ]]; then
    basekey=${key:0:2}
fi

# Calculate transposition needed (negative to go down to C)
if [ ${distances[$basekey]+_} ]; then
    transpose=$((0 - ${distances[$basekey]}))
    echo $transpose
else
    echo "Error: Unrecognized key $key" >&2
    exit 1
fi
