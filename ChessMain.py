# This class is responsible for:
#   hundling user input
# displaying the current GameState object

import pygame as p
import ChessEngine

Width = Height = 512
Dimension = 8
SQ_Size = Height/Dimension
Max_FPS = 15
Images = {}

def loadImages():
    pieces = ["bp","bR","bN","bB","bQ","bK","wp","wR","wN","wB","wQ","wK"]
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load("./images/" +piece+".png"),(SQ_Size,SQ_Size))
        
        
def main():
    p.init()
    screen = p.display.set_mode((Width,Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected =()
    playerClicks = []
    
    while running: 
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = int(location[0]//SQ_Size)
                row = int(location[1]//SQ_Size)
                
                if gs.board[row][col] =="--" and  sqSelected == ():
                    continue
                
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen,gs)
        clock.tick(Max_FPS)
        p.display.flip()
        
def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_Size,r*SQ_Size,SQ_Size,SQ_Size ))
            
    
def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece!='--':
                screen.blit(Images[piece],p.Rect(c*SQ_Size,r*SQ_Size,SQ_Size,SQ_Size))

if __name__ == "__main__":
    main()

    
    