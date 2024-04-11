import socket
import threading
#from playsound import playsound
from time import sleep
# import decoder
# from decoder import decode_to_threads
# from pygame import mixer
from multiprocessing import Process
#from pydub import AudioSegment,playback
import json
import numpy as np
import math
#from dynamixel_sdk import *
import serial
import subprocess
from shimi_dances_real_time import *
import time
import random
import os

HOST = "172.20.10.4"  # Standard loopback interface address (localhost)
PORT = 5020  # Port to listen on (non-privileged ports are > 1023)

global music
global start
global seg_thread
#global music_thread
global tempo_data
global seg_data
global verticals_data
global beats_data
global _play
global _valueChange
global _event
global wav
global beats_time_dif
global tempo_from_beats
global lyrics_time_list
global genre
funk1 = ShimiDanceRealTime("Gestures/funk_1.csv")
funk1_max = 0.5
funk2 = ShimiDanceRealTime("Gestures/funk_2.csv")
funk2_max = 2.5
funk3 = ShimiDanceRealTime("Gestures/funk_3.csv")
funk3_max = 2.5
funk4 = ShimiDanceRealTime("Gestures/funk_5.csv")
funk4_max = 2.5
edm1 = ShimiDanceRealTime("Gestures/edm_1.csv")
edm1_max = 3.5
edm2 = ShimiDanceRealTime("Gestures/edm_2.csv")
edm2_max = 2.5
edm3 = ShimiDanceRealTime("Gestures/edm_3.csv")
edm3_max = 2.5
edm4 = ShimiDanceRealTime("Gestures/edm_4.csv")
edm4_max = 2.5
rock1 = ShimiDanceRealTime("Gestures/rock_1.csv")
rock1_max = 0.5
rock2 = ShimiDanceRealTime("Gestures/rock_2.csv")
rock2_max = 2.5
rock3 = ShimiDanceRealTime("Gestures/rock_3.csv")
rock3_max = 2.5
rock4 = ShimiDanceRealTime("Gestures/rock_4.csv")
rock4_max = 2.5
pop1 = ShimiDanceRealTime("Gestures/pop_1.csv")
pop1_max = 0.5
pop2 = ShimiDanceRealTime("Gestures/pop_2.csv")
pop2_max = 1.5
pop3 = ShimiDanceRealTime("Gestures/pop_3.csv")
pop3_max = 1.5
pop4 = ShimiDanceRealTime("Gestures/pop_4.csv")
pop4_max = 2.5
maxes = [[funk1_max, funk2_max, funk3_max, funk4_max], [edm1_max, edm2_max, edm3_max, edm4_max],
         [rock1_max, rock2_max, rock3_max, rock4_max], [pop1_max, pop2_max, pop3_max, pop4_max]]
dances = [[funk1, funk2, funk3, funk4], [edm1, edm2, edm3, edm4], [rock1, rock2, rock3, rock4],
          [pop1, pop2, pop3, pop4]]
# ADDR_MX_TORQUE_ENABLE = 24
# ADDR_MX_GOAL_POSITION = 30
# ADDR_MX_PRESENT_POSITION = 36
# degree_changes = [10, 20, 30, 40, 30, 40, 50, 60, 50, 60, 70, 80, 70, 80, 90, 100, 90, 100, 110, 120,
#                       110, 120, 130, 140, 130, 140, 150, 160, 150, 160, 170, 180, 170, 160, 150, 140, 150,
#                       140, 130, 120, 130, 120, 110, 100, 110, 100, 90, 80, 90, 80, 70, 60, 70, 60, 50, 40,
#                       50, 40, 30, 20, 30, 20, 10, 0]
#
# MORTOR_TIME_DELAY = 0.01 #116.62/60/36
#
# # Protocol version
# PROTOCOL_VERSION = 1.0
#
# # Default motor ID
# MOTOR_ID = 4
#
# # Set your motor properties (baudrate, motor ID, etc.)
# BAUDRATE = 1000000
# DEVICENAME = '/dev/tty.usbmodem112301'  # Change this to the appropriate serial port on your system
#
# # Initialize the Dynamixel SDK
# portHandler = PortHandler(DEVICENAME)
# packetHandler = PacketHandler(PROTOCOL_VERSION)PROTOCOL_VERSION



