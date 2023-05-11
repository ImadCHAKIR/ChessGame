# this class is responsble of:
# storing all data about the current state of a chess game
# determining the valid move of the current state 

import ChessMove

class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions = { 'p': self.getPawnMoves, 'R': self.getRookMoves,
                                'Q': self.getQueenMoves , 'K':self.getKingMoves,
                                'B': self.getBishopMoves, 'N':self.getKnightMoves}
        self.sqSelected = ()
        self.whiteToMove = True
        self.moveLog=[]
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.blackCastling = (True,True)
        self.whiteCastling = (True,True)
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        
        if move.pieceMoved[1] == 'p' and move.pieceCaptured == "--" and move.startCol != move.endCol:
            self.board[move.startRow][move.endCol] = "--"
            
        if move.pieceMoved[1]=='K':
            if abs(move.startCol - move.endCol)==2:
                self.board[move.startRow][0 if move.endCol<4 else 7] = "--"
                self.board[move.endRow][3 if move.endCol<4 else 5] = move.pieceMoved[0] + 'R'
            
            if self.whiteToMove: 
                self.whiteKingLocation = (move.endRow, move.endCol) 
                self.whiteCastling = (False,False)
            else: 
                self.blackKingLocation = (move.endRow, move.endCol) 
                self.blackCastling = (False,False)
            
        if move.pieceMoved[1]=='R':
            if move.startCol in [0,7]:
                if self.whiteToMove:
                    self.whiteCastling[move.startCol//7]= False
                else:
                    self.blackCastling[move.startCol//7]= False
                                      
        self.whiteToMove= not self.whiteToMove 
              
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove= not self.whiteToMove 
            
            if move.pieceMoved[1] == 'p' and move.pieceCaptured == "--" and move.startCol != move.endCol:
                self.board[move.startRow][move.endCol] = ('b' if self.whiteToMove else 'w')  + 'p'
            
            if abs(move.startCol - move.endCol)==2:
                self.board[move.startRow][0 if move.endCol<4 else 7] = move.pieceMoved[0] + 'R'
                self.board[move.endRow][3 if move.endCol<4 else 5] = "--"
            
            if move.pieceMoved[1]=='K':
                if self.whiteToMove: 
                    self.whiteKingLocation = (move.startRow, move.startCol) 
                    self.whiteCastling = (True,True)
                else: 
                    self.blackKingLocation = (move.startRow, move.startCol)
                    self.blackCastling = (True,True)          
            
            if move.pieceMoved[1]=='R':
                if move.startCol in [0,7]:
                    if self.whiteToMove:
                        self.whiteCastling[move.startCol//7]= True
                    else:
                        self.blackCastling[move.startCol//7]= True
                        
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
            
        if self.inCheck:
            if len(self.checks) == 1:
                moves =self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] == 'K':
                        if (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
                    else:
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])          
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()        
        
        return moves
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        
        if self.whiteToMove:
            ennemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:   
            ennemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
            
        directions = ((0,1),(0,-1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow +d[0]*i
                endCol = startCol +d[1]*i
                if 0<= endRow <8 and 0<= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin =(endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == ennemyColor:
                        type = endPiece[1]
                        if (0<= j <=3 and type == 'R') or\
                            (4<= j <=7 and type == 'B') or\
                            (i==1 and type == 'p' and ((ennemyColor == 'w' and 6<= j <=7) or (ennemyColor == 'b' and 4<= j <=5))) or\
                            (type =='Q') or (i==1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((1,2),(1,-2),(-1,-2),(-1,2),(2,1),(2,-1),(-2,1),(-2,-1))
        for m in knightMoves:
            endRow = startRow +m[0]
            endCol = startCol +m[1]
            if 0<= endRow <8 and 0<= endCol <8:
                endPiece =self.board[endRow][endCol]
                if endPiece[0] == ennemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
                        
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    
    def getPawnMoves(self,r,c,moves):
        pawnMove = -1 if self.whiteToMove else 1
        notTurn = 'b' if self.whiteToMove else 'w'
        
        if 0<r<7:
            if self.board[r+pawnMove][c]=="--":    
                moves.append(ChessMove.Move((r,c),(r+pawnMove,c),self.board))
                if self.board[int(3.5-0.5*pawnMove)][c]=="--" and r==int(3.5-2.5*pawnMove): 
                    moves.append(ChessMove.Move((r,c),(int(3.5-0.5*pawnMove),c),self.board))
            if c>=1 and  self.board[r+pawnMove][c-1][0] == notTurn:
                moves.append(ChessMove.Move((r,c),(r+pawnMove,c-1),self.board))
            if  c<=6 and self.board[r+pawnMove][c+1][0] == notTurn:
                moves.append(ChessMove.Move((r,c),(r+pawnMove,c+1),self.board))
                
        if ((self.whiteToMove and r==3) or (not self.whiteToMove and r==4)) and self.moveLog[-1].pieceMoved[1] == 'p':
            if abs(self.moveLog[-1].startCol-c)==1 and abs(self.moveLog[-1].startRow-self.moveLog[-1].endRow)==2:
                moves.append(ChessMove.Move((r,c),(r+(self.moveLog[-1].startRow-self.moveLog[-1].endRow)//2,self.moveLog[-1].startCol),self.board))
             
    def getRookMoves(self,r,c,moves):
        turn = 'w' if self.whiteToMove else 'b'
        notTurn = 'w' if not self.whiteToMove else 'b'
        rookMoves = ((0,1),(0,-1),(-1,0),(1,0))
        
        for m in rookMoves:
            a,b=r,c
            while (0<=a+m[0]<=7 and 0<=b+m[1]<=7):
                if self.board[a+m[0]][b+m[1]]=="--":
                    moves.append(ChessMove.Move((r,c),(a+m[0],b+m[1]),self.board))            
                elif self.board[a+m[0]][b+m[1]][0]==notTurn:
                    moves.append(ChessMove.Move((r,c),(a+m[0],b+m[1]),self.board))            
                    break
                elif self.board[a+m[0]][b+m[1]][0]==turn:          
                    break
                a+=m[0]
                b+=m[1]
              
    def getBishopMoves(self,r,c,moves):
        turn = 'w' if self.whiteToMove else 'b'
        notTurn = 'w' if not self.whiteToMove else 'b'
        bishopMoves = ((1,1),(1,-1),(-1,1),(-1,-1))
        for m in bishopMoves:
            a,b = r + m[0],c + m[1]
            while (0<=a<=7 and 0<=b<=7):
                if self.board[a][b]=="--":
                    moves.append(ChessMove.Move((r,c),(a,b),self.board))            
                elif self.board[a][b][0]==notTurn:
                    moves.append(ChessMove.Move((r,c),(a,b),self.board))            
                    break
                elif self.board[a][b][0]==turn:          
                    break
                a += m[0]
                b += m[1]
                
    def getKingMoves(self,r,c,moves):
        turn = 'w' if self.whiteToMove else 'b'
        kingMoves = ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <= 7 and 0 <=endCol <= 7 :
                if self.board[endRow][endCol][0]!=turn:
                    moves.append(ChessMove.Move((r,c),(endRow,endCol),self.board))
                    
        if self.whiteToMove:
            if self.whiteCastling[0] == True and\
                self.board[7][1]=="--" and self.board[7][2]=="--" and self.board[7][3]=="--":
                moves.append(ChessMove.Move((7,4), (7,2),self.board))
            if self.whiteCastling[1] == True and\
                self.board[7][5]=="--" and self.board[7][6]=="--":
                moves.append(ChessMove.Move((7,4), (7,6),self.board)) 
                   
        if not self.whiteToMove:
            if self.blackCastling[0] == True and\
                self.board[0][1]=="--" and self.board[0][2]=="--" and self.board[0][3]=="--":
                moves.append(ChessMove.Move((0,4), (0,2),self.board))
            if self.blackCastling[1] == True and\
                self.board[0][5]=="--" and self.board[0][6]=="--":
                moves.append(ChessMove.Move((0,4), (0,6),self.board))  
     
    def getKnightMoves(self,r,c,moves):
        turn = 'w' if self.whiteToMove else 'b'
        knightMoves = ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <= 7 and 0 <=endCol <= 7 :
                if self.board[endRow][endCol][0]!=turn:
                    moves.append(ChessMove.Move((r,c),(endRow,endCol),self.board))  
        
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
    