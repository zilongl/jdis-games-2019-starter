# MyBot.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import random
from pacman.game import Directions
import pacman.util as util # Free utility functions like Stack or Queue ! 
from pacman.capture import GameState
from pacman.captureAgents import CaptureAgent

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers. isRed is True if the red team is being created, and
    will be False if the blue team is being created.
    """

    # The following line is an example only; feel free to change it.

    return [AgentOne(firstIndex), AgentOne(secondIndex)]

##########
# Agents #
##########

class AgentOne(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState: GameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 5 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

        '''
        Your initialization code goes here, if you need any.
        '''
        self.reverseRed = False
        self.reverseBlue = False

    def intersection(self, lst1, lst2): 
        lst3 = [value for value in lst1 if value in lst2] 
        return lst3 

    def nbFoodAvailable(self, foodList):
        count = 0
        for row in foodList:
            for elem in row:
                if elem == True:
                    count += 1
        return count

    def chooseAction(self, gameState: GameState) -> str:
        """
        Picks among legal actions randomly.
        """
        actions = gameState.getLegalActions(self.index)
        #print(gameState.isOnRedTeam(self.index))
        redActions = ["East", "Jump_East", "Stop", "FROZEN", "South", "Jump_South"]
        blueActions = ["West", "Jump_West", "Stop", "FROZEN", "North", "Jump_North"]
    
        previousState = self.getPreviousObservation()
        currentState = self.getCurrentObservation()

        if gameState.isOnRedTeam(self.index):
            if previousState:
                print(self.nbFoodAvailable(previousState.getBlueFood()), self.nbFoodAvailable(currentState.getBlueFood()))
            if previousState and self.nbFoodAvailable(previousState.getBlueFood()) != self.nbFoodAvailable(currentState.getBlueFood()):
                print(self.nbFoodAvailable(previousState.getBlueFood()), self.nbFoodAvailable(currentState.getBlueFood()))
                self.reverseRed = True
            
            if self.reverseRed:
                possiblesActions = self.intersection(blueActions,actions)    
            else:
                possiblesActions = self.intersection(redActions,actions)   
        else:
            if previousState and self.nbFoodAvailable(previousState.getRedFood()) != self.nbFoodAvailable(currentState.getRedFood()):
                self.reverseBlue = True
            
            if self.reverseBlue:
                possiblesActions = self.intersection(redActions,actions)    
            else:
                possiblesActions = self.intersection(blueActions,actions)

        print(possiblesActions)
        return random.choice(possiblesActions)


class AgentTwo(CaptureAgent):
    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
    
    def chooseAction(self, gameState: GameState) -> str:

        gameState.getAgentDistances()

        actions = gameState.getLegalActions(self.index)

        return random.choice(actions)
