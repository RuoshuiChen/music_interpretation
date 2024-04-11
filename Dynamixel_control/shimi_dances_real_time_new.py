import os
import sys
import random
from shimi import *
import time
import datetime
from motion.move import Move
import argparse
import threading
import csv
import operator

class ShimiDanceRealTime:
	def __init__(self, csv_file_name, haptics=True, haptics_csv='Haptics/haptics_2.csv'):
		self.shimi = Shimi()
		# self.tempo = tempo

		self.neck_ud = Move(self.shimi, self.shimi.neck_ud, 1, 0.875)
		self.neck_ud.stop_move()
		self.neck_ud.start()
		self.neck_ud.join()

		self.neck_lr = Move(self.shimi, self.shimi.neck_lr, 0.5, 0.875)
		self.neck_lr.stop_move()
		self.neck_lr.start()
		self.neck_lr.join()

		self.torso = Move(self.shimi, self.shimi.torso, 1, 0.875)
		self.torso.stop_move()
		self.torso.start()
		self.torso.join()

		self.foot = Move(self.shimi, self.shimi.foot, 0, 0.875)
		self.foot.stop_move()
		self.foot.start()
		self.foot.join()

		self.phone = Move(self.shimi, self.shimi.phone, 0.5, 0.875)
		self.phone.stop_move()
		self.phone.start()
		self.phone.join()

		self.torso_moves = []
		self.neck_lr_moves = []
		self.neck_ud_moves = []
		self.foot_moves = []
		self.phone_moves = []
		self.parse(csv_file_name, haptics)
		#if haptics:
			#self.parse_haptics(haptics_csv, tempo)
		# self.parse_song(csv_file_name, tempo)
		self.torso.start()
		self.neck_lr.start()
		self.neck_ud.start()
		self.foot.start()
		self.phone.start()
		#self.convert_to_array_indexing()
		#print(self.torso_moves)
		#print(self.neck_lr_moves)
		#print(self.neck_ud_moves)
		#print(self.foot_moves)
		#print(self.phone_moves)
		#time.sleep(1)

	# def set_tempo(self, tempo):
		# self.tempo = tempo

	def phonee(self, position):
		"""
		phone = Move(self.shimi, self.shimi.phone, position, 1)
		phone.start()
		phone.join()
		"""
		"""
		self.phone.stop_move()
		self.phone.join()
		self.phone.add_move(position, 1, vel_algo="constant")
		self.phone.start()
		"""
		"""
		self.torso.stop_move()
		self.torso.join()
		self.torso.add_move(position, 1, vel_algo="constant")
		self.torso.start()
		self.neck_ud.stop_move()
		self.neck_ud.join()
		self.neck_ud.add_move(position, 1, vel_algo="constant")
		self.neck_ud.start()
		"""
		self.neck_lr.stop_move()
		self.neck_lr.join()
		self.neck_lr.add_move(position, 1, vel_algo="constant")
		self.neck_lr.start()
		"""
		self.neck_ud.stop_move()
		self.neck_ud.join()
		self.neck_ud.add_move(position, 1, vel_algo="constant")
		self.neck_ud.start()
		"""

	def initialize(self):
		self.torso.stop_move()
		self.torso.join()
		self.torso.add_move(1, 0.875, vel_algo="constant")
		self.torso.start()

		self.neck_lr.stop_move()
		self.neck_lr.join()
		self.neck_lr.add_move(0.5, 0.875, vel_algo="constant")
		self.neck_lr.start()

		self.neck_ud.stop_move()
		self.neck_ud.join()
		self.neck_ud.add_move(1, 0.875, vel_algo="constant")
		self.neck_ud.start()

		self.foot.stop_move()
		self.foot.join()
		self.foot.add_move(0, 0.875, vel_algo="constant")
		self.foot.start()

		self.phone.stop_move()
		self.phone.join()
		self.phone.add_move(0.5, 0.875, vel_algo="constant")
		self.phone.start()

	"""
	def parse_song(self, song_csv, tempo):
		self.torso_moves = []
		self.neck_lr_moves = []
		self.neck_ud_moves = []
		self.foot_moves = []
		with open(song_csv, 'r') as csv_song:
			csv_reader = csv.reader(csv_song)

			for line in csv_reader:
				gesture = "Gestures/" + line[0] + ".csv"
				beat = float(line[1])
				with open(gesture, 'r') as csv_gesture:
					csv_reader_gesture = csv.reader(csv_gesture)

					for line_2 in csv_reader_gesture:
						move = []
						move.append(float(line_2[0]))
						move.append(float(line_2[1]) + beat)
						move.append(float(line_2[2]))
						move.append(float(line_2[3]))
						if move[0] == 1:
							self.torso_moves.append(move)
						if move[0] == 2:
							self.neck_lr_moves.append(move)
						if move[0] == 3:
							self.neck_ud_moves.append(move)
						if move[0] == 5:
							self.foot_moves.append(move)
						if move[0] != 1 and move[0] != 2 and move[0] != 3 and move[0] != 5:
							print(move, "removed beause", move[0], "is not a valid motor ID")
		self.torso_moves = sorted(self.torso_moves, key=operator.itemgetter(1))
		self.neck_lr_moves = sorted(self.neck_lr_moves, key=operator.itemgetter(1))
		self.neck_ud_moves = sorted(self.neck_ud_moves, key=operator.itemgetter(1))
		self.foot_moves = sorted(self.foot_moves, key=operator.itemgetter(1))
		# remove overlapping intervals
		self.torso_moves, removed_torso_moves = self.remove_overlapping_intervals(self.torso_moves)
		self.neck_lr_moves, removed_neck_lr_moves = self.remove_overlapping_intervals(self.neck_lr_moves)
		self.neck_ud_moves, removed_neck_ud_moves = self.remove_overlapping_intervals(self.neck_ud_moves)
		self.foot_moves, removed_foot_moves = self.remove_overlapping_intervals(self.foot_moves)
		# add initialization
		# self.torso_moves = self.add_initialization(self.torso_moves, 1, 1)
		# self.neck_lr_moves = self.add_initialization(self.neck_lr_moves, 2, 0.5)
		# self.neck_ud_moves = self.add_initialization(self.neck_ud_moves, 3, 1)
		# self.foot_moves = self.add_initialization(self.foot_moves, 5, 0)
		for move in self.torso_moves:
			move[3] = 60 / tempo * move[3]
		for move in self.neck_lr_moves:
			move[3] = 60 / tempo * move[3]
		for move in self.neck_ud_moves:
			move[3] = 60 / tempo * move[3]
		for move in self.foot_moves:
			move[3] = 60 / tempo * move[3]
		print("torso moves:", self.torso_moves)
		print("removed torso moves:", removed_torso_moves)
		print("neck_lr moves:", self.neck_lr_moves)
		print("removed neck_lr moves:", removed_neck_lr_moves)
		print("neck_ud moves:", self.neck_ud_moves)
		print("removed neck_ud moves:", removed_neck_ud_moves)
		print("foot moves:", self.foot_moves)
		print("removed foot moves:", removed_foot_moves)
		"""

	def parse(self, csv_file_name, haptics):
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
		self.torso_moves, removed_torso_moves = self.remove_overlapping_intervals(self.torso_moves)
		self.neck_lr_moves, removed_neck_lr_moves = self.remove_overlapping_intervals(self.neck_lr_moves)
		self.neck_ud_moves, removed_neck_ud_moves = self.remove_overlapping_intervals(self.neck_ud_moves)
		self.foot_moves, removed_foot_moves = self.remove_overlapping_intervals(self.foot_moves)
		self.phone_moves, removed_phone_moves = self.remove_overlapping_intervals(self.phone_moves)
		# max
		max = 0
		if len(self.torso_moves) != 0:
			if self.torso_moves[-1][1] + self.torso_moves[-1][3] > max:
				max = self.torso_moves[-1][1] + self.torso_moves[-1][3]
		if len(self.neck_lr_moves) != 0:
			if self.neck_lr_moves[-1][1] + self.neck_lr_moves[-1][3] > max:
				max = self.neck_lr_moves[-1][1] + self.neck_lr_moves[-1][3]
		if len(self.neck_ud_moves) != 0:
			if self.neck_ud_moves[-1][1] + self.neck_ud_moves[-1][3] > max:
				max = self.neck_ud_moves[-1][1] + self.neck_ud_moves[-1][3]
		if len(self.foot_moves) != 0:
			if self.foot_moves[-1][1] + self.foot_moves[-1][3] > max:
				max = self.foot_moves[-1][1] + self.foot_moves[-1][3]
		if len(self.phone_moves) != 0:
			if self.phone_moves[-1][1] + self.phone_moves[-1][3] > max:
				max = self.phone_moves[-1][1] + self.phone_moves[-1][3]
		"""
		# add initialization
		self.torso_moves = self.add_initialization(self.torso_moves, 1, 1)
		self.neck_lr_moves = self.add_initialization(self.neck_lr_moves, 2, 0.5)
		self.neck_ud_moves = self.add_initialization(self.neck_ud_moves, 3, 1)
		self.foot_moves = self.add_initialization(self.foot_moves, 5, 0)
		"""
		# add beginning stay moves
		self.torso_moves = self.add_beginning_stays(self.torso_moves, 1, 1, max)
		self.neck_lr_moves = self.add_beginning_stays(self.neck_lr_moves, 2, 0.5, max)
		self.neck_ud_moves = self.add_beginning_stays(self.neck_ud_moves, 3, 1, max)
		self.foot_moves = self.add_beginning_stays(self.foot_moves, 5, 0, max)
		self.phone_moves = self.add_beginning_stays(self.phone_moves, 4, 0.5, max)
		# add middle stay moves
		self.torso_moves = self.add_middle_stays(self.torso_moves)
		self.neck_lr_moves = self.add_middle_stays(self.neck_lr_moves)
		self.neck_ud_moves = self.add_middle_stays(self.neck_ud_moves)
		self.foot_moves = self.add_middle_stays(self.foot_moves)
		self.phone_moves = self.add_middle_stays(self.phone_moves)
		# add end stay moves
		self.torso_moves = self.add_end_stays(self.torso_moves, max)
		self.neck_lr_moves = self.add_end_stays(self.neck_lr_moves, max)
		self.neck_ud_moves = self.add_end_stays(self.neck_ud_moves, max)
		self.foot_moves = self.add_end_stays(self.foot_moves, max)
		self.phone_moves = self.add_end_stays(self.phone_moves, max)
		# set limits
		for move in self.torso_moves:
			if move[2] < 0:
				move[2] = 0
			if move[2] > 1:
				move[2] = 1
			if move[2] < 0.85:
				move[2] = 0.85
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

		print("torso moves:", self.torso_moves)
		print("removed torso moves:", removed_torso_moves)
		print("neck_lr moves:", self.neck_lr_moves)
		print("removed neck_lr moves:", removed_neck_lr_moves)
		print("neck_ud moves:", self.neck_ud_moves)
		print("removed neck_ud moves:", removed_neck_ud_moves)
		print("foot moves:", self.foot_moves)
		print("removed foot moves:", removed_foot_moves)
		print("phone moves:", self.phone_moves)
		print("removed phone moves:", removed_phone_moves)
	# def set_tempo(self, tempo):
	# 	for move in self.torso_moves:
	# 		move[3] = 60 / tempo * move[3]
	# 	for move in self.neck_lr_moves:
	# 		move[3] = 60 / tempo * move[3]
	# 	for move in self.neck_ud_moves:
	# 		move[3] = 60 / tempo * move[3]
	# 	for move in self.foot_moves:
	# 		move[3] = 60 / tempo * move[3]
	# 	for move in self.phone_moves:
	# 		move[3] = 60 / tempo * move[3]
		# update phone motor positions
		# if tempo > 60:
		# 	for move in self.phone_moves:
		# 		if move[2] == 0.4:
		# 			move[2] = 0.3
		# 		elif move[2] == 0.3:
		# 			move[2] = 0.1
		# 		elif move[2] == 0.2:
		# 			move[2] = -0.1
		# 		elif move[2] == 0.1:
		# 			move[2] = -0.3
	"""
	def parse_haptics(self, csv_file_name, tempo):
		self.phone_moves = []
		with open(csv_file_name, 'r') as csv_file:
			csv_reader = csv.reader(csv_file)

			for line in csv_reader:
				move = []
				move.append(float(line[0]))
				move.append(float(line[1]))
				move.append(float(line[2]))
				move.append(float(line[3]))
				if move[0] == 0:
					print("Rest move removed")
				if move[0] == 4:
					self.phone_moves.append(move)
				if move[0] != 4:
					print(move, "removed beause", move[0], "is not a valid haptics motor ID")
		self.phone_moves = sorted(self.phone_moves, key=operator.itemgetter(1))
		# remove overlapping intervals
		self.phone_moves, removed_phone_moves = self.remove_overlapping_intervals(self.phone_moves)
		# max
		max = 0
		if len(self.phone_moves) != 0:
			if self.phone_moves[-1][1] + self.phone_moves[-1][3] > max:
				max = self.phone_moves[-1][1] + self.phone_moves[-1][3]
		# add beginning stay moves
		self.phone_moves = self.add_beginning_stays(self.phone_moves, 4, -1, max)
		# add middle stay moves
		self.phone_moves = self.add_middle_stays(self.phone_moves)
		# add end stay moves
		self.phone_moves = self.add_end_stays(self.phone_moves, max)
		for move in self.phone_moves:
			move[3] = 60 / tempo * move[3]
		print("phone moves:", self.phone_moves)
		print("removed phone moves:", removed_phone_moves)
	"""

	def add_beginning_stays(self, moves, motor, start, max):
		moves_copy = moves.copy()
		if len(moves_copy) == 0:
			moves_copy.append([motor, 0.0, start, max])
			return moves_copy
		first = moves_copy[0]
		if first[1] != 0:
			moves_copy.insert(0, [motor, 0.0, start, first[1]])
			return moves_copy
		return moves_copy

	def add_middle_stays(self, moves):
		additional = []
		for i in range(len(moves) - 1):
			if moves[i][1] + moves[i][3] != moves[i+1][1]:
				additional.append([moves[i][0], moves[i][1] + moves[i][3], moves[i][2], moves[i+1][1] - (moves[i][1] + moves[i][3])])
		added_moves = moves + additional
		added_moves = sorted(added_moves, key=operator.itemgetter(1))
		return added_moves

	def add_end_stays(self, moves, max):
		moves_copy = moves.copy()
		if moves_copy[-1][1] + moves_copy[-1][3] != max:
			moves_copy.append([moves[0][0], moves[-1][1] + moves[-1][3], moves[-1][2], max - (moves[-1][1] + moves[-1][3])])
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
		for move in self.torso_moves:
			if move[1] == beat:
				#self.torso.stop_move()
				self.torso.join()
				self.torso.add_move(move[2], 60 / tempo * move[3], vel_algo="constant")
				self.torso.start()
				break
		for move in self.neck_lr_moves:
			if move[1] == beat:
				#self.neck_lr.stop_move()
				self.neck_lr.join()
				self.neck_lr.add_move(move[2], 60 / tempo * move[3], vel_algo="constant")
				self.neck_lr.start()
				break
		for move in self.neck_ud_moves:
			if move[1] == beat:
				#self.neck_ud.stop_move()
				#self.neck_ud.join()
				self.neck_ud.add_move(move[2], 60 / tempo * move[3], vel_algo="constant")
				self.neck_ud.run()
				self.neck_ud.start()
				break
		for move in self.foot_moves:
			if move[1] == beat:
				#self.foot.stop_move()
				self.foot.join()
				self.foot.add_move(move[2], 60 / tempo * move[3], vel_algo="constant")
				self.foot.start()
				break
		for move in self.phone_moves:
			if move[1] == beat:
				#self.phone.stop_move()
				self.phone.join()
				self.phone.add_move(move[2], (60 / tempo * move[3]), vel_algo="constant")
				self.phone.start()
				break
		"""
		if int(beat * 4) <= len(self.torso_moves) - 1:
			move = self.torso_moves[int(beat * 4)]
			if len(move) != 0:
				self.torso.stop_move()
				self.torso.add_move(move[2], move[3], vel_algo="constant")
				self.torso.start()

		if int(beat * 4) <= len(self.neck_lr_moves) - 1:
			move = self.neck_lr_moves[int(beat * 4)]
			if len(move) != 0:
				self.neck_lr.stop_move()
				self.neck_lr.add_move(move[2], move[3], vel_algo="constant")
				self.neck_lr.start()

		if int(beat * 4) <= len(self.neck_ud_moves) - 1:
			move = self.neck_ud_moves[int(beat * 4)]
			if len(move) != 0:
				self.neck_ud.stop_move()
				self.neck_ud.add_move(move[2], move[3], vel_algo="constant")
				self.neck_ud.start()

		if int(beat * 4) <= len(self.foot_moves) - 1:
			move = self.foot_moves[int(beat * 4)]
			if len(move) != 0:
				self.foot.stop_move()
				self.foot.add_move(move[2], move[3], vel_algo="constant")
				self.foot.start()
		"""

	def convert_to_array_indexing(self):
		if len(self.torso_moves) != 0:
			empty_lists = [ [] for _ in range(int(self.torso_moves[-1][1] * 4) + 1) ]
			for i in range(len(self.torso_moves)):
				empty_lists[int(self.torso_moves[i][1] * 4)] = self.torso_moves[i]
			self.torso_moves = empty_lists

		if len(self.neck_lr_moves) != 0:
			empty_lists = [ [] for _ in range(int(self.neck_lr_moves[-1][1] * 4) + 1) ]
			for i in range(len(self.neck_lr_moves)):
				empty_lists[int(self.neck_lr_moves[i][1] * 4)] = self.neck_lr_moves[i]
			self.neck_lr_moves = empty_lists

		if len(self.neck_ud_moves) != 0:
			empty_lists = [ [] for _ in range(int(self.neck_ud_moves[-1][1] * 4) + 1) ]
			for i in range(len(self.neck_ud_moves)):
				empty_lists[int(self.neck_ud_moves[i][1] * 4)] = self.neck_ud_moves[i]
			self.neck_ud_moves = empty_lists

		if len(self.foot_moves) != 0:
			empty_lists = [ [] for _ in range(int(self.foot_moves[-1][1] * 4) + 1) ]
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

	def join_threads(self):
		self.neck_ud.join()
		self.neck_lr.join()
		self.torso.join()
		self.foot.join()
		self.phone.join()
