from motion.dynamixelmove import *
import threading
import math


class motorsThreading():
    def __init__(self):
        DEVICENAME = '/dev/ttyUSB0'
        PROTOCOL_VERSION = 1.0
        ADDR_MX_GOAL_POSITION = 30
        LEN_MX_GOAL_POSITION = 2
        BAUDRATE = 1000000
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        self.port_init(BAUDRATE)
        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, ADDR_MX_GOAL_POSITION,
                                             LEN_MX_GOAL_POSITION)
        self.Move = New_Move(self.portHandler, self.packetHandler, self.groupSyncWrite)

        self.dance_thread = threading.Thread(target=self.motor_repeat)

        # self.goal_pos = {"torso": [],
        #                  "neck_lr": [],
        #                  "neck_ud": [],
        #                  "phone": [],
        #                  "foot": []}
        # self.moving_speed = {"torso": [],
        #                      "neck_lr": [],
        #                      "neck_ud": [],
        #                      "phone": [],
        #                      "foot": []}
        # self.duration = {"torso": [],
        #                  "neck_lr": [],
        #                  "neck_ud": [],
        #                  "phone": [],
        #                  "foot": []}
        self.moves = []

        self.motors = [DXL1_ID, DXL2_ID, DXL3_ID, DXL4_ID, DXL5_ID]
        self._new_moves = [False, False, False, False, False]

    def port_init(self, BAUDRATE):
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        if self.portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

    # def single_motor_move(self, motor_id):
    #     curr_motor = self.motors[motor_id]
    #     goal_pos = self.goal_pos[list(self.goal_pos.keys())[motor_id]].pop(0)
    #     moving_speed = self.moving_speed[list(self.goal_pos.keys())[motor_id]].pop(0)
    #     duration = self.duration[list(self.goal_pos.keys())[motor_id]].pop(0)
    #     self.Move.set_goal_position(curr_motor, goal_pos, duration, moving_speed)

    def motor_repeat(self):
        while 1:
            while len(self.moves) > 0:
                # print(movelist)
                moveToDo = self.moves.pop()
                print("current Motor:")
                print(moveToDo["motor_id"])
                print("Requested Position:")
                print(moveToDo["goal_position"])
                speed = self.get_speed(moveToDo["motor_id"], moveToDo["goal_position"], moveToDo["duration"], 60)
                self.Move.set_goal_position(moveToDo["motor_id"], moveToDo["goal_position"], moveToDo["duration"], speed)
                print("set goal position")

    def get_speed(self, motor_id, goal_pos, duration, tempo):
        curr_pos = self.Move.get_present_positions(motor_id)
        d = abs(goal_pos - curr_pos)
        print("curr_pos: ", curr_pos)
        duration_in_sec = duration*(60/tempo)
        degrees_to_radians_ratio = math.pi/180
        degrees_to_radians = (d/duration_in_sec) * 0.088 * (degrees_to_radians_ratio)
        radians_to_rpm = (degrees_to_radians * 60)/(2 * math.pi)
        speed = int(radians_to_rpm/.114)
        print(speed)
        return speed