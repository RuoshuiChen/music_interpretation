import csv
import operator
import time
import math
from DxlThreading import *

class ShimiDanceOffline:
    def __init__(self, sync_move, csv_file_name, haptics=False, haptics_csv='Haptics/haptics_2.csv'):
        self.torso_moves = []
        self.neck_lr_moves = []
        self.neck_ud_moves = []
        self.foot_moves = []
        self.phone_moves = []
        self.parse(csv_file_name, haptics)
        self.goal_pos = []
        self.move_speed = []
        self.sync_move = sync_move
        print("torso_move",  self.torso_moves)

    def initialize(self):
        """move all motors to starting position"""
        self.goal_pos = [1, .5, 1, 0, .5]  # [2214, 1804, 2175, 0, 2198.5]
        self.sync_move.Move.move(self.goal_pos, [0,0,0,0,0], 2)
        self.goal_pos = []


    def normalize(self, value, id):
        curr_threshold = self.sync_move.Move.threshold[id]
        return (curr_threshold[1] - curr_threshold[0]) / value

    def parse(self, csv_file_name, haptics):
        print("start parsing")
        start = time.time()
        self.torso_moves = []
        self.neck_lr_moves = []
        self.neck_ud_moves = []
        self.foot_moves = []
        self.phone_moves = []
        with open(csv_file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            for line in csv_reader:
                move = []
                move.append(float(line[0]))
                # move.append(60 / tempo * float(line[1]))
                move.append(float(line[1]))
                move.append(float(line[2]))
                # move.append(60 / tempo * float(line[3]))
                move.append(float(line[3]))
                if move[0] == 0:
                    print("Rest move removed")
                if move[0] == 1:
                    self.torso_moves.append(move)
                if move[0] == 2:
                    self.neck_lr_moves.append(move)
                if move[0] == 3:
                    self.neck_ud_moves.append(move)
                if move[0] == 4 and haptics:
                    self.phone_moves.append(move)
                if move[0] == 5:
                    self.foot_moves.append(move)
                if move[0] != 0 and move[0] != 1 and move[0] != 2 and move[0] != 3 and move[0] != 4 and move[0] != 5:
                    print(move, "removed beause", move[0], "is not a valid motor ID")
        self.torso_moves = sorted(self.torso_moves, key=operator.itemgetter(1))
        self.neck_lr_moves = sorted(self.neck_lr_moves, key=operator.itemgetter(1))
        self.neck_ud_moves = sorted(self.neck_ud_moves, key=operator.itemgetter(1))
        self.foot_moves = sorted(self.foot_moves, key=operator.itemgetter(1))
        self.phone_moves = sorted(self.phone_moves, key=operator.itemgetter(1))
        # remove overlapping intervals
        # self.torso_moves, removed_torso_moves = self.remove_overlapping_intervals(self.torso_moves)
        # self.neck_lr_moves, removed_neck_lr_moves = self.remove_overlapping_intervals(self.neck_lr_moves)
        # self.neck_ud_moves, removed_neck_ud_moves = self.remove_overlapping_intervals(self.neck_ud_moves)
        # self.foot_moves, removed_foot_moves = self.remove_overlapping_intervals(self.foot_moves)
        # self.phone_moves, removed_phone_moves = self.remove_overlapping_intervals(self.phone_moves)
        # max
        moves_max = 0
        if len(self.torso_moves) != 0:
            if self.torso_moves[-1][1] + self.torso_moves[-1][3] > moves_max:
                moves_max = self.torso_moves[-1][1] + self.torso_moves[-1][3]
        if len(self.neck_lr_moves) != 0:
            if self.neck_lr_moves[-1][1] + self.neck_lr_moves[-1][3] > moves_max:
                moves_max = self.neck_lr_moves[-1][1] + self.neck_lr_moves[-1][3]
        if len(self.neck_ud_moves) != 0:
            if self.neck_ud_moves[-1][1] + self.neck_ud_moves[-1][3] > moves_max:
                moves_max = self.neck_ud_moves[-1][1] + self.neck_ud_moves[-1][3]
        if len(self.foot_moves) != 0:
            if self.foot_moves[-1][1] + self.foot_moves[-1][3] > moves_max:
                moves_max = self.foot_moves[-1][1] + self.foot_moves[-1][3]
        if len(self.phone_moves) != 0:
            if self.phone_moves[-1][1] + self.phone_moves[-1][3] > moves_max:
                moves_max = self.phone_moves[-1][1] + self.phone_moves[-1][3]

        # add beginning stay moves
        self.torso_moves = self.add_beginning_stays(self.torso_moves, 1, 1, moves_max)
        self.neck_lr_moves = self.add_beginning_stays(self.neck_lr_moves, 2, 0.5, moves_max)
        self.neck_ud_moves = self.add_beginning_stays(self.neck_ud_moves, 3, 1, moves_max)
        self.foot_moves = self.add_beginning_stays(self.foot_moves, 5, 0, moves_max)
        self.phone_moves = self.add_beginning_stays(self.phone_moves, 4, 0.5, moves_max)
        # add middle stay moves
        self.torso_moves = self.add_middle_stays(self.torso_moves)
        self.neck_lr_moves = self.add_middle_stays(self.neck_lr_moves)
        self.neck_ud_moves = self.add_middle_stays(self.neck_ud_moves)
        self.foot_moves = self.add_middle_stays(self.foot_moves)
        self.phone_moves = self.add_middle_stays(self.phone_moves)
        # add end stay moves
        self.torso_moves = self.add_end_stays(self.torso_moves, moves_max)
        self.neck_lr_moves = self.add_end_stays(self.neck_lr_moves, moves_max)
        self.neck_ud_moves = self.add_end_stays(self.neck_ud_moves, moves_max)
        self.foot_moves = self.add_end_stays(self.foot_moves, moves_max)
        self.phone_moves = self.add_end_stays(self.phone_moves, moves_max)
        # set limits
        for move in self.torso_moves:
            if move[2] < 0:
                move[2] = 0
            if move[2] > 1:
                move[2] = 1
            # if move[2] < 0.85:
            #     move[2] = 0.85
        for move in self.neck_lr_moves:
            if move[2] < 0:
                move[2] = 0
            if move[2] > 1:
                move[2] = 1
        for move in self.neck_ud_moves:
            if move[2] < 0:
                move[2] = 0
            if move[2] > 1:
                move[2] = 1
        for move in self.foot_moves:
            if move[2] < 0:
                move[2] = 0
            if move[2] > 1:
                move[2] = 1
        for move in self.phone_moves:
            if move[2] < 0:
                move[2] = 0
            if move[2] > 1:
                move[2] = 1
        # update beats
        for move in self.torso_moves:
            move[3] = move[3] - 0.125
        for move in self.neck_lr_moves:
            move[3] = move[3] - 0.125
        for move in self.neck_ud_moves:
            move[3] = move[3] - 0.125
        for move in self.foot_moves:
            move[3] = move[3] - 0.125
        for move in self.phone_moves:
            move[3] = move[3] - 0.125
        # change beats to seconds

        #print("torso moves:", self.torso_moves)
        #print("removed torso moves:", removed_torso_moves)
        #print("neck_lr moves:", self.neck_lr_moves)
        #print("removed neck_lr moves:", removed_neck_lr_moves)
        #print("neck_ud moves:", self.neck_ud_moves)
        #print("removed neck_ud moves:", removed_neck_ud_moves)
        #print("foot moves:", self.foot_moves)
        #print("removed foot moves:", removed_foot_moves)
        #print("phone moves:", self.phone_moves)
        #print("removed phone moves:", removed_phone_moves)
        print("parse finished")
        print(time.time() - start)
        

    def add_beginning_stays(self, moves, motor, start, moves_max):
        moves_copy = moves.copy()
        if len(moves_copy) == 0:
            moves_copy.append([motor, 0.0, start, moves_max])
            return moves_copy
        first = moves_copy[0]
        if first[1] != 0:
            moves_copy.insert(0, [motor, 0.0, start, first[1]])
            return moves_copy
        return moves_copy

    def add_middle_stays(self, moves):
        additional = []
        for i in range(len(moves) - 1):
            if moves[i][1] + moves[i][3] != moves[i + 1][1]:
                additional.append([moves[i][0], moves[i][1] + moves[i][3], moves[i][2],
                                   moves[i + 1][1] - (moves[i][1] + moves[i][3])])
        added_moves = moves + additional
        added_moves = sorted(added_moves, key=operator.itemgetter(1))
        return added_moves

    def add_end_stays(self, moves, moves_max):
        moves_copy = moves.copy()
        if moves_copy[-1][1] + moves_copy[-1][3] != moves_max:
            moves_copy.append(
                [moves[0][0], moves[-1][1] + moves[-1][3], moves[-1][2], moves_max - (moves[-1][1] + moves[-1][3])])
        return moves_copy

    def remove_overlapping_intervals(self, moves):
        keep = []
        removed = []
        for move in moves:
            remove = True
            if len(keep) == 0:
                keep.append(move)
                remove = False
            if self.no_overlap(move, keep):
                keep.append(move)
                remove = False
            if remove:
                removed.append(move)
        return keep, removed

    def no_overlap(self, move, keep):
        for movement in keep:
            if move[1] < movement[1] + movement[3]:
                return False
        return True

    def send(self, beat, tempo):
        # """stop all motors from moving"""
        # # self.sync_move.stop_move()
        # print("beat:", beat)
        # print(self.torso_moves)
        # print(self.neck_lr_moves)
        # print(self.neck_ud_moves)
        # print(self.phone_moves)
        # print(self.foot_moves)
        # print(beat)
        # max_durations = []
        """adding torso's goal_pos to the goal_pos list"""
        for move in self.torso_moves:
            if move[1] == beat:
                goal_pos = self.sync_move.Move.denormalize_single_value(0,move[2])
                duration = move[3]
                move = {"motor_id": 1, "goal_position": goal_pos, "duration": duration}
                self.sync_move.moves.insert(0,move)
                break

        """adding neck_lr's goal_pos to the goal_pos list"""
        for move in self.neck_lr_moves:
            if move[1] == beat:
                goal_pos = self.sync_move.Move.denormalize_single_value(0, move[2])
                duration = move[3]
                move = {"motor_id": 2, "goal_position": goal_pos, "duration": duration}
                self.sync_move.moves.insert(0,move)
                break

        """adding neck_ud's goal_pos to the goal_pos list"""
        for move in self.neck_ud_moves:
            if move[1] == beat:
                goal_pos = self.sync_move.Move.denormalize_single_value(0, move[2])
                duration = move[3]
                move = {"motor_id": 3, "goal_position": goal_pos, "duration": duration}
                self.sync_move.moves.insert(0,move)
                break

        """adding phone's goal_pos to the goal_pos list"""
        for move in self.phone_moves:
            if move[1] == beat:
                goal_pos = self.sync_move.Move.denormalize_single_value(0, move[2])
                duration = move[3]
                move = {"motor_id": 4, "goal_position": goal_pos, "duration": duration}
                self.sync_move.moves.insert(0,move)
                break


        """adding foot's goal_pos to the goal_pos list"""
        print("beat: ", beat)
        for move in self.foot_moves:
            if move[1] == beat:
                goal_pos = self.sync_move.Move.denormalize_single_value(0, move[2])
                duration = move[3]
                move = {"motor_id": 5, "goal_position": goal_pos, "duration": duration}
                self.sync_move.moves.insert(0, move)
                break


    def convert_to_array_indexing(self):
        if len(self.torso_moves) != 0:
            empty_lists = [[] for _ in range(int(self.torso_moves[-1][1] * 4) + 1)]
            for i in range(len(self.torso_moves)):
                empty_lists[int(self.torso_moves[i][1] * 4)] = self.torso_moves[i]
            self.torso_moves = empty_lists

        if len(self.neck_lr_moves) != 0:
            empty_lists = [[] for _ in range(int(self.neck_lr_moves[-1][1] * 4) + 1)]
            for i in range(len(self.neck_lr_moves)):
                empty_lists[int(self.neck_lr_moves[i][1] * 4)] = self.neck_lr_moves[i]
            self.neck_lr_moves = empty_lists

        if len(self.neck_ud_moves) != 0:
            empty_lists = [[] for _ in range(int(self.neck_ud_moves[-1][1] * 4) + 1)]
            for i in range(len(self.neck_ud_moves)):
                empty_lists[int(self.neck_ud_moves[i][1] * 4)] = self.neck_ud_moves[i]
            self.neck_ud_moves = empty_lists

        if len(self.foot_moves) != 0:
            empty_lists = [[] for _ in range(int(self.foot_moves[-1][1] * 4) + 1)]
            for i in range(len(self.foot_moves)):
                empty_lists[int(self.foot_moves[i][1] * 4)] = self.foot_moves[i]
            self.foot_moves = empty_lists

    def add_initialization(self, moves, motor, start):
        moves_copy = moves.copy()
        if len(moves_copy) == 0:
            moves_copy.append([motor, 0, start, 0.25])
            return moves_copy
        first = moves_copy[0]
        if first[1] != 0:
            moves_copy.insert(0, [motor, 0, start, 0.25])
            return moves_copy
        return moves_copy

    """
    def get_speed(self, motor_id, goal_pos, duration, tempo):
        curr_pos = self.sync_move.get_present_positions(motor_id)
        print("currrent_position:", curr_pos)
        d = abs(goal_pos - curr_pos)
        duration_in_sec = duration*(tempo/60)
        print("motor id:", motor_id)
        print(int((((d/duration_in_sec) * 0.088) / 360 / (.114/60))/2))
        return int((((d/duration_in_sec) * 0.088) / 360 / (.114/60))/2)
    """
    """
    def get_speed(self, motor_id, goal_pos, duration, tempo):
        curr_pos = self.sync_move.get_present_positions(motor_id)
        print("currrent_position:", curr_pos)
        d = abs(goal_pos - curr_pos)
        duration_in_sec = duration*(60/tempo)
        speed = int((0.143159*(d/duration_in_sec) - 5.36535)/2)
        if speed < 10:
            speed = 10
        if speed > 100:
            speed = 100
        print("current speed: ", speed)
        return speed
    """
    def get_speed(self, motor_id, goal_pos, duration, tempo):
        curr_pos = self.sync_move.Move.get_present_positions(motor_id)
        d = abs(goal_pos - curr_pos)
        print("curr_pos: ", curr_pos)
        duration_in_sec = duration*(60/tempo)
        degrees_to_radians_ratio = math.pi/180
        degrees_to_radians =  (d/duration_in_sec) * 0.088 * (degrees_to_radians_ratio)
        radians_to_rpm = (degrees_to_radians * 60)/(2 * math.pi)
        speed = int(radians_to_rpm/.114)
        print(speed)
        return speed
    





