# Import the Google Cloud Text-to-Speech library
from google.cloud import texttospeech


# Define the text input for speech synthesis

# Create a client for Text-to-Speech service

client = texttospeech.TextToSpeechClient()

# Read text from a file
with open("null-wavefront.txt", "r", encoding="utf-8") as file:
    text_content = file.read()

# Check if the text exceeds the API's character limit
if len(text_content) > 5000:
    print("Error: The text exceeds the 5000 character limit for a single request.")
    # Handle the error - maybe split the text into smaller chunks or truncate it
else:
    # Define the text input for speech synthesis
    input_text = texttospeech.SynthesisInput(text=text_content)


# Voice selection parameters
# You can specify the voice by name. Available voices can be listed
# using client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="es-US",  # Set the language code
    name="es-US-Studio-B",  # Specify the voice model
)

# Configuration for the audio output
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # Set the audio format
    speaking_rate=0.75  # Set the speaking rate
)

# Request to synthesize speech
response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config}
)

# Save the synthesized speech to a file
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

