#!/bin/bash

# Check if a filename was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 filename.abc"
    exit 1
fi

# Extract the key from the K: line
key=$(grep "^K:" "$1" | cut -d':' -f2 | tr -d ' ')

# Define semitone distances from C
declare -A distances
distances["C"]=0
distances["C#"]=1
distances["Db"]=1
distances["D"]=2
distances["D#"]=3
distances["Eb"]=3
distances["E"]=4
distances["F"]=5
distances["F#"]=6
distances["Gb"]=6
distances["G"]=7
distances["G#"]=8
distances["Ab"]=8
distances["A"]=9
distances["A#"]=10
distances["Bb"]=10
distances["B"]=11

# Get the base key (first character)
basekey=${key:0:1}
# Check for sharp/flat in the key
if [[ $key =~ [b#] ]]; then
    basekey=${key:0:2}
fi

# Calculate transposition needed (negative to go down to C)
if [[ -n "${distances[$basekey]}" ]]; then
    transpose=$((0 - distances[$basekey]))
    echo $transpose
else
    echo "Error: Unrecognized key $key" >&2
    exit 1
fi
