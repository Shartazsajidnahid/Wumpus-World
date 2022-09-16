from Agent import Agent


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
            
        # set the game board