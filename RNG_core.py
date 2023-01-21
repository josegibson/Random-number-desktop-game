import random

class RandomNumberGame:
    def __init__(self):
        self.win_matrix = [0] * 13

    def set_win_matrix(self, number):
        self.win_matrix[number] = 9
        self.win_matrix[10] = 2 if number in [1, 3, 7, 9] else 1.5 if number == 5 else 0
        self.win_matrix[11] = 2 if number in [2, 4, 6, 8] else 1.5 if number == 0 else 0
        self.win_matrix[12] = 4.5 if number in [0, 5] else 0

    def play_round(self, bets_matrix):
        self.set_win_matrix(random.randint(0, 9))
        prize_matrix = [round(self.win_matrix[i] * bets_matrix[i] * 0.97, 2) for i in range(13)]
        return prize_matrix



