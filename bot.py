import argparse
import chess
import sys

import chess_state
import evaluators
import minimax

argparser = argparse.ArgumentParser()
argparser.add_argument('--player', "-p", default="white", type=str, help="'[w]hite' or '[b]lack'; the bot player's color")

class Bot(object):
    def __init__(self, player=chess.WHITE, searchdepth=5, evaluate=evaluators.MaterialEvaluator()):
        self.state = chess_state.ChessState(evaluate=evaluate)
        self.player = player
        self.searchdepth = searchdepth

    def choose_move(self):
        _, move = minimax.minimax(self.state,
                player=(minimax.MAX
                    if self.player == chess.WHITE
                    else minimax.MIN),
                maxdepth=self.searchdepth)

        return move

    def make_move(self, move):
        self.state.push(move)

def main(player=chess.WHITE, searchdepth=2):
    b = Bot(player=player, searchdepth=searchdepth)
    if player == chess.WHITE:
        m = b.choose_move()
        print(m.uci())
        b.make_move(m)
        print(b.state)
        print()

    while True:
        m = chess.Move.from_uci(input())
        while not b.state.is_legal(m):
            print("Illegal move! Try again.\n")
            m = chess.Move.from_uci(input())

        b.make_move(m)
        print(b.state)
        print()
        if b.state.is_game_over():
            print("Game over!")
            break

        m = b.choose_move()
        print(m.uci())
        b.make_move(m)
        print(b.state)
        print()
        if b.state.is_game_over():
            print("Game over!")
            break


if __name__ == "__main__":
    args = argparser.parse_args()
    main()

