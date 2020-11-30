import time
import random

class Chess():

    # use file, rank as x,y, reading DOWN the board

    def __init__(self):
        self.board = []
        self.board.append('RNBQKBNR')
        self.board.append('PPPPPPPP')
        # self.board.append('........')
        self.board.append('........')
        self.board.append('........')
        self.board.append('........')
        self.board.append('........')
        # self.board.append('........')
        self.board.append('pppppppp')
        self.board.append('rnbqkbnr')

        # self.reset_board()
        # self.set_piece(4,4,'Q')
        # self.set_piece(4,5,'p')

    def reset_board(self):
        self.board = []
        for i in range(0,8):
            self.board.append('........')


    def drawBoard(self):
        for rank in self.board:
            print(rank)
        print('')

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
            moves.append([file, rank + direction, 0, file, rank, self.getPiece(file, rank)])
        if rank == 1 and self.getPiece(file, rank + 2 * direction) == '.':
            moves.append([file, rank + 2 *  direction, 0, file, rank, self.getPiece(file, rank)])
        target = self.getPiece(file - 1, rank + direction)
        if target != None and target != '.' and self.opposition(target, white):
            moves.append([file - 1, rank + direction, self.getPieceValue(target), file, rank, self.getPiece(file, rank)])
        target = self.getPiece(file + 1, rank + direction)
        if target != None and target != '.' and self.opposition(target, white):
            moves.append([file + 1, rank + direction, self.getPieceValue(target), file, rank, self.getPiece(file, rank)])
        if len(moves) == 0:
            return None
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup:tup[2], reverse=True)
        return moves[0]

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
            moves.append([new_file, new_rank, self.getPieceValue(target), file, rank, me])
            break
        return moves

    def moveRook(self, file, rank, white):
        moves = []
        moves.extend(self.moveDirection(file, rank, white, 1, 0))
        moves.extend(self.moveDirection(file, rank, white, 0, 1))
        moves.extend(self.moveDirection(file, rank, white, -1, 0))
        moves.extend(self.moveDirection(file, rank, white, 0, -1))
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup:tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

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
        moves = sorted(moves, key=lambda tup:tup[2], reverse=True)
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
        moves = sorted(moves, key=lambda tup:tup[2], reverse=True)
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
        moves = sorted(moves, key=lambda tup:tup[2], reverse=True)
        if len(moves) == 0:
            return None
        return moves[0]

    def move(self, from_file, from_rank, to_file, to_rank):
        self.set_piece(to_file, to_rank, self.board[from_rank][from_file] )
        self.set_piece(from_file, from_rank, '.')

    def set_piece(self, file, rank, piece):
        old_rank = self.board[rank]
        new_rank = old_rank[:file] + piece + old_rank[file+1:]
        self.board[rank] = new_rank
        
    def handle_special_circumstances(self, move, white):
        if move[5] == 'P' and move[1] == 7:
            self.set_piece(move[0],move[1],'Q')
        if move[5] == 'p' and move[1] == 0:
            self.set_piece(move[0],move[1],'Q')
        # en passant 

    def moveWhite(self):
        return self.move_generic(True)
    
    def move_generic(self, white):
        pieces = self.findPieces(white)
        moves = self.findMoves(pieces, white)
        if len(moves) == 0:
            return False
        random.shuffle(moves)
        moves = sorted(moves, key=lambda tup:tup[2], reverse=True)
        move = moves[0]
        self.move(move[3],move[4],move[0],move[1])
        self.handle_special_circumstances(move, white)
        return True

    def moveBlack(self):
        return self.move_generic(False)

    def play(self):
        self.drawBoard()
        move = 1
        sleep = 0.1
        while(True):
            print('{} white \n'.format(move))
            if not self.moveWhite():
                print('white has no moves')
                break
            self.drawBoard()
            time.sleep(sleep)
            if not self.pieceExists('k'):
                print('White won')
                break
            print('{} black \n'.format(move))
            if not self.moveBlack():
                print('black has no moves')
                break
            self.drawBoard()
            time.sleep(sleep)
            if not self.pieceExists('K'):
                print('Black won')
                break
            move = move + 1
        pass


chess = Chess()
chess.play()
