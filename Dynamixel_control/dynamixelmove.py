import random
import sys
#import dynamixel_sdk
import os
import threading
from config.dynamixel_definitions import *

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

DXL_MOVING_STATUS_THRESHOLD = 20

from dynamixel_sdk import *

class New_Move():
    def __init__(self, port_handler, packet_handler, groupSync):
        """
        Args:
            portHandler (port_handler) Port handler from dynamxiel_sdk to open/close ports for motor communication
            packetHandler (packet_handler) Packet handler to deliver packets/instructions to specific motors
            motor_list (list[]) list of motors to execute moves at the same time
            goal_list (list[]) list of goal positions for each motor in motor list
        """
        self.portHandler = port_handler
        self.packetHandler = packet_handler
        self.groupSync = groupSync
        self.thresholds = [[1929,2214], [1399, 2209], [1730, 2175], [0,4095], [2109, 2288]]
        self.motors = [DXL1_ID,DXL2_ID,DXL3_ID,DXL4_ID,DXL5_ID]
        self.lock = threading.Lock()
        self._stop_move = False
    def enable_torque(self):
        # Enable Dynamixel#1 Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL1_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
                print("Dynamixel#%d has been successfully connected" % DXL1_ID)

        # Enable Dynamixel#2 Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL2_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
                print("Dynamixel#%d has been successfully connected" % DXL2_ID)
                # Enable Dynamixel#3 Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL3_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
                print("Dynamixel#%d has been successfully connected" % DXL3_ID)
                # Enable Dynamixel#4 Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL4_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
                print("Dynamixel#%d has been successfully connected" % DXL4_ID)
                # Enable Dynamixel#5 Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL5_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
                print("Dynamixel#%d has been successfully connected" % DXL5_ID)
        print("Everything connected")
        return

    def disable_torque(self):
            # Disable Dynamixel#1 Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL1_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

            # Disable Dynamixel#2 Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL2_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            # Disable Dynamixel#3 Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL3_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

            # Disable Dynamixel#4 Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL4_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

            # Disable Dynamixel#5 Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL5_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

            print("Everything disconnected")
            return

    def move(self, goal_list, speed_list, time_limit):
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL1_ID, ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            print(dxl1_present_position)

            #denormalize goal positions -> write them into groupsync with addParam(DXLID, goal postion)
            # motorlist = []
            # index = 0
            # for goal in goal_list:
            #     if goal == 0:
            #         motorlist.append(False)
            #     else:
            #         motorlist.append(True)
            # print(motorlist)
            
            #check which motors to supply to add param of the groupSync
            goal_list = self.denormalize(goal_list)
            print(goal_list)
            self.groupSync.clearParam()
            #normalize all positions
            for i in range(5):
                #print(i)
                print(speed_list)
                if goal_list[i] == "no_move":
                    motor_id = i + 1
                    print("[ID:%03d] motor value is 0 so skipped" % motor_id)
                else:
                    param_goal_position = [DXL_LOBYTE(goal_list[i]), DXL_HIBYTE(goal_list[i])]
                    print("adding params")
                    if i == 0:
                        dxl_addparam_result = self.groupSync.addParam(DXL1_ID, param_goal_position)
                        self.set_moving_speed(1, speed_list[0])
                        print(param_goal_position)
                        print(len(param_goal_position))
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam failed" % DXL1_ID)
                            #print("[ID:%03d] groupSyncWrite addparam failed" % DXL1_ID)
                            quit()
                    elif i == 1:
                        dxl_addparam_result = self.groupSync.addParam(DXL2_ID, param_goal_position)
                        self.set_moving_speed(2, speed_list[1])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam failed" % DXL2_ID)
                            quit()
                    elif i == 2:
                        dxl_addparam_result = self.groupSync.addParam(DXL3_ID, param_goal_position)
                        print(param_goal_position)
                        self.set_moving_speed(3, speed_list[2])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam failed" % DXL3_ID)
                            quit()
                    elif i == 3:
                        dxl_addparam_result = self.groupSync.addParam(DXL4_ID, param_goal_position)
                        print(param_goal_position)
                        self.set_moving_speed(4, speed_list[3])
                        #self.get_moving_speed()
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam failed" % DXL4_ID)
                            quit()
                    elif i == 4:
                        dxl_addparam_result = self.groupSync.addParam(DXL5_ID, param_goal_position)
                        self.set_moving_speed(5, speed_list[4])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam failed" % DXL5_ID)
                            quit()
                
            print("params added, groupsync write...")
            #self.get_moving_speed()
            #self.get_goal_position()
            dxl_comm_result = self.groupSync.txPacket()
            #self.set_moving_speed(4, speed_list[3])
            #self.get_goal_position()

            #self.get_moving_speed()
            time_test = time.time()
            curr_time = time.time()
            max_time = curr_time + time_limit
            #print(self.get_moving_speed())

            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            self.groupSync.clearParam()
            print("groupsync cleared params")
           
            #self.get_moving_speed()
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL4_ID, ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            #self.get_moving_status()
            
            while curr_time < max_time:
                curr_time = time.time()
            
            return
            
    def denormalize_single_value(self, motor_id, values):
        threshold_min = self.thresholds[motor_id][0]
        threshold_max = self.thresholds[motor_id][1]
        denorm_values = int(threshold_min + (values * (threshold_max - threshold_min)))
        return denorm_values

    def denormalize(self,values):
        denorm_values = []
        for i in range(5):
            try:
                threshold_min = self.thresholds[i][0]
                threshold_max = self.thresholds[i][1]
                denorm_values.append(int(threshold_min + (values[i] * (threshold_max - threshold_min))))
            except:
                denorm_values.append(values[i])
        return denorm_values

    def get_moving_speed(self, motor_id):
        self.lock.acquire()
        speed = self.packetHandler.read2ByteTxRx(self.portHandler, motor_id, ADDR_MX_MOVING_SPEED)[0]
        print("[ID:%03d] has moving speed: %d"  % (motor_id, speed))
        self.lock.release()
        #all 0. The maximum rpm of the motor is used without controlling the speed.

    def get_goal_position(self, motor_id):
        goal_position = self.packetHandler.read2ByteTxRx(self.portHandler, motor_id, ADDR_MX_GOAL_POSITION)[0]
        print("[ID:%03d] has goal position: %d"  % (motor_id, goal_position))

    def set_moving_speed(self, motor_id, speed):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, motor_id, ADDR_MX_MOVING_SPEED, speed)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        self.get_moving_speed(motor_id)

    def set_goal_position(self, motor_id, goal_position, duration, speed):
        with self.lock:
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, motor_id, ADDR_MX_MOVING_SPEED, speed)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, motor_id, ADDR_MX_GOAL_POSITION, goal_position)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
               print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            max_time = time.time() + duration
            curr_time = time.time()
            while curr_time < max_time:
                curr_time = time.time()

    def get_firmware(self):
        print("Firmware:")
        print(self.packetHandler.read1ByteTxRx(self.portHandler, DXL1_ID, ADDR_MX_FIRMWARE))

        print(self.packetHandler.read1ByteTxRx(self.portHandler, DXL2_ID, ADDR_MX_FIRMWARE))

        print(self.packetHandler.read1ByteTxRx(self.portHandler, DXL3_ID, ADDR_MX_FIRMWARE))
 
        print(self.packetHandler.read1ByteTxRx(self.portHandler, DXL4_ID, ADDR_MX_FIRMWARE))

        print(self.packetHandler.read1ByteTxRx(self.portHandler, DXL5_ID, ADDR_MX_FIRMWARE))
        #all motors except neck_lr(2) is v30. neck_lr(2) is v29. Spinning may be caused by a firmware issue?
        return

    def get_present_load(self, motor_id):
        present_load = self.packetHandler.read2ByteTxRx(self.portHandler, motor_id, ADDR_MX_PRESENT_LOAD)[0]
        print("[ID:%03d] has present load: %d"  % (motor_id, present_load))

    def get_present_voltage(self, motor_id):
        present_voltage = self.packetHandler.read2ByteTxRx(self.portHandler, motor_id, ADDR_MX_PRESENT_VOLTAGE)[0]
        print("[ID:%03d] has present voltage: %d"  % (motor_id, present_voltage))

    def get_shutdown(self):
        print("Shutdown information")
        
        if (self.packetHandler.read1ByteTxRx(self.portHandler, DXL1_ID, ADDR_MX_SHUTDOWN)[0] == 36):
            print("no error")
        else:
            print(bin(self.packetHandler.read1ByteTxRx(self.portHandler, DXL1_ID, ADDR_MX_SHUTDOWN)[0]))

        if (self.packetHandler.read1ByteTxRx(self.portHandler, DXL2_ID, ADDR_MX_SHUTDOWN)[0] == 36):
            print("no error")
        else:
            print(bin(self.packetHandler.read1ByteTxRx(self.portHandler, DXL2_ID, ADDR_MX_SHUTDOWN)[0]))

        if (self.packetHandler.read1ByteTxRx(self.portHandler, DXL3_ID, ADDR_MX_SHUTDOWN)[0] == 36):
            print("no error")
        else:
            print(bin(self.packetHandler.read1ByteTxRx(self.portHandler, DXL3_ID, ADDR_MX_SHUTDOWN)[0]))
 
        if (self.packetHandler.read1ByteTxRx(self.portHandler, DXL4_ID, ADDR_MX_SHUTDOWN)[0] == 36):
            print("no error")
        else:
            print(bin(self.packetHandler.read1ByteTxRx(self.portHandler, DXL4_ID, ADDR_MX_SHUTDOWN)[0]))

        if (self.packetHandler.read1ByteTxRx(self.portHandler, DXL5_ID, ADDR_MX_SHUTDOWN)[0] == 36):
            print("no error")
        else:
            print(bin(self.packetHandler.read1ByteTxRx(self.portHandler, DXL5_ID, ADDR_MX_SHUTDOWN)[0]))
    def get_present_positions(self, id):
        self.lock.acquire()
        currMotor = self.motors[id]
        curr_pos = self.packetHandler.read2ByteTxRx(self.portHandler, currMotor, ADDR_MX_PRESENT_POSITION)[0]
        self.lock.release()
        return curr_pos
    def get_moving_status(self, motor_id):
        print("Moving:")
        return self.packetHandler.read1ByteTxRx(self.portHandler, motor_id, ADDR_MX_MOVING)[0]

    def initial_position(self):
        print("Resetting to initial positions:")
        #lock.acquire()
        self.goal_pos = [1, .5, 1, 0, .5]  # [2214, 1804, 2175, 0, 2198.5]
        self.move(self.goal_pos, [0,0,0,0,0], 2)
        #lock.release()
    def checks_bounds(self):
        curr_1 = self.get_present_positions(1)
        if curr_1 > 2214:
            print("[ID:%03d] is out of bounds, readjusting to nearest bound: %d"  % (DXL1_ID, 2214))
            self.set_goal_position(1, 2214)
        curr_2 = self.get_present_positions(2)
        if curr_1 < 1399:
            print("[ID:%03d] is out of bounds, readjusting to nearest bound: %d"  % (DXL2_ID, 1399))
            self.set_goal_position(2, 1399)
        elif curr_1 > 2209:
            print("[ID:%03d] is out of bounds, readjusting to nearest bound: %d"  % (DXL2_ID, 2209))
            self.set_goal_position(2, 2209)



            
        


        