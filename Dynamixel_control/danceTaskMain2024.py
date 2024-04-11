import socket
from time import sleep
import json
import subprocess
from shimi_dances_offline import *
from DxlThreading import *
import time
import random
import threading

tempo_data = []
seg_data = []
beats_data = []
_play = False
wav = ""
lyrics_time_list = []
genre = ""
motors_control = motorsThreading()
motors_control.dance_thread.start()

funk1 = ShimiDanceOffline(motors_control, "Gestures/funk_1.csv")
funk1_max = 0.5
funk2 = ShimiDanceOffline(motors_control, "Gestures/funk_2.csv")
funk2_max = 2.5
funk3 = ShimiDanceOffline(motors_control, "Gestures/funk_3.csv")
funk3_max = 2.5
funk4 = ShimiDanceOffline(motors_control, "Gestures/funk_5.csv")
funk4_max = 2.5
edm1 = ShimiDanceOffline(motors_control, "Gestures/edm_1.csv")
edm1_max = 3.5
edm2 = ShimiDanceOffline(motors_control, "Gestures/edm_2.csv")
edm2_max = 2.5
edm3 = ShimiDanceOffline(motors_control, "Gestures/edm_3.csv")
edm3_max = 2.5
edm4 = ShimiDanceOffline(motors_control, "Gestures/edm_4.csv")
edm4_max = 2.5
rock1 = ShimiDanceOffline(motors_control, "Gestures/rock_1.csv")
rock1_max = 0.5
rock2 = ShimiDanceOffline(motors_control, "Gestures/rock_2.csv")
rock2_max = 2.5
rock3 = ShimiDanceOffline(motors_control, "Gestures/rock_3.csv")
rock3_max = 2.5
rock4 = ShimiDanceOffline(motors_control, "Gestures/rock_4.csv")
rock4_max = 2.5
pop1 = ShimiDanceOffline(motors_control, "Gestures/pop_1.csv")
pop1_max = 0.5
pop2 = ShimiDanceOffline(motors_control, "Gestures/pop_2.csv")
pop2_max = 1.5
pop3 = ShimiDanceOffline(motors_control, "Gestures/pop_3.csv")
pop3_max = 1.5
pop4 = ShimiDanceOffline(motors_control, "Gestures/pop_4.csv")
pop4_max = 2.5
maxes = [[funk1_max, funk2_max, funk3_max, funk4_max], [edm1_max, edm2_max, edm3_max, edm4_max],
              [rock1_max, rock2_max, rock3_max, rock4_max], [pop1_max, pop2_max, pop3_max, pop4_max]]
dances = [[funk1, funk2, funk3, funk4], [edm1, edm2, edm3, edm4], [rock1, rock2, rock3, rock4],
               [pop1, pop2, pop3, pop4]]


def message_decoder(message):
    if "stop" in message:
        return "stop"
    elif "start" in message:
        return "start"
    else:
        genre = message[message.find("genre") + 7: message.find("name") - 1]
        songName = message[message.find("name") + 6: -1]
        if genre == "1":
            genre = "pop"
        elif genre == "2":
            genre = "rock"
        elif genre == "3":
            genre = "EDM"
        elif genre == "4":
            genre = "funk"
        return genre + "/" + songName + "xyz"


def read_txt(file):
    sentence_list = file.read().split("\n")
    time_list = []
    for i in range(len(sentence_list)):
        curr_line = sentence_list[i]
        if curr_line == "":
            continue
        init_time_text = curr_line[:10]
        curr_line = curr_line[11:].split()
        # print(init_time_text[1:3])
        mins = float(init_time_text[1:3]) * 60
        # print(init_time_text[1:3])
        sec = float(init_time_text[4:6])
        msec = float(init_time_text[7:9]) * 0.01
        init_time = mins + sec + msec
        time_list.append(init_time)
    return time_list


def read_json(file):
    json_file = json.load(file)
    time = []
    for i in range(len(json_file)):
        time.append(json_file[i]['start'])
    return time


