import os
import random
# from shimi import *
import time
import datetime
from motion.dynamixelmove import *
import argparse
import threading
from dynamixel_sdk import *
from dynamixel_sdk import group_sync_write
from shimi_dances_offline import *
from DxlThreading import *
BAUDRATE = 1000000  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'
ADDR_MX_GOAL_POSITION = 30
LEN_MX_GOAL_POSITION = 2
def main():
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    try:
        packetHandler = PacketHandler(PROTOCOL_VERSION)
        portHandler = port_setup()
        groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION)
        test =  motorsThreading()
        test1 = New_Move(portHandler, packetHandler, groupSyncWrite)       
        dance_1 = ShimiDanceOffline(test, "Gestures/pop_1.csv")

        lock = threading.Lock()
        test.Move.checks_bounds()
        test.Move.enable_torque()
        test.Move.initial_position()
        test.Move.get_present_voltage(2)
        move = {"motor_id": 1, "goal_position":1929, "duration":.5}
        move2 = {"motor_id": 1, "goal_position":2214, "duration":.5}

        move3 = {"motor_id": 2, "goal_position":1399, "duration":1}
        move4 = {"motor_id": 2, "goal_position":2209, "duration":1}

        move5 = {"motor_id": 3, "goal_position":1730, "duration":.5}
        move6 = {"motor_id": 3, "goal_position":2175, "duration":.5}
        
        move7 = {"motor_id": 4, "goal_position":0, "duration":.5}
        move8 = {"motor_id": 4, "goal_position":4095, "duration":.5}
        
        move9 = {"motor_id": 5, "goal_position":2119, "duration":.5}
        move10 = {"motor_id": 5, "goal_position":2335, "duration":.5}

        down = False
        global movelist
        movelist = []
        print("starting movelist")
        print(movelist)
        thread1 = threading.Thread(target=motor_repeat, args=(movelist,dance_1,test1, ))
        thread1.daemon = True
        thread1.start()
        start_time = time.time()
        tempo = 120
        count = 0
        while 1:
            if time.time() - start_time > 60/tempo:
                if count == 0.5:
                    movelist.insert(0, move9)
                    movelist.insert(0, move3)
                    movelist.insert(0, move5)
                    #movelist.insert(0, move6)
                if count == 1.0:
                    movelist.insert(0,move10)
                    movelist.insert(0, move6)
                    movelist.insert(0, move4)
                print(time.time() - start_time)
                #print(movelist)
                start_time = time.time()
            #time.sleep(0.5)
                if count == 1.0:
                    count = 0
                else:
                    count += 0.5

        """
        while 1:
            if time.time() - start_time > 60/tempo:
                dance_1.send(count, tempo)
                print(time.time() - start_time)
                start_time = time.time()
            #time.sleep(0.5)
                if count == 3.5:
                    count = 0
                else:
                    count += 0.5
        """         
        """ 
        range_array = ["no_move", "no_move", "no_move", "no_move", 0]
        #test.move([0,0,0,0,0],[0,0,0,0,0],5)
        #test.move([0,0,0,1,0],[0,0,0,300,0],5)
        #test.get_present_positions(1)
        #test.move([0, "no_move", "no_move", "no_move", "no_move"], [0,0,0,1000,0], 3)
        
        speed_array = [100,100,100,100,100]
        while True:
             if range_array[0] == 0:
        
                 test.move(range_array, speed_array, 1)
                 speed_array[0] = 146
                 print("Curr speed")
                 print(packetHandler.read2ByteTxRx(portHandler, DXL4_ID, ADDR_MX_PRESENT_SPEED))
                 range_array[0] = 1
             else:
                 test.move(range_array,speed_array, 1)
                 speed_array[0] = 146
                 print("Curr speed")
                 print(packetHandler.read2ByteTxRx(portHandler, DXL4_ID, ADDR_MX_PRESENT_SPEED))
        
                 range_array[0] = 0
        """
        """
        dance_1 = ShimiDanceOffline(test, "Gestures/pop_1.csv")
        dance_1.initialize()
        count = 0
        tempo = 120
        start_time = time.time()
        while 1:
            if time.time() - start_time > 60/tempo:
                dance_1.send(count, tempo)
            #time.sleep(0.5)
                if count == 3.5:
                    count = 0
                else:
                    count += 0.5

        """
        # # usually a problem when combining instructions with neck_lr(2), any combination with 2.
        # # test.move([1, .5, 1, .9, 1])
        # # test.move([.5,1,.5,1,1])
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling tasks...")
    finally:
        test.Move.initial_position()
        test.Move.disable_torque()
        portHandler.closePort()
        print("done")
def port_setup():

    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

        # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()
    return portHandler
def motor_repeat(movelist, dance_1,test1):
    while 1:
        while len(movelist) > 0:
                #print(movelist)
                moveToDo = movelist.pop()
                print("current Motor:")
                print(moveToDo["motor_id"])
                print("Requested Position:")
                print(moveToDo["goal_position"])
                speed = dance_1.get_speed(moveToDo["motor_id"], moveToDo["goal_position"], moveToDo["duration"], 60)
                test1.set_goal_position(moveToDo["motor_id"], moveToDo["goal_position"], moveToDo["duration"], speed)
                print("set goal position")

    
if __name__ == "__main__":
    main()

