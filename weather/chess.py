import time
import random

#from sense_emu import SenseHat
from sense_hat import SenseHat

# Basic chess demo for SenseHat. Has most moves (can't do en passant, castling, pawns always
# promote to Queen) and only takes best attacking move possible (won't defend, will also open to check.)
# Cute enough for a display, but not a serious simulation yet. This is a slightly modified copy of the plain one
# (up one dir, down to chess) set up to integrate nicely with my Weather app.
#
# Simon Garton
# simon.garton@gmail.com
# November / December 2020


class Chess():

    # use file, rank as x,y, reading DOWN the board
    def __init__(self):
        self.board = []
        self.board.append('RNBQKBNR')
        self.board.append('PPPPPPPP')
        self.board.append('........')
        self.board.append('........')
        self.board.append('........')
        self.board.append('........')
        self.board.append('pppppppp')
        self.board.append('rnbqkbnr')

        self.color_values = {
            'k': 250,
            'q': 200,
            'r': 150,
            'b': 100,
            'n': 50,
            'p': 0
        }

        self.sense = SenseHat()
        self.sense.clear()

        self.draw_board()
        time.sleep(3)

    def reset_board(self):
        self.board = []
        for i in range(0, 8):
            self.board.append('........')

    def remove_pieces(self, white):
        for file in range(0, 8):
            for rank in range(0, 8):
                tile = self.getPiece(file, rank)
                if tile == '.':
                    continue
                if tile.isupper() and not white:
                    self.set_piece(file, rank, '.')
                    self.undraw_piece(file, rank)
                    time.sleep(0.2)
                if tile.islower() and white:
                    self.set_piece(file, rank, '.')
                    self.undraw_piece(file, rank)
                    time.sleep(0.2)

    def draw_board(self):
        self.sense.clear()
        for file in range(0, 8):
            for rank in range(0, 8):
                tile = self.getPiece(file, rank)
                if tile == '.':
                    continue
                self.draw_piece(tile, file, rank)

    def draw_piece(self, tile, file, rank):
        if tile.isupper():
            self.sense.set_pixel(
                file, rank, [255, 0, self.color_values[tile.lower()]])
        else:
            self.sense.set_pixel(
                file, rank, [0, 255, self.color_values[tile.lower()]])

    def undraw_piece(self, file, rank):
        self.sense.set_pixel(file, rank, [0, 0, 0])

    def findPieces(self, white):
        pieces = []
        for file in range(0, 8):
            for rank in range(0, 8):
                tile = self.getPiece(file, rank)
                if tile == '.':
                    continue
                if white and tile.isupper():
                    pieces.append([file, rank, tile])
                if not white and not tile.isupper():
                    pieces.append([file, rank, tile])
        return pieces

    def findMoves(self, pieces, white):
        moves = []
        for piece in pieces:
            move = self.findMove(piece, white)
            if not move == None:
                moves.append(move)
        return moves

    def findMove(self, piece, white):
        # best move for this piece (there may be many moves)
        file = piece[0]
        rank = piece[1]
        type = piece[2]
        if type == 'P' or type == 'p':
            return self.movePawn(file, rank, white)
        if type == 'R' or type == 'r':
            return self.moveRook(file, rank, white)
        if type == 'B' or type == 'b':
            return self.moveBishop(file, rank, white)
        if type == 'Q' or type == 'q':
            return self.moveQueen(file, rank, white)
        if type == 'K' or type == 'k':
            return self.moveKing(file, rank, white)
        if type == 'N' or type == 'n':
            return self.moveKnight(file, rank, white)
        return None

    def pieceExists(self, piece):
        for rank in self.board:
            if piece in rank:
                return True
        return False

    def getPiece(self, file, rank):
        if rank < 0 or rank > 7:
            return None
        if file < 0 or file > 7:
            return None
        return self.board[rank][file]

    def getPieceValue(self, piece):
        pieceLower = piece.lower()
        if pieceLower == 'p':
            return 1
        if pieceLower == 'n' or pieceLower == 'b':
            return 3
        if pieceLower == 'r':
            return 5
        if pieceLower == 'q':
            return 9
        if pieceLower == 'k':
            return 100

    def opposition(self, piece, white):
        if white:
            return piece.islower()
        else:
            return piece.isupper()

    def movePawn(self, file, rank, white):
        # a move is [to-file, to-rank, value, from-file, from-rank, moving-piece]
        direction = 1 if white else -1
        moves = []
        if self.getPiece(file, rank + direction) == '.':
            moves.append([file, rank + direction, 0, file,
                          rank, self.getPiece(file, rank)])
        if rank == 1 and self.getPiece(file, rank + 2 * direction) == '.':
            moves.append([file, rank + 2 * direction, 0, file,
                          rank, self.getPiece(file, rank)])
        target = self.getPiece(file - 1, rank + direction)
        if target != None and target != '.' and self.opposition(target, white):
            moves.append([file - 1, rank + direction, self.getPieceValue(target),
                          file, rank, self.getPiece(file, rank)])
        target = self.getPiece(file + 1, rank + direction)
        if target != None and target != '.' and self.opposition(target, white):
            moves.append([file + 1, rank + direction, self.getPieceValue(target),
                          file, rank, self.getPiece(file, rank)])
        if len(moves) == 0:
            return None
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        return moves[0]

    def moveDirectionOnce(self, file, rank, white, xdelta, ydelta):
        me = self.getPiece(file, rank)
        moves = []
        new_file = file + xdelta
        new_rank = rank + ydelta
        target = self.getPiece(new_file, new_rank)
        if target == None:
            return moves
        if target == '.':
            moves.append([new_file, new_rank, 0, file, rank, me])
            return moves
        if not self.opposition(target, white):
            return moves
        moves.append(
            [new_file, new_rank, self.getPieceValue(target), file, rank, me])
        return moves

    def moveDirection(self, file, rank, white, xdelta, ydelta):
        me = self.getPiece(file, rank)
        moves = []
        new_file = file + xdelta
        new_rank = rank + ydelta
        while(True):
            target = self.getPiece(new_file, new_rank)
            if target == None:
                break
            if target == '.':
                moves.append([new_file, new_rank, 0, file, rank, me])
                new_file = new_file + xdelta
                new_rank = new_rank + ydelta
                continue
            if not self.opposition(target, white):
                break
            moves.append(
                [new_file, new_rank, self.getPieceValue(target), file, rank, me])
            break
        return moves

    def moveQueen(self, file, rank, white):
        moves = []
        moves.extend(self.moveDirection(file, rank, white, 1, 1))
        moves.extend(self.moveDirection(file, rank, white, -1, 1))
        moves.extend(self.moveDirection(file, rank, white, 1, -1))
        moves.extend(self.moveDirection(file, rank, white, -1, -1))
        moves.extend(self.moveDirection(file, rank, white, 1, 0))
        moves.extend(self.moveDirection(file, rank, white, 0, 1))
        moves.extend(self.moveDirection(file, rank, white, -1, 0))
        moves.extend(self.moveDirection(file, rank, white, 0, -1))
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

    def moveKing(self, file, rank, white):
        moves = []
        moves.extend(self.moveDirectionOnce(file, rank, white, 1, 1))
        moves.extend(self.moveDirectionOnce(file, rank, white, -1, 1))
        moves.extend(self.moveDirectionOnce(file, rank, white, 1, -1))
        moves.extend(self.moveDirectionOnce(file, rank, white, -1, -1))
        moves.extend(self.moveDirectionOnce(file, rank, white, 1, 0))
        moves.extend(self.moveDirectionOnce(file, rank, white, 0, 1))
        moves.extend(self.moveDirectionOnce(file, rank, white, -1, 0))
        moves.extend(self.moveDirectionOnce(file, rank, white, 0, -1))
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

    def moveKnight(self, file, rank, white):
        moves = []
        moves.extend(self.moveDirectionOnce(file, rank, white, 1, 2))
        moves.extend(self.moveDirectionOnce(file, rank, white, -1, 2))
        moves.extend(self.moveDirectionOnce(file, rank, white, 2, 1))
        moves.extend(self.moveDirectionOnce(file, rank, white, 2, -1))
        moves.extend(self.moveDirectionOnce(file, rank, white, 1, -2))
        moves.extend(self.moveDirectionOnce(file, rank, white, -1, -2))
        moves.extend(self.moveDirectionOnce(file, rank, white, -2, 1))
        moves.extend(self.moveDirectionOnce(file, rank, white, -2, -1))
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

    def moveBishop(self, file, rank, white):
        moves = []
        moves.extend(self.moveDirection(file, rank, white, 1, 1))
        moves.extend(self.moveDirection(file, rank, white, -1, 1))
        moves.extend(self.moveDirection(file, rank, white, 1, -1))
        moves.extend(self.moveDirection(file, rank, white, -1, -1))
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

    def moveRook(self, file, rank, white):
        moves = []
        moves.extend(self.moveDirection(file, rank, white, 1, 0))
        moves.extend(self.moveDirection(file, rank, white, 0, 1))
        moves.extend(self.moveDirection(file, rank, white, -1, 0))
        moves.extend(self.moveDirection(file, rank, white, 0, -1))
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

    def move(self, from_file, from_rank, to_file, to_rank):
        tile = self.board[from_rank][from_file]
        self.set_piece(to_file, to_rank, tile)
        self.set_piece(from_file, from_rank, '.')
        self.draw_piece(tile, to_file, to_rank)
        self.undraw_piece(from_file, from_rank)

    def set_piece(self, file, rank, piece):
        old_rank = self.board[rank]
        new_rank = old_rank[:file] + piece + old_rank[file+1:]
        self.board[rank] = new_rank

    def handle_special_circumstances(self, move, white):
        if move[5] == 'P' and move[1] == 7:
            self.set_piece(move[0], move[1], 'Q')
        if move[5] == 'p' and move[1] == 0:
            self.set_piece(move[0], move[1], 'q')
        # en passant

    def moveWhite(self):
        return self.move_generic(True)

    def moveBlack(self):
        return self.move_generic(False)

    def move_generic(self, white):
        pieces = self.findPieces(white)
        moves = self.findMoves(pieces, white)
        if len(moves) == 0:
            return False
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup: tup[2], reverse=True)
        move = moves[0]
        self.move(move[3], move[4], move[0], move[1])
        self.handle_special_circumstances(move, white)
        return True

    def play(self):
        move = 1
        sleep = 0.5
        while(True):
            print('{} white \n'.format(move))
            if not self.moveWhite():
                print('white has no moves')
                break
            time.sleep(sleep)
            if not self.pieceExists('k'):
                print('White won')
                time.sleep(3)
                self.remove_pieces(True)
                time.sleep(3)
                break
            print('{} black \n'.format(move))
            if not self.moveBlack():
                print('black has no moves')
                break
            time.sleep(sleep)
            if not self.pieceExists('K'):
                print('Black won')
                time.sleep(3)
                self.remove_pieces(False)
                time.sleep(3)
                break
            move = move + 1
        pass