# def playSong(file_path):
#     playsound(file_path)


def wait(time):
    count = 0
    while count < time - .5:
        global _play
        if not _play:
            break
        sleep(.5)
        count += .5

def setup_motor():
    # Open the serial port
    if portHandler.openPort():
        print("Succeeded to open the port!")
    else:
        print("Failed to open the port!")
        return False

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to set the baudrate!")
    else:
        print("Failed to set the baudrate!")
        return False

    # Enable torque for the motor
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_TORQUE_ENABLE, 1)
    if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:
        print("Failed to enable torque!")
        print(dxl_comm_result)
        return False

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_GOAL_POSITION, 0)

    return True




def message_decoder(message):
    if "stop" in message:
        return "stop"
    elif "start" in message:
        return "start"
    else:
        genre = message[message.find("genre") + 7 : message.find("name") - 1]
        songName = message[message.find("name")+6 : -1]
        if genre == "1":
            genre = "pop"
        elif genre == "2":
            genre = "rock"
        elif genre == "3":
            genre = "EDM"
        elif genre == "4":
            genre = "funk"
        return genre+"/"+songName + "xyz"



def signal_decode(type, file):
    if type == "segmentation" or type == "onset":
        for i in range(len(file)):
            if i == 0:
                curr_time = file[i][0]
                curr_pow = file[i][1]
            else:
                curr_time = file[i][0] - file[i - 1][0]
                curr_pow = file[i][1]
            count = 0
            break_bool = False
            while count < curr_time - .5:
                global _play
                if not _play:
                    break_bool = True
                    break
                sleep(.5)
                count += .5
            if break_bool:
                break
            '''do job here'''
            #print(curr_pow)

    # elif type == "tempo":
    #     for i in range(len(file)):
    #         curr_time = file[i]
    #         if i == 0:
    #             sleep(curr_time)
    #         else:
    #             sleep(curr_time - file[i-1])
    #         '''do job here'''
    #         print(curr_time)






def move_motor(angle, sleep_time):
    # Convert degrees to Dynamixel units (0 to 4095 for MX-28)

    sleep(sleep_time)
    position = int((angle / 360) * 4095)

    # Send the goal position to the motor
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_GOAL_POSITION, position)

    print("position:", position)
    print("degree:", angle)
    if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:

        print("Failed to send goal position!")

        return False
    #sleep(MORTOR_TIME_DELAY)
    return True


def seg_movement(angle, degree_turn):
    position = int((angle / 360) * 4095)
    for i in range(math.floor(degree_turn)):
        _up = True
        if position >= 4095:
            position = 4095
            _up = False
        elif position <= 0:
            position = 0
            _up = True

        if _up:
            position += int((10 / 360) * 4095)
        else:
            position -= int((10 / 360) * 4095)

        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_GOAL_POSITION, position)





    # # Set the goal position to 4095
    # dxl_goal_position = 0
    # dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_GOAL_POSITION,
    #                                                           dxl_goal_position)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print(packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print(packetHandler.getRxPacketError(dxl_error))
    # else:
    #     print("Goal position set to 0")
    #
    # time.sleep(0.00075 * angle)
    #
    # # Set the goal position to 2048
    # dxl_goal_position = 4095
    # dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_GOAL_POSITION,
    #                                                           dxl_goal_position)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print(packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print(packetHandler.getRxPacketError(dxl_error))
    # else:
    #     print("Goal position set to 4095")
    #
    # time.sleep(3.12)
    #
    # dxl_goal_position = 0
    # dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, MOTOR_ID, ADDR_MX_GOAL_POSITION,
    #                                                           dxl_goal_position)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print(packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print(packetHandler.getRxPacketError(dxl_error))
    # else:
    #     print("Goal position set to 0")

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
        #print(init_time_text[1:3])
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
            while(count < time_list[i]):
                sleep(.2)
                count += .2
                if not _play:
                    break
        else:
            count = 0
            while (count < (time_list[i] - time_list[i-1])):
                sleep(.2)
                count += .2
                if not _play:
                    break
        conn.send("lyrics".encode())