def print_lyrics(time_list):
    for i in range(1, len(time_list)):
        if not _play:
            break
        if i == 1:
            count = 0
            while (count < time_list[i]):
                sleep(.2)
                count += .2
                if not _play:
                    break
        else:
            count = 0
            while (count < (time_list[i] - time_list[i - 1])):
                sleep(.2)
                count += .2
                if not _play:
                    break
        conn.send("lyrics".encode())


def move_with_tempo(tempo):
    global _play
    curr_dances = 0
    count_tempo = 0
    count_segmentation = 1
    curr_dance_count = 0
    start_time = time.time()

    curr_max = 3.5
    curr_dance_number = 0
    lyrics_count = 0

    if genre == "funk":
        # curr_maxes = maxes[0]
        curr_dances = dances[0]
    if genre == "EDM":
        # curr_maxes = maxes[1]
        curr_dances = dances[1]
    if genre == "rock":
        # curr_maxes = maxes[2]
        curr_dances = dances[2]
    if genre == "pop":
        # curr_maxes = maxes[3]
        curr_dances = dances[3]

    curr_dance = curr_dances[0]
    while _play:
        curr_time = time.time() - start_time
        # if clock == 0:
        if curr_time >= beats_data[count_tempo] - 60 / (8 * tempo):
            print("curr_beats:", count_tempo)
            curr_dance.send(curr_dance_count, tempo)
            if curr_dance_count == curr_max:
                curr_dance_count = 0
            else:
                curr_dance_count += .5
            count_tempo += 1
        # if clock == 1:
        if beats_data[count_tempo] >= seg_data[count_segmentation][0]:  # - 8*(60/tempo) - 1:
            print("a new section", seg_data[count_segmentation][0])
            print(curr_dance)
            new_nuber = random.randint(0, 3)
            while new_nuber == curr_dance_number:
                new_nuber = random.randint(0, 3)
            curr_dance_number = new_nuber
            curr_dance = curr_dances[curr_dance_number]
            curr_max = 3.5
            count_segmentation += 1

        # if curr_time >= lyrics_time_list[lyrics_count] - 2 * (60 / tempo) - 1:
        #     conn.send("lyrics".encode())
        #     lyrics_count += 1

        if count_tempo == len(beats_data) - 1:
            s.send(b"done")
            _play = False
            break


# socket.AF_INET, socket.SOCK_STREAM
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("192.168.0.101", 5020))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            data = str(data)
            print(data)
            message = message_decoder(data)
            if message == "stop":
                _play = False
                print("stop playing")
                subprocess.Popen(['pkill', 'aplay'])
                motor_thread.join()
                pop1.initialize()
            elif message == "start":
                print("start playing")
                _play = True
                motor_thread = threading.Thread(target=move_with_tempo, args=(tempo_data,))
                motor_thread.start()
                subprocess.Popen(['aplay', '-D', 'plughw:CARD=Device,DEV=0', '-N', wav])
            elif "xyz" in message:
                message = message.replace("xyz", "")
                path = "music&data/"
                genre = message.split("/")[0]
                lyrics_path = "lyrics/" + message
                wav = path + message + ".wav"
                json_data = path + message + ".json"
                file = open(json_data)
                json_file = json.load(file)
                try:
                    print(lyrics_path + ".txt")
                    txt_file = open(lyrics_path + ".txt")
                    print(1)
                    lyrics_time_list = read_txt(txt_file)
                except:
                    json_lyrics_file = open(lyrics_path + ".json")
                    lyrics_time_list = read_json(json_lyrics_file)

                seg_data = json_file["segmentation"]
                tempo_data = json_file["tempo"]
                beats_data = json_file["beats"]

                print("done loading " + message)

"""one thing to fix: change _play after the whole song finished
"born this way",
cruel summer verse
good for you verse
levitating sectioning rap
light verse  
"""
