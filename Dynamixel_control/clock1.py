import pyaudio
import wave
import json
import time
import sys



CHUNK = 1024
sr = 44100

# if len(sys.argv) < 2:
#     print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
#     sys.exit(-1)
path = "music&data/rock/De_do_do_do"
json_data = path + ".json"
wave_data = path + ".wav"
#music = AudioSegment.from_file(wav)
file = open(json_data)
json_file = json.load(file)
beats = json_file["beats"]
# if len(sys.argv) < 2:
#     print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
#     sys.exit(-1)

with wave.open("music&data/rock/De_do_do_do.wav", 'rb') as wf:
    # Define callback for playback (1)
    def callback(in_data, frame_count, time_info, status):
        global beats_count
        global curr_frame
        data = wf.readframes(frame_count)
        curr_frame += frame_count
        # If len(data) is less than requested frame_count, PyAudio automatically
        # assumes the stream is finished, and the stream stops.
        if curr_frame >= int(beats[beats_count]*sr):
            print("beat")
            beats_count += 1
        return(data, pyaudio.paContinue)


    # Instantiate PyAudio and initialize PortAudio system resources (2)
    p = pyaudio.PyAudio()
    beats_count = 0
    curr_frame = 0
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    # Open stream using callback (3)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback,
                    input_device_index=22)

    # Wait for stream to finish (4)
    while stream.is_active():
        time.sleep(0.1)

    # Close the stream (5)
    stream.close()

    # Release PortAudio system resources (6)
    p.terminate()