def move_with_tempo(tempo):
    curr_dances = 0
    curr_maxes = 0
    if genre == "funk":
        curr_maxes = maxes[0]
        curr_dances = dances[0]
        # funk1 = ShimiDanceRealTime("Gestures/funk_1.csv", tempo_data + 30)
        # funk1_max = 0.5
        # funk2 = ShimiDanceRealTime("Gestures/funk_2.csv", tempo_data + 30)
        # funk2_max = 2.5
        # funk3 = ShimiDanceRealTime("Gestures/funk_3.csv", tempo_data + 30)
        # funk3_max = 2.5
        # funk4 = ShimiDanceRealTime("Gestures/funk_5.csv", tempo_data + 30)
        # funk4_max = 2.5
        # curr_dances = [funk1, funk2, funk3, funk4]
        # curr_maxes = [funk1_max, funk2_max, funk3_max, funk4_max]

    if genre == "EDM":
        curr_maxes = maxes[1]
        curr_dances = dances[1]
        # edm1 = ShimiDanceRealTime("Gestures/edm_1.csv", tempo_data + 30)
        # edm1_max = 3.5
        # edm2 = ShimiDanceRealTime("Gestures/edm_2.csv", tempo_data + 30)
        # edm2_max = 2.5
        # edm3 = ShimiDanceRealTime("Gestures/edm_3.csv", tempo_data + 30)
        # edm3_max = 2.5
        # edm4 = ShimiDanceRealTime("Gestures/edm_4.csv", tempo_data + 30)
        # edm4_max = 2.5
        # curr_dances = [edm1, edm2, edm3, edm4]
        # curr_maxes = [edm1_max, edm2_max, edm3_max, edm4_max]
    if genre == "rock":
        curr_maxes = maxes[2]
        curr_dances = dances[2]
        # rock1 = ShimiDanceRealTime("Gestures/rock_1.csv", tempo_data + 30)
        # rock1_max = 0.5
        # rock2 = ShimiDanceRealTime("Gestures/rock_2.csv", tempo_data + 30)
        # rock2_max = 2.5
        # rock3 = ShimiDanceRealTime("Gestures/rock_3.csv", tempo_data + 30)
        # rock3_max = 2.5
        # rock4 = ShimiDanceRealTime("Gestures/rock_4.csv", tempo_data + 30)
        # rock4_max = 2.5
        # curr_dances = [rock1, rock2, rock3, rock4]
        # curr_maxes = [rock1_max, rock2_max, rock3_max, rock4_max]
    if genre == "pop":
        curr_maxes = maxes[3]
        curr_dances = dances[3]
        # pop1 = ShimiDanceRealTime("Gestures/pop_1.csv", tempo_data + 30)
        # pop1_max = 0.5
        # pop2 = ShimiDanceRealTime("Gestures/pop_2.csv", tempo_data + 30)
        # pop2_max = 1.5
        # pop3 = ShimiDanceRealTime("Gestures/pop_3.csv", tempo_data + 30)
        # pop3_max = 1.5
        # pop4 = ShimiDanceRealTime("Gestures/pop_4.csv", tempo_data + 30)
        # pop4_max = 2.5
        # curr_dances = [pop1, pop2, pop3, pop4]
        # curr_maxes = [pop1_max, pop2_max, pop3_max, pop4_max]
    count_tempo = 0
    count_motor = 0
    count_segmentation = 1
    curr_dance = 1
    count_lyrics = 1
    curr_dance_count = 0
    start_time = time.time()
    #clock = 0
    curr_dance = curr_dances[0]
    curr_max = 3.5
    curr_dance_number = 0
    lyrics_count = 0
    while _play:
        curr_time = time.time() - start_time
        #if clock == 0:
        if curr_time >= beats_data[count_tempo]-60/(8*tempo):
            print("curr_beats:", count_tempo)
            curr_dance.send(curr_dance_count, tempo)
            if curr_dance_count == curr_max:
                curr_dance_count = 0
            else:
                curr_dance_count += .5
            count_tempo += 1
        #if clock == 1:
        if beats_data[count_tempo] >= seg_data[count_segmentation][0]:# - 8*(60/tempo) - 1:
            print("a new section", seg_data[count_segmentation][0])
            print(curr_dance)
            new_nuber = random.randint(0,3)
            while new_nuber == curr_dance_number:
                new_nuber = random.randint(0, 3)
            curr_dance_number = new_nuber
            curr_dance = curr_dances[curr_dance_number]
            curr_max = 3.5
            count_segmentation += 1
        if curr_time >= lyrics_time_list[lyrics_count] - 2*(60/tempo) - 1:
            conn.send("lyrics".encode())
            lyrics_count+=1

        # if curr_time >= lyrics_time_list[count_lyrics] - 0.1:
        #     conn.send("lyrics".encode())
        #     print(lyrics_time_list[count_lyrics])
        #     count_lyrics += 1




