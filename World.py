import random
from Agent import Agent
from MyAI import MyAI


class World():
    
    # Tile Structure
    class __Tile:
        pit    = False;
        wumpus = False;
        gold   = False;
        breeze = False;
        stench = False;
    
    #constructor

    def __init__ ( self, file = None ):
        # Agent Initialization
        self.__goldLooted   = False
        self.__hasArrow     = True
        self.__bump         = False
        self.__scream       = False
        self.__score        = 0
        self.__agentDir     = 0
        self.__agentX       = 0
        self.__agentY       = 0
        self.__lastAction   = Agent.Action.CLIMB
        
        
        # set the AI function 
        self.__agent = MyAI()
        # set the game board
        self.__colDimension = 10
        self.__rowDimension = 10
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addFeatures() 
    
    def __randomInt (limit):
        return random.randrange(limit)

    def run ( self ):
        while self.__score >= -1000:
                        
            # Get the move
            self.__lastAction = self.__agent.getAction (
														self.__board[self.__agentX][self.__agentY].stench,
														self.__board[self.__agentX][self.__agentY].breeze,
														self.__board[self.__agentX][self.__agentY].gold,
														self.__bump,
														self.__scream
													   )

            # Make the move
            self.__score -= 1;
            self.__bump   = False;
            self.__scream = False;
            
            if self.__lastAction == Agent.Action.TURN_LEFT:
                self.__agentDir -= 1
                if (self.__agentDir < 0):
                    self.__agentDir = 3
                    
            elif self.__lastAction == Agent.Action.TURN_RIGHT:
                self.__agentDir += 1
                if self.__agentDir > 3:
                    self.__agentDir = 0
                    
            elif self.__lastAction == Agent.Action.FORWARD:
                if self.__agentDir == 0 and self.__agentX+1 < self.__colDimension:
                    self.__agentX += 1
                elif self.__agentDir == 1 and self.__agentY-1 >= 0:
                    self.__agentY -= 1
                elif self.__agentDir == 2 and self.__agentX-1 >= 0:
                    self.__agentX -= 1
                elif self.__agentDir == 3 and self.__agentY+1 < self.__rowDimension:
                    self.__agentY += 1
                else:
                    self.__bump = True
                    
                if self.__board[self.__agentX][self.__agentY].pit or self.__board[self.__agentX][self.__agentY].wumpus:
                    self.__score -= 1000
                    # if self.__debug:
                    #     self.__printWorldInfo()
                    return self.__score
                
            elif self.__lastAction == Agent.Action.SHOOT:
            
                if self.__hasArrow:
                    self.__hasArrow = False
                    self.__score -= 10
                    
                    if self.__agentDir == 0:
                        for x in range (self.__agentX, self.__colDimension):
                                if self.__board[x][self.__agentY].wumpus:
                                    self.__board[x][self.__agentY].wumpus = False
                                    self.__board[x][self.__agentY].stench = True
                                    self.__scream = True
                    
                    elif self.__agentDir == 1:
                        for y in range (self.__agentY, -1, -1):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False
                                self.__board[self.__agentX][y].stench = True
                                self.__scream = True
                    
                    elif self.__agentDir == 2:
                        for x in range (self.__agentX, -1, -1):
                            if self.__board[x][self.__agentY].wumpus:
                                self.__board[x][self.__agentY].wumpus = False
                                self.__board[x][self.__agentY].stench = True
                                self.__scream = True

                    elif self.__agentDir == 3:
                        for y in range (self.__agentY, self.__rowDimension):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False
                                self.__board[self.__agentX][y].stench = True
                                self.__scream = True
                    
            elif self.__lastAction == Agent.Action.GRAB:
                if self.__board[self.__agentX][self.__agentY].gold:
                    self.__board[self.__agentX][self.__agentY].gold = False
                    self.__goldLooted = True
                    
            elif self.__lastAction == Agent.Action.CLIMB:
                if self.__agentX == 0 and self.__agentY == 0:
                    if self.__goldLooted:
                        self.__score += 1000
                    # if (self.__debug):
                    #     self.__printWorldInfo()
                    return self.__score;
        return self.__score
    # def __addFeatures ( self, file = None ):
    def __addFeatures ( self, file = None ):
        if file == None:
            # Generate pits
            for r in range (self.__rowDimension):
                for c in range (self.__colDimension):
                    rand = random.randrange(10)
                    if (c != 0 or r != 0) and rand < 2:
                        self.__addPit ( c, r )
            
            # Generate wumpus
            wc = random.randrange(self.__colDimension)
            wr = random.randrange(self.__rowDimension)
            
            while wc == 0 and wr == 0:
                wc = self.__randomInt(self.__colDimension)
                wr = self.__randomInt(self.__rowDimension)
                
            self.__addWumpus ( wc, wr );
            
            # Generate gold
            gc = random.randrange(self.__colDimension)
            gr = random.randrange(self.__rowDimension)
                
            while gc == 0 and gr == 0:
                gc = random.randrange(self.__colDimension)
                gr = random.randrange(self.__rowDimension)
            
            self.__addGold ( gc, gr )
            
        else:
            # Add the Wumpus
            c, r = [int(x) for x in next(file).split()]
            self.__addWumpus ( c, r )
            
            # Add the Gold
            c, r = [int(x) for x in next(file).split()]
            self.__addGold ( c, r )
            
            # Add the Pits
            numOfPits = int(next(file))
            
            while numOfPits > 0:
                numOfPits -= 1
                c, r = [int(x) for x in next(file).split()]
                self.__addPit ( c, r )
                
            file.close()
    
    def __addPit ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].pit = True
            self.__addBreeze ( c+1, r )
            self.__addBreeze ( c-1, r )
            self.__addBreeze ( c, r+1 )
            self.__addBreeze ( c, r-1 )

    def __addWumpus ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].wumpus = True
            self.__addStench ( c+1, r )
            self.__addStench ( c-1, r )
            self.__addStench ( c, r+1 )
            self.__addStench ( c, r-1 )
    
    def __addGold ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].gold = True
    
    def __addStench ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = True
    
    def __addBreeze ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].breeze = True
    
    def __isInBounds ( self, c, r ):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0
    