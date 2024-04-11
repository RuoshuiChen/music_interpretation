from shimi_dances_offline import *
import os
import random
import time
import datetime
from motion.dynamixelmove import *
import argparse
import threading
from dynamixel_sdk import *
from dynamixel_sdk import group_sync_write
from shimi_dances_real_time import *



BAUDRATE = 1000000  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyACM0'
ADDR_MX_GOAL_POSITION = 30
LEN_MX_GOAL_POSITION = 4

try:
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)
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
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION)
    test = New_Move(portHandler, packetHandler, groupSyncWrite)
    print(packetHandler.read2ByteTxRx(portHandler, DXL2_ID, ADDR_MX_MODEL_NUMBER))
    test.enable_torque()
    test.get_moving_status()
    # test.get_shutdown()
    # test.get_present_positions()
    #test.move([1, .5, 1, 0, .5], 1)
    #test.move([0, "no_move", .5, .5, .5], 1)
    # test.move([1, "no_move", 1, 0, .5], 1)
    dance_1 = ShimiDanceOffline(test, "Gestures/funk_1.csv")
    dance_1.initialize()
    count = 0
    for i in range(7):
        dance_1.send(count, 120)
        time.sleep(0.5)
    # usually a problem when combining instructions with neck_lr(2), any combination with 2.
    # test.move([1, .5, 1, .9, 1])
    # test.move([.5,1,.5,1,1])
except KeyboardInterrupt as e:
    print("Caught keyboard interrupt. Canceling tasks...")
finally:
    test.disable_torque()
    portHandler.closePort()
    print("done")