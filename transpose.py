#!/usr/bin/env python3

import sys
import re

def get_key_from_abc(filename):
    """Extract the key from an ABC file's K: field."""
    with open(filename) as f:
        for line in f:
            if line.startswith('K:'):
                return line.split(':')[1].strip()
    raise ValueError(f"No key signature found in {filename}")

def get_transposition(key):
    """Calculate semitones needed to transpose to C."""
    # Map of keys to semitones from C
    distances = {
        'C': 0,  'C#': 1,  'Db': 1,
        'D': 2,  'D#': 3,  'Eb': 3,
        'E': 4,
        'F': 5,  'F#': 6,  'Gb': 6,
        'G': 7,  'G#': 8,  'Ab': 8,
        'A': 9,  'A#': 10, 'Bb': 10,
        'B': 11
    }
    
    # Get base key (handle both 'G' and 'Gm' etc)
    base_key = key[0]
    if len(key) > 1 and key[1] in '#b':
        base_key = key[:2]
    
    try:
        return -distances[base_key]  # Negative to transpose down to C
    except KeyError:
        raise ValueError(f"Unrecognized key: {key}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} filename.abc", file=sys.stderr)
        sys.exit(1)
    
    try:
        key = get_key_from_abc(sys.argv[1])
        trans = get_transposition(key)
        print(trans)
    except (IOError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
