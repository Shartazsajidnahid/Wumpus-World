from Agent import Agent


#test
class MyAI ( Agent ):

    def __init__ ( self ):
        self.__moves = 0
        self.__safe_tiles = []
        self.__unsafe_tiles = set()
        self.__tile_history = []
        self.__x_tile = 1
        self.__y_tile = 1
        self.__dir = 'E'
        self.__move_history = []
        self.__has_gold = False
        self.__revert_home = False
        self.__dest_node = (1,1)
        self.__xBorder = 0
        self.__yBorder = 0
        self.__x_border = 10
        self.__y_border = 10
        self.__dead_wump = False
        self.__found_wump = False
        self.__pitless_wump = False
        self.__wump_node = (0,0)
        self.__potential_wump_nodes = []
        self.__stench_nodes = []
        self.__potential_pit_nodes = []
        self.__breeze_nodes = []
        self.__shot_arrow = False
        pass

    def getAction( self, stench, breeze, glitter, bump, scream ):
        self.__check_bump(bump)
        
        self.__update_history_tiles()
        
        self.__moves+=1
        return self.__determineAction(stench, breeze, glitter, bump, scream)
        

    class Node:
        def __init__(self, x,y):
            self.__node = (x,y)
            self.__Nnode = (x,y+1)
            self.__Enode = (x+1,y)
            self.__Snode = (x,y-1)
            self.__Wnode = (x-1,y)
        def getCurrent(self):
            return self.__node
        def getNorth(self):
            return self.__Nnode
        def getEast(self):
            return self.__Enode
        def getSouth(self):
            return self.__Snode
        def getWest(self):
            return self.__Wnode
        def getX(self):
            return self.__node[0]
        def getY(self):
            return self.__node[1]
    def __getExploredAllSafeNodes(self):
         for i in range(len(self.__safe_tiles)):
            node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
            if node not in self.__tile_history:
                return False
         return True

    
        
    #def __determineAction(self,stench, breeze, glitter, bump, scream ):
     

    def __Update_Potential_Pit_Locations(self):
        if (self.__x_tile,self.__y_tile) in self.__breeze_nodes:
            return
        else:
            self.__breeze_nodes.append((self.__x_tile,self.__y_tile))
        Pit_Spots = []
        if self.__x_tile-1>=1: #Left
            if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile-1,self.__y_tile))
        if self.__x_tile+1<=self.__x_border: #Right
            if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile+1,self.__y_tile))
        if self.__y_tile-1>=1: #Down
            if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile,self.__y_tile-1))
        if self.__y_tile+1<=self.__y_border: #Up
            if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                Pit_Spots.append((self.__x_tile,self.__y_tile+1))
        if len(Pit_Spots)==1:
            if Pit_Spots[0] not in self.__potential_pit_nodes:
                self.__potential_pit_nodes.append(Pit_Spots[0])
            return
        for node in Pit_Spots:
            if node not in self.__potential_pit_nodes:
                self.__potential_pit_nodes.append(node)
        
    def __Update_Potential_Wump_Locations(self):
        if (self.__x_tile,self.__y_tile) in self.__stench_nodes:
            return
        else:
            self.__stench_nodes.append((self.__x_tile,self.__y_tile))
        Wump_Spots = []
        if not self.__found_wump:
            if self.__x_tile-1>=1: #Left
                if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile-1,self.__y_tile))
            if self.__x_tile+1<=self.__x_border: #Right
                if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile+1,self.__y_tile))
            if self.__y_tile-1>=1: #Down
                if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile,self.__y_tile-1))
            if self.__y_tile+1<=self.__y_border: #Up
                if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                    Wump_Spots.append((self.__x_tile,self.__y_tile+1))
                    
        if len(Wump_Spots)==1:
            self.__found_wump = True
            self.__potential_wump_nodes = []
            self.__potential_wump_nodes.append(Wump_Spots[0])
            self.__wump_node = Wump_Spots[0]
            return
        for node in Wump_Spots:
            if node in self.__potential_wump_nodes:
                self.__found_wump = True
                self.__potential_wump_nodes = []
                self.__potential_wump_nodes.append(node)
                self.__wump_node = node
                break
            else:
                self.__potential_wump_nodes.append(node)
        if self.__found_wump and not self.__pitless_wump:
            for node in self.__stench_nodes:
                if node not in self.__breeze_nodes:
                    self.__pitless_wump = True
                    break
                
    def __UpdateSafeTiles(self):
            
        if (self.__x_tile,self.__y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((self.__x_tile,self.__y_tile))
            if (self.__x_tile,self.__y_tile) in self.__potential_wump_nodes:
                self.__potential_wump_nodes.remove((self.__x_tile,self.__y_tile))
            if (self.__x_tile,self.__y_tile) in self.__potential_pit_nodes:
                self.__potential_pit_nodes.remove((self.__x_tile,self.__y_tile))
        if self.__x_tile-1>=1: #Left
            if (self.__x_tile-1,self.__y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((self.__x_tile-1,self.__y_tile))
                if (self.__x_tile-1,self.__y_tile) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((self.__x_tile-1,self.__y_tile))
                if (self.__x_tile-1,self.__y_tile) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((self.__x_tile-1,self.__y_tile))
        if self.__x_tile+1<=self.__x_border: #Right
            if (self.__x_tile+1,self.__y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((self.__x_tile+1,self.__y_tile))
                if (self.__x_tile+1,self.__y_tile) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((self.__x_tile+1,self.__y_tile))
                if (self.__x_tile+1,self.__y_tile) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((self.__x_tile+1,self.__y_tile))
        if self.__y_tile-1>=1: #Down
            if (self.__x_tile,self.__y_tile-1) not in self.__safe_tiles:
                self.__safe_tiles.append((self.__x_tile,self.__y_tile-1))
                if (self.__x_tile,self.__y_tile-1) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((self.__x_tile,self.__y_tile-1))
                if (self.__x_tile,self.__y_tile-1) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((self.__x_tile,self.__y_tile-1))
        if self.__y_tile+1<=self.__y_border: #Up
            if (self.__x_tile,self.__y_tile+1) not in self.__safe_tiles:
                self.__safe_tiles.append((self.__x_tile,self.__y_tile+1))
                if (self.__x_tile,self.__y_tile+1) in self.__potential_wump_nodes:
                    self.__potential_wump_nodes.remove((self.__x_tile,self.__y_tile+1))
                if (self.__x_tile,self.__y_tile+1) in self.__potential_pit_nodes:
                    self.__potential_pit_nodes.remove((self.__x_tile,self.__y_tile+1))

    def __UpdateSafeStench(self):
        for node in self.__stench_nodes:
            if node not in self.__breeze_nodes:
                self.__UpdateSafeTile()
        
    def __UpdateSafeTileManual(self,x_tile,y_tile):        
        if (x_tile,y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((x_tile,y_tile))
        if x_tile-1>=1: #Left
            if (x_tile-1,y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile-1,y_tile))
        if x_tile+1<=self.__x_border: #Right
            if (x_tile+1,y_tile) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile+1,y_tile))
        if y_tile-1>=1: #Down
            if (x_tile,y_tile-1) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile,y_tile-1))
        if y_tile+1<=self.__y_border: #Up
            if (x_tile,y_tile+1) not in self.__safe_tiles:
                self.__safe_tiles.append((x_tile,y_tile+1))


    def __update_history_tiles(self):
        if len(self.__tile_history) == 0:
            self.__tile_history.append((self.__x_tile,self.__y_tile))
        elif self.__tile_history[-1]!=(self.__x_tile,self.__y_tile):
            self.__tile_history.append((self.__x_tile,self.__y_tile))
        if (self.__x_tile,self.__y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((self.__x_tile,self.__y_tile))

