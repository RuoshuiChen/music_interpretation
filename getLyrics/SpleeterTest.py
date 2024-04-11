import requests
import numpy as np
import soundfile as sf
#!/usr/bin/env python
from aeneas.executetask import ExecuteTask

# Function to separate vocals using Spleeter API
def separate_vocals(song_path, output_path):
    # Spleeter API endpoint
    api_url = 'https://api.spleeter.ai/v1/separate'

    # Parameters for the separation
    payload = {
        'audio': open(song_path, 'rb'),
        'stems': 'vocals',
        'nfft': 2048,
        'overlap': 0.5
    }

    # Send POST request to the API
    response = requests.post(api_url, files=payload)

    # Retrieve the vocals from the response
    vocals = np.frombuffer(response.content, np.float32)

    # Save the vocals to an MP3 file
    sf.write(output_path, vocals, 44100, format='MP3')


# Example usage
song_path = 'Breaking All Illusions-HZlYCvamxKM.mp3'  # Replace with the path to your input song
output_path = 'SpleeterTest.mp3'  # Replace with the desired output path

separate_vocals(song_path, output_path)
