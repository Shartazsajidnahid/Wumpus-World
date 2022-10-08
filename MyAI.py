from Agent import Agent


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
        self.__path_home = []
        self.__dest_path = []
        self.__dest_node = (1,1)
        self.__xBorder = 0
        self.__yBorder = 0
        self.__in_danger = False
        self.__last_danger = (0,0)
        self.__x_border = 7
        self.__y_border = 7
        self.__stop_iteration = False
        self.__stopped_on_iteration = 0
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
    def __determineAction(self,stench, breeze, glitter, bump, scream ):
        if scream:
            if self.__wump_node == (0,0):
                self.__wump_node = (2,1)
            self.__UpdateSafeStench()
            self.__dead_wump = True
            if self.__wump_node not in self.__safe_tiles:
                self.__safe_tiles.append(self.__wump_node)
            found_node = False
            for i in range(len(self.__safe_tiles)):
                node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
                if node not in self.__tile_history:
                    self.__dest_node = (node[0], node[1])
                    self.__dest_path = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
                    self.__stop_iteration = False
                    found_node = True
                    break
            if not found_node:
                self.__revert_home = True
            else:
                self.__revert_home = False
        elif self.__moves == 2 and stench == True and self.__shot_arrow:
            self.__safe_tiles.append((2,1))
            self.__wump_node = (1,2)
            self.__potential_wump_nodes.append(self.__wump_node)
            self.__found_wump = True
            found_node = False
            for i in range(len(self.__safe_tiles)):
                node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
                if node not in self.__tile_history:
                    self.__dest_node = (node[0], node[1])
                    self.__dest_path = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
                    self.__stop_iteration = False
                    found_node = True
                    break
            if not found_node:
                self.__revert_home = True
            else:
                self.__revert_home = False
        if not breeze and not bump:
            if  not stench or (stench and self.__dead_wump):
                self.__UpdateSafeTiles()
        if not self.__shot_arrow and self.__pitless_wump and not self.__dead_wump:
            if self.__Facing_Wump():
                self.__shot_arrow = True
                self.__print_debug_info(stench, breeze, glitter, bump, scream)
                return Agent.Action.SHOOT
            else:
                return self.__Align_To_Wump(stench, breeze, glitter, bump, scream)
        if breeze:
            self.__Update_Potential_Pit_Locations()
        if stench and not self.__found_wump:
            self.__Update_Potential_Wump_Locations()
        if (breeze or bump or (stench and not self.__dead_wump)):
            if bump:
                if self.__dir == 'E':
                    self.__x_border = self.__x_tile
                    for i in self.__safe_tiles:
                        if i[0] > self.__x_border:
                            self.__safe_tiles.remove(i)
                elif self.__dir == 'N':
                    self.__y_border = self.__y_tile
                    for i in self.__safe_tiles:
                        if i[1] > self.__y_border:
                            self.__safe_tiles.remove(i)
            if (not self.__in_danger) or (self.__in_danger and (self.__last_danger != (self.__x_tile,self.__y_tile)) or self.__dest_node not in self.__safe_tiles):
                found_node = False
                for i in range(len(self.__safe_tiles)):
                    node = self.__safe_tiles[len(self.__safe_tiles)-i-1]
                    if node not in self.__tile_history:
                        self.__dest_node = (node[0], node[1])
                        self.__dest_path = self.__optimal_home_path(self.__x_tile,self.__y_tile,self.__dest_node[0],self.__dest_node[1])
                        self.__stop_iteration = False
                        found_node = True
                        break
                self.__in_danger = True
                self.__last_danger = (self.__x_tile,self.__y_tile)
                if not found_node:
                    self.__revert_home = True
        else:
            self.__in_danger = False
        if not self.__revert_home:
            if self.__moves > 1:
                if self.__getExploredAllSafeNodes():
                    self.__revert_home = True
        if glitter == True: #Glitter Check
            self.__has_gold = True
            self.__revert_home = True
            self.__move_history.append("GRAB")
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return Agent.Action.GRAB
        elif self.__has_gold == True and self.__x_tile == 1 and self.__y_tile == 1: #ClimbToWin
            self.__move_history.append("CLIMB")
            return Agent.Action.CLIMB
        elif self.__moves == 1 and breeze == True: #FirstMoveCheck
            self.__move_history.append("CLIMB")
            return Agent.Action.CLIMB
        elif self.__moves == 1 and stench == True:
            self.__shot_arrow = True
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return Agent.Action.SHOOT
        elif self.__revert_home == True:
            if len(self.__path_home) == 0:
                self.__path_home = self.__optimal_home_path(self.__x_tile,self.__y_tile,1,1)
                self.__stop_iteration = False
            elif self.__x_tile == 1 and self.__y_tile == 1:
                self.__move_history.append("CLIMB")
                return Agent.Action.CLIMB
            curNode = self.Node(self.__x_tile,self.__y_tile)
            index = 0
            for i in range(len(self.__path_home)):
                if self.__path_home[i] == curNode.getCurrent():
                    index = i
                    break
            try:
                nextNode = self.Node(self.__path_home[i+1][0],self.__path_home[i+1][1])
            except:
                self.__path_home = self.__optimal_home_path(self.__x_tile,self.__y_tile,1,1)
                self.__stop_iteration = False
                curNode = self.Node(self.__x_tile,self.__y_tile)
                index = 0
                for i in range(len(self.__path_home)):
                    if self.__path_home[i] == curNode.getCurrent():
                        index = i
                        break
                nextNode = self.Node(self.__path_home[i+1][0],self.__path_home[i+1][1])
            self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return self.__NodeToNode(nextNode,curNode)
        if self.__dest_node[0] == self.__x_tile and self.__dest_node[1] == self.__y_tile:
            self.__dest_node = (self.__dest_node[0] + (self.__dir_to_coordinate(self.__dir)[0]),
                                self.__dest_node[1] + (self.__dir_to_coordinate(self.__dir)[1]))
            curNode = self.Node(self.__x_tile,self.__y_tile)
            nextNode = self.Node(self.__dest_node[0], self.__dest_node[1])
            # self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return self.__NodeToNode(nextNode,curNode)
        else:
            curNode = self.Node(self.__x_tile,self.__y_tile)
            for i in range(len(self.__dest_path)):
                if self.__dest_path[i] == curNode.getCurrent():
                    index = i
                    break
            nextNode = self.Node(self.__dest_path[index+1][0],self.__dest_path[index+1][1])
            # self.__print_debug_info(stench, breeze, glitter, bump, scream)
            return self.__NodeToNode(nextNode,curNode)


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

    def __NodeToNode(self, potentialNode, CurrentNode):
        xValue = potentialNode.getX() - CurrentNode.getX()
        yValue = potentialNode.getY() - CurrentNode.getY()
        if (xValue,yValue) == (0,1):
            return self.__GoNorth()
        elif (xValue,yValue) == (1,0):
            return self.__GoEast()
        elif (xValue,yValue) == (0,-1):
            return self.__GoSouth()
        elif (xValue,yValue) == (-1,0):
            return self.__GoWest()
        else:
            return self.__GoNorth()
    def __GoNorth(self):
        if self.__dir == 'N':#N
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'E':#E
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':#S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':#W
            self.__dir = 'N'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
    def __GoEast(self):
        if self.__dir == 'N':#N
            self.__dir = 'E'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'E':#E
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'S':#S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':#W
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
    def __GoSouth(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'S'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'S':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
        elif self.__dir == 'W':
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
    def __GoWest(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':
            self.__dir = 'W'
            self.__move_history.append("RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'W':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            return Agent.Action.FORWARD
     

    def __NodeDifference(self,x1,y1,x2,y2):
        node_score = 0
        x_score = 0
        y_score = 0

        x_score = x2-x1
        y_score = y2-y1

        if x_score<0:
            x_score = x_score*-1
        if y_score<0:
            y_score = y_score*-1
        node_score = x_score+y_score
        return node_score
        
    def __dir_to_coordinate(self, direction):
        if direction == 'N':
            return (0,1)
        elif direction == 'E':
            return (1,0)
        elif direction == 'S':
            return (0,-1)
        elif direction == 'W':
            return (-1,0)
        else:
            return (0,1)
    
    def __check_bump(self,bump):
        if(bump==True):
           self.__x_tile -= self.__dir_to_coordinate(self.__dir)[0]
           self.__y_tile -= self.__dir_to_coordinate(self.__dir)[1]
           if self.__dir == 'N':
               self.__yBorder = self.__y_tile
           elif self.__dir == 'E':
               self.__xBorder = self.__x_tile
        


    def __update_history_tiles(self):
        if len(self.__tile_history) == 0:
            self.__tile_history.append((self.__x_tile,self.__y_tile))
        elif self.__tile_history[-1]!=(self.__x_tile,self.__y_tile):
            self.__tile_history.append((self.__x_tile,self.__y_tile))
        if (self.__x_tile,self.__y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((self.__x_tile,self.__y_tile))

