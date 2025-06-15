#!/bin/bash

# Check if a filename was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 filename.abc"
    exit 1
fi

# Extract the key from the K: line
key=$(grep "^K:" "$1" | cut -d':' -f2 | tr -d ' ')

# Get the base key (first character)
basekey=${key:0:1}
# Check for sharp/flat in the key
if [[ $key =~ [b#] ]]; then
    basekey=${key:0:2}
fi

# Calculate transposition needed (negative to go down to C)
case $basekey in
    "C")  echo "0" ;;
    "C#") echo "-1" ;;
    "Db") echo "-1" ;;
    "D")  echo "-2" ;;
    "D#") echo "-3" ;;
    "Eb") echo "-3" ;;
    "E")  echo "-4" ;;
    "F")  echo "-5" ;;
    "F#") echo "-6" ;;
    "Gb") echo "-6" ;;
    "G")  echo "-7" ;;
    "G#") echo "-8" ;;
    "Ab") echo "-8" ;;
    "A")  echo "-9" ;;
    "A#") echo "-10" ;;
    "Bb") echo "-10" ;;
    "B")  echo "-11" ;;
    *)    echo "Error: Unrecognized key $key" >&2; exit 1 ;;
esac
