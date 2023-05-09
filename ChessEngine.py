# this class is responsble of:
# storing all data about the current state of a chess game
# determining the valid move of the current state 

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
        self.whiteToMove = True
        self.moveLog=[]
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove= not self.whiteToMove 
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove= not self.whiteToMove 
            
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r,c,moves) 
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
                    elif piece == 'B':
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getBishopMoves(r,c,moves)
                        self.getRookMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)
                    elif piece == 'N':
                        self.getKnightMoves(r,c,moves)
                       
        return moves
    
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove : 
            if self.board[r-1][c]=="--":    
                moves.append(Move((r,c),(r-1,c),self.board))
                if self.board[4][c]=="--" and r==6: 
                    moves.append(Move((6,c),(4,c),self.board))
            if c>=1 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if  c<=6 and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r,c),(r-1,c+1),self.board))
        if not self.whiteToMove : 
            if self.board[r+1][c]=="--":    
                moves.append(Move((r,c),(r+1,c),self.board))
                if self.board[3][c]=="--" and r==1: 
                    moves.append(Move((1,c),(3,c),self.board))
            if  c>=1 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if  c<=6 and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r,c),(r+1,c+1),self.board))
                
    def getRookMoves(self,r,c,moves):
        turn = 'w' if self.whiteToMove else 'b'
        notTurn = 'w' if not self.whiteToMove else 'b'
        a = r
        while (a<7):
            if self.board[a+1][c]=="--":
                moves.append(Move((r,c),(a+1,c),self.board))            
            elif self.board[a+1][c][0]==notTurn:
                moves.append(Move((r,c),(a+1,c),self.board))            
                break
            elif self.board[a+1][c][0]==turn:          
                break
            a+=1
        a = r
        while (a>0):
            if self.board[a-1][c]=="--":
                moves.append(Move((r,c),(a-1,c),self.board))            
            elif self.board[a-1][c][0]==notTurn:
                moves.append(Move((r,c),(a-1,c),self.board))            
                break
            elif self.board[a-1][c][0]==turn:          
                break
            a-=1
        a=c
        while (a>0):
            if self.board[r][a-1]=="--":
                moves.append(Move((r,c),(r,a-1),self.board))            
            elif self.board[r][a-1][0]==notTurn:
                moves.append(Move((r,c),(r,a-1),self.board))            
                break
            elif self.board[a-1][c][0]==turn:          
                break
            a-=1
        a=c
        while (a<7):
            if self.board[r][a+1]=="--":
                moves.append(Move((r,c),(r,a+1),self.board))            
            elif self.board[r][a+1][0]==notTurn:
                moves.append(Move((r,c),(r,a+1),self.board))            
                break
            elif self.board[a+1][c][0]==turn:          
                break
            a+=1
        
    def getBishopMoves(self,r,c,moves):
        turn = 'w' if self.whiteToMove else 'b'
        notTurn = 'w' if not self.whiteToMove else 'b'
        a,b = r,c
        while (a<7 and b<7):
            if self.board[a+1][b+1]=="--":
                moves.append(Move((r,c),(a+1,b+1),self.board))            
            elif self.board[a+1][b+1][0]==notTurn:
                moves.append(Move((r,c),(a+1,b+1),self.board))            
                break
            elif self.board[a+1][b+1][0]==turn:          
                break
            a+=1
            b+=1
            
        a,b = r,c
        while (a>0 and b>0):
            if self.board[a-1][b-1]=="--":
                moves.append(Move((r,c),(a-1,b-1),self.board))            
            elif self.board[a-1][b-1][0]==notTurn:
                moves.append(Move((r,c),(a-1,b-1),self.board))            
                break
            elif self.board[a-1][b-1][0]==turn:          
                break
            a-=1
            b-=1
        
        a,b = r,c
        while (a>0 and b<7):
            if self.board[a-1][b+1]=="--":
                moves.append(Move((r,c),(a-1,b+1),self.board))            
            elif self.board[a-1][b+1][0]==notTurn:
                moves.append(Move((r,c),(a-1,b+1),self.board))            
                break
            elif self.board[a-1][b+1][0]==turn:          
                break
            a-=1
            b+=1   
            
        a,b = r,c
        while (b>0 and a<7):
            if self.board[a+1][b-1]=="--":
                moves.append(Move((r,c),(a+1,b-1),self.board))            
            elif self.board[a+1][b-1][0]==notTurn:
                moves.append(Move((r,c),(a+1,b-1),self.board))            
                break
            elif self.board[a+1][b-1][0]==turn:          
                break
            a+=1
            b-=1     
                
    def getKingMoves(self,r,c,moves):
        notTurn = 'w' if not self.whiteToMove else 'b'
        
        if r<7 and (self.board[r+1][c]=="--" or self.board[r+1][c][0]==notTurn):
            moves.append(Move((r,c),(r+1,c),self.board))  
        if r>0 and (self.board[r-1][c]=="--" or self.board[r-1][c][0]==notTurn):
            moves.append(Move((r,c),(r-1,c),self.board))   
              
        if c<7 and (self.board[r][c+1]=="--" or self.board[r][c+1][0]==notTurn):
            moves.append(Move((r,c),(r,c+1),self.board))  
        if c>0 and (self.board[r][c-1]=="--" or self.board[r][c-1][0]==notTurn):
            moves.append(Move((r,c),(r,c-1),self.board)) 
            
        if r<7 and c<7 and (self.board[r+1][c+1]=="--" or self.board[r+1][c+1][0]==notTurn):
            moves.append(Move((r,c),(r+1,c+1),self.board))  
        if r>0 and c>0 and (self.board[r-1][c-1]=="--" or self.board[r-1][c-1][0]==notTurn):
            moves.append(Move((r,c),(r-1,c-1),self.board))   
              
        if c<7 and r>0 and (self.board[r-1][c+1]=="--" or self.board[r-1][c+1][0]==notTurn):
            moves.append(Move((r,c),(r-1,c+1),self.board))  
        if c>0 and r<7 and (self.board[r+1][c-1]=="--" or self.board[r+1][c-1][0]==notTurn):
            moves.append(Move((r,c),(r+1,c-1),self.board))      
     
    def getKnightMoves(self,r,c,moves):
        notTurn = 'w' if not self.whiteToMove else 'b'
        
        if r<6 and c<7 and (self.board[r+2][c+1]=="--" or self.board[r+2][c+1][0]==notTurn):
            moves.append(Move((r,c),(r+2,c+1),self.board))  
        if r>1 and c>0 and (self.board[r-2][c-1]=="--" or self.board[r-2][c-1][0]==notTurn):
            moves.append(Move((r,c),(r-2,c-1),self.board))   
              
        if r<7 and c<6 and (self.board[r+1][c+2]=="--" or self.board[r+1][c+2][0]==notTurn):
            moves.append(Move((r,c),(r+1,c+2),self.board))  
        if r>0 and c>1 and (self.board[r-1][c-2]=="--" or self.board[r-1][c-2][0]==notTurn):
            moves.append(Move((r,c),(r-1,c-2),self.board))
            
        if r<7 and c>1 and (self.board[r+1][c-2]=="--" or self.board[r+1][c-2][0]==notTurn):
            moves.append(Move((r,c),(r+1,c-2),self.board))  
        if r>1 and c<7 and (self.board[r-2][c+1]=="--" or self.board[r-2][c+1][0]==notTurn):
            moves.append(Move((r,c),(r-2,c+1),self.board))
            
        if r<6 and c>0 and (self.board[r+2][c-1]=="--" or self.board[r+2][c-1][0]==notTurn):
            moves.append(Move((r,c),(r+2,c-1),self.board))  
        if r>0 and c<6 and (self.board[r-1][c+2]=="--" or self.board[r-1][c+2][0]==notTurn):
            moves.append(Move((r,c),(r-1,c+2),self.board))
        
class Move():
    ranksToRows = { "1":7, "2":6, "3":5, "4":4, 
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = { v:k for k,v in ranksToRows.items()}
    
    filesToCols = { "a":0, "b":1, "c":2, "d":3, 
                   "e":4, "f":5, "g":6, "h":7}
    colsToFils = { v:k for k,v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
            
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFils[c] + self.rowsToRanks[r]