command_queue = []
#socket.AF_INET, socket.SOCK_STREAM
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("192.168.0.101", 5020))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        _play = False
        global music_thread
        pop1.start_playing()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            data = str(data)
            print(data)
            message = message_decoder(data)
            #start_dance = ShimiDanceRealTime("Gestures/funk_2.csv")
            #start_dance.start_playing()
            if message == "stop":
                # if command_queue[-1] == "start":
                _play = False
                print("stop playing")
                #music_thread.stop()
                subprocess.Popen(['pkill', 'aplay'])
                #seg_thread.join()
                motor_thread.join()
                #lyrics_thread.join()
                # reset_dacne = ShimiDanceRealTime("Gestures/funk_2.csv")
                pop1.initialize()
            elif message == "start":
                #if not len(command_queue) == 0:
                print("start playing")
                #seg_thread = threading.Thread(target=signal_decode, args=("segmentation",seg_data))
                #music_thread = playback._play_with_simpleaudio(music)
                _play = True
                motor_thread = threading.Thread(target=move_with_tempo, args=(tempo_data,))
                motor_thread.start()
                subprocess.Popen(['aplay', '-D', 'plughw:CARD=Device,DEV=0', '-N', wav])
                #lyrics_thread = threading.Thread(target=print_lyrics, args=(lyrics_time_list,))
                #lyrics_thread.start()
                #seg_thread.start()
                #music_thread.start()
            elif "xyz" in message:
                message = message.replace("xyz","")
                path = "music&data/"
                genre = message.split("/")[0]
                lyrics_path = "lyrics/" + message
                wav = path + message + ".wav"
                json_data = path + message + ".json"
                #music = AudioSegment.from_file(wav)
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
                #txt_file = open(lyrics_path + ".txt")
                #lyrics_time_list = read_txt(txt_file)
                #print(json_file)
                seg_data = json_file["segmentation"]
                tempo_data = json_file["tempo"]
                print(tempo_data)
                beats_data = json_file["beats"]


                # beats_time_dif = np.array(beats_data[1:]) - np.array(beats_data[: len(beats_data) - 1])
                # fake_array = np.full(beats_time_dif.shape, .0075)
                # beats_time_dif = beats_time_dif - fake_array
                # tempo_from_beats = np.average(beats_time_dif)
                # beats_time_dif = beats_time_dif.tolist()
                # beats_time_dif.insert(0,beats_data[0] - 0.0075)
                # #print(beats_time_dif)
                #
                # verticals_data = json_file["verticals"]
                # _valueChange = True
                # #print(seg_thread)
                print("done loading " + message)
                #print(seg_data)
                # print("tempo:", tempo_data)
            command_queue.append(message)
            # if _play and not music_thread.is_alive():
            #     music_thread.join()
            #     _play = False
            # if _play and not seg_thread.is_alive():
            #     seg_thread.join()
            #     _play = False




"""one thing to fix: change _play after the whole song finished
"born this way",
cruel summer verse
good for you verse
levitating sectioning rap
light verse  
"""






