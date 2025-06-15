#!/usr/bin/env python3

import os
import subprocess
import typer
import csv
from pathlib import Path
from typing import Optional
import rich

app = typer.Typer()

@app.command()
def list():
    """List all ABC files in the ./abc directory."""
    abc_dir = Path('abc')
    if not abc_dir.exists():
        typer.echo("ABC directory not found!", err=True)
        raise typer.Exit(1)
        
    files = sorted(abc_dir.glob('*.abc'))
    if not files:
        typer.echo("No ABC files found!")
        return
        
    typer.echo("Available ABC files:")
    for file in files:
        typer.echo(f"  {file.name}")

def get_key_from_abc(filename: Path) -> str:
    """Extract the key from an ABC file's K: field."""
    with open(filename) as f:
        for line in f:
            if line.startswith('K:'):
                return line.split(':')[1].strip()
    raise ValueError(f"No key signature found in {filename}")

def get_transposition(key: str) -> int:
    """Calculate semitones needed to transpose to C."""
    distances = {
        'C': 0,  'C#': 1,  'Db': 1,
        'D': 2,  'D#': 3,  'Eb': 3,
        'E': 4,
        'F': 5,  'F#': 6,  'Gb': 6,
        'G': 7,  'G#': 8,  'Ab': 8,
        'A': 9,  'A#': 10, 'Bb': 10,
        'B': 11
    }
    
    base_key = key[0]
    if len(key) > 1 and key[1] in '#b':
        base_key = key[:2]
    
    try:
        return -distances[base_key]  # Negative to transpose down to C
    except KeyError:
        raise ValueError(f"Unrecognized key: {key}")

def transpose_abc(input_file: Path, output_file: Path, semitones: int) -> None:
    """Transpose ABC file by given number of semitones."""
    subprocess.run(['abc2abc', str(input_file), '-t', str(semitones)], 
                  stdout=open(output_file, 'w'),
                  check=True)

def abc_to_midi(abc_file: Path, midi_file: Path) -> None:
    """Convert ABC to MIDI."""
    subprocess.run(['abc2midi', str(abc_file), '-o', str(midi_file)], 
                  check=True)

def midi_to_mp3(midi_file: Path, mp3_file: Path) -> None:
    """Convert MIDI to MP3 using timidity and lame."""
    subprocess.run(
        f'timidity {midi_file} -Ow -o - | lame - {mp3_file}',
        shell=True,
        check=True
    )

@app.command()
def process(
    filename: str,
    transpose: bool = True,
    render: bool = True,
    key: Optional[str] = 'C',
    output_dir: Path = Path('mp3')
) -> None:
    """Process an ABC file: optionally transpose it and render to MP3."""

    try:
        # Handle file paths
        input_path = Path(filename)
        if not input_path.suffix:
            input_path = input_path.with_suffix('.abc')
        
        # Try current directory first, then ./abc directory
        if not input_path.exists():
            abc_path = Path('abc') / input_path
            if abc_path.exists():
                input_path = abc_path
            else:
                raise typer.BadParameter(f"File not found in current directory or ./abc: {input_path}")
            
        base_name = input_path.stem
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Transposition
        if transpose:
            orig_key = get_key_from_abc(input_path)
            semitones = get_transposition(orig_key)
            transposed_file = output_dir / f"{base_name}-in-{key.lower()}.abc"
            transpose_abc(input_path, transposed_file, semitones)
            typer.echo(f"Transposed to {key}: {transposed_file}")
            working_file = transposed_file
        else:
            working_file = input_path
            
        # Rendering
        if render:
            midi_file = output_dir / f"{base_name}.mid"
            mp3_file = output_dir / f"{base_name}.mp3"
            
            abc_to_midi(working_file, midi_file)
            typer.echo(f"Created MIDI: {midi_file}")
            
            midi_to_mp3(midi_file, mp3_file)
            typer.echo(f"Created MP3: {mp3_file}")
            
            # Clean up intermediate files
            midi_file.unlink()
            if transpose:
                working_file.unlink()  # Remove the transposed ABC file
            
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error in external command: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def process_all(
    transpose: bool = True,
    render: bool = True,
    key: Optional[str] = 'C',
    output_dir: Path = Path('mp3')
) -> None:
    """Process all ABC files in the ./abc directory."""
    abc_dir = Path('abc')
    if not abc_dir.exists():
        typer.echo("ABC directory not found!", err=True)
        raise typer.Exit(1)
        
    files = sorted(abc_dir.glob('*.abc'))
    if not files:
        typer.echo("No ABC files found!")
        return

    output_dir.mkdir(exist_ok=True)
    
    for file in files:
        typer.echo(f"\nProcessing {file.name}...")
        try:
            process(
                filename=str(file),
                transpose=transpose,
                render=render,
                key=key,
                output_dir=output_dir
            )
        except Exception as e:
            typer.echo(f"Error processing {file.name}: {e}", err=True)
            continue

@app.command()
def make_flashcards(output_file: Path = Path("music_flashcards.csv")):
    """Create Anki flashcards for all MP3 files."""
    mp3_dir = Path('mp3')
    if not mp3_dir.exists():
        typer.echo("MP3 directory not found!", err=True)
        raise typer.Exit(1)
        
    files = sorted(mp3_dir.glob('*.mp3'))
    if not files:
        typer.echo("No MP3 files found!")
        return

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["Front", "Back"])
        # Write a row for each song
        for file in files:
            writer.writerow([f"[sound:{file.absolute()}]", "Play this song"])
    
    typer.echo(f"Created flashcards file: {output_file}")

if __name__ == "__main__":
    app()
