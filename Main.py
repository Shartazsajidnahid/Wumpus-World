

import sys
import os
import math
from World import World

def main ( ):
    world = World(True)
    score = world.run()
    print ("Your agent scored: " + str(score))
        

main()
