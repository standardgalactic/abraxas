import logging
from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence

# Set up logging
logging.basicConfig(filename='chord_extraction.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of MP3 files to extract chords from
files_to_extract_from = [
    '01 - The Abyss Within.mp3',
    '02 - Beyond Good and Evil.mp3',
    '03 - Deserted Island Blues.mp3',
    '04 - Visions of the Canvas.mp3',
    '05 - Amnesiac Love.mp3',
    '06 - Raccoon Ruckus.mp3',
    '07 - Free From Desire.mp3',
    '08 - Picture the Scene.mp3',
    '09 - Humanity Dethroned.mp3',
    '10 - In the Depths of Existence.mp3',
    '11 - Beyond Illusions.mp3',
    '12 - Code to the Beats.mp3',
    '13 - Guardians of Tomorrow.mp3',
    '14 - Bread-Quail Wisdom.mp3',
    '15 - Intersubjectivity Collapse.mp3',
    '16 - Cultural Shift.mp3',
    '17 - My Boots are Worn.mp3',
    '18 - Shattered Dreams.mp3',
    '19 - Genius Prodigy and Talent.mp3',
    '20 - Hack the Planet.mp3',
    '21 - Vertical Scaling.mp3',
    '22 - Carmen Scientiae.mp3',
    '23 - Regal Wind.mp3',
    '24 - I am in Need of Music.mp3'
]

# Create the Chordino object
chordino = Chordino()

# Function to save extracted chords to a text file and handle errors
def save_to_db_cb(results: LabelledChordSequence):
    song_name = results.id  # Get the song's identifier (file name)
    chords = results.sequence  # Get the list of chord changes
    
    # Open the file in append mode
    with open("chords_by_song.txt", "a") as file:
        file.write(f"Song: {song_name}\n")
        for chord_change in chords:
            file.write(f"Chord: {chord_change.chord}, Time: {chord_change.timestamp}\n")
        file.write("\n")

# Optionally clear cache of file conversions
clear_conversion_cache()

# Run bulk extraction with better error handling and logging
for file in files_to_extract_from:
    try:
        logging.info(f"Processing: {file}")
        res = chordino.extract_many([file], callback=save_to_db_cb, 
                                    num_extractors=2, num_preprocessors=2, 
                                    max_files_in_cache=10, stop_on_error=False)
        logging.info(f"Successfully processed: {file}")
    except Exception as e:
        logging.error(f"Failed to process {file} with error: {e}")
