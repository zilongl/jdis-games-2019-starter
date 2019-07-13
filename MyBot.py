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
import sys

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

    return [AgentOne(firstIndex), AgentTwo(secondIndex)]

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
        self.finishQuarter = False
        self.goingEndgame = False

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
    
    def transformAllFoodToPositions(self, foodList):
        allFoodPositions = []
        for i, row in enumerate(foodList):
            for  j, value in enumerate(row):
                if value == True:
                    allFoodPositions.append((i,j))
        return allFoodPositions
        
    def transformAllEmptyPositions(self, walls):
        allEmptyPositions = []
        for i, row in enumerate(walls):
            for  j, value in enumerate(row):
                if value == False:
                    allEmptyPositions.append((i,j))
        return allEmptyPositions

    def closestCenterCase(self, isRed, currentPosition, gameState, walls):
        allEmptyPositions = self.transformAllEmptyPositions(walls)
        centerEmptyCases = [x for x in allEmptyPositions if x[0] == 16] if isRed else [x for x in allEmptyPositions if x[0] == 17] 
        
        closestEmptyDistance = sys.maxsize
        closestEmptyPosition = (1,1) if gameState.isOnRedTeam(self.index) else (32,15)
        for pos in centerEmptyCases:
            dist = self.getMazeDistance(gameState.getAgentPosition(self.index), pos)
            if dist < closestEmptyDistance:
                closestEmptyDistance = dist
                closestEmptyPosition = pos
        return closestEmptyPosition

    def isBotInCenter(self, isRed, currentPosition):
        return currentPosition[0] == 17 if isRed else currentPosition[0] == 16

    def closestFood(self, foodList, gameState, capsulesPositions):
        allFoodPositions = self.transformAllFoodToPositions(foodList)
        allFoodPositions += capsulesPositions
        closestFoodDistance = sys.maxsize
        closestFoodPosition = (1,1) if gameState.isOnRedTeam(self.index) else (32,15)

        allFoodPositions = [x for x in allFoodPositions if x[1] <= 7]

        if not self.finishQuarter:
            allFoodPositions = [x for x in allFoodPositions if x[0] <= 24] if gameState.isOnRedTeam(self.index) else [x for x in allFoodPositions if x[0] >= 8]
        
        if len(allFoodPositions) == 0 and not self.finishQuarter and not self.goingEndgame:
            closestFoodPosition = self.closestCenterCase(gameState.isOnRedTeam(self.index), gameState.getAgentPosition(self.index), gameState, gameState.getWalls())
        
        if len(allFoodPositions) == 0 and self.isBotInCenter(gameState.isOnRedTeam(self.index),gameState.getAgentPosition(self.index)):
            self.finishQuarter = True 
            self.goingEndgame = True
        
        
        for pos in allFoodPositions:
            dist = self.getMazeDistance(gameState.getAgentPosition(self.index), pos)
            if dist < closestFoodDistance:
                closestFoodDistance = dist
                closestFoodPosition = pos
        return closestFoodPosition
                
    def strategyBasic(self, gameState):
        """
        Picks among legal actions randomly.
        """
        actions = gameState.getLegalActions(self.index)
        #print(gameState.isOnRedTeam(self.index))
        redActions = ["East", "Jump_East", "Stop", "FROZEN", "South", "Jump_South"]
        blueActions = ["West", "Jump_West", "Stop", "FROZEN", "North", "Jump_North"]
    
        previousState = self.getPreviousObservation()
        currentState = self.getCurrentObservation()

        print(self.index, gameState.getAgentPosition(self.index), self.closestFood(self.getFood(gameState), gameState))

        if gameState.isOnRedTeam(self.index):
            if previousState:
                print(self.nbFoodAvailable(previousState.getBlueFood()), self.nbFoodAvailable(currentState.getBlueFood()))
            if previousState and self.nbFoodAvailable(previousState.getBlueFood()) != self.nbFoodAvailable(currentState.getBlueFood()):
                print(self.nbFoodAvailable(previousState.getBlueFood()), self.nbFoodAvailable(currentState.getBlueFood()))
                self.reverseRed = True

            if previousState and self.getScore(previousState) < self.getScore(currentState):
                self.reverseRed = False
            
            if self.reverseRed:
                possiblesActions = self.intersection(blueActions,actions)    
            else:
                possiblesActions = self.intersection(redActions,actions)   
        else:
            if previousState and self.nbFoodAvailable(previousState.getRedFood()) != self.nbFoodAvailable(currentState.getRedFood()):
                self.reverseBlue = True

            if previousState and self.getScore(previousState) < self.getScore(currentState):
                self.reverseBlue = False
            
            if self.reverseBlue:
                possiblesActions = self.intersection(redActions,actions)    
            else:
                possiblesActions = self.intersection(blueActions,actions)

        print(possiblesActions)
        if len(possiblesActions) == 1 and possiblesActions[0] == "Stop":
            return random.choice(self.intersection(actions, ["South","North","Stop"]))
        return random.choice(possiblesActions)

    def addPositions(self, pos1, pos2):
        return (pos1[0]+pos2[0], pos1[1]+pos2[1])

    def getBestActionToFood(self, closestFoodPosition, currentAgentPosition, possibleActions):
        cardinalToPositionChange = {
            "North": (0, 1),
            "Jump_North": (0, 2),
            "West": (-1, 0),
            "Jump_West": (-2, 0),
            "East": (1, 0),
            "Jump_East": (2, 0),
            "South": (0, -1),
            "Jump_South": (0, -2),
            "FROZEN": (0, 0),
            "FREEZE": (0, 0),
            "Stop": (0, 0)
        }

        bestAgentDistanceToFood = sys.maxsize
        bestAgentMove = random.choice(possibleActions)
        for action in possibleActions:
            newAgentPosition = self.addPositions(currentAgentPosition, cardinalToPositionChange[action])
            #print(action, currentAgentPosition, newAgentPosition)
            newAgentDistanceToFood = self.getMazeDistance(newAgentPosition, closestFoodPosition)

            if newAgentDistanceToFood < bestAgentDistanceToFood:
                bestAgentDistanceToFood = newAgentDistanceToFood
                bestAgentMove = action

        return bestAgentMove

    def getAvailableCapsules(self, capsules, isRed):
        if isRed:
            return [pos for pos in capsules if pos[0] > 15]
        else:
            return [pos for pos in capsules if pos[0] < 15]

    def strategyClosestFood(self, gameState):
        capsulesPositions = self.getAvailableCapsules(gameState.getCapsules(), gameState.isOnRedTeam(self.index))

        closestFoodPosition = self.closestFood(self.getFood(gameState), gameState, capsulesPositions)
        currentAgentPosition = gameState.getAgentPosition(self.index)
        possibleActions = gameState.getLegalActions(self.index)

        return self.getBestActionToFood(closestFoodPosition, currentAgentPosition, possibleActions)

    def chooseAction(self, gameState: GameState) -> str:
        return self.strategyClosestFood(gameState)


class AgentTwo(CaptureAgent):
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
        self.finishQuarter = False
        self.goingEndgame = False

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
    
    def transformAllFoodToPositions(self, foodList):
        allFoodPositions = []
        for i, row in enumerate(foodList):
            for  j, value in enumerate(row):
                if value == True:
                    allFoodPositions.append((i,j))
        return allFoodPositions
    
    def transformAllEmptyPositions(self, walls):
        allEmptyPositions = []
        for i, row in enumerate(walls):
            for  j, value in enumerate(row):
                if value == False:
                    allEmptyPositions.append((i,j))
        return allEmptyPositions

    def closestCenterCase(self, isRed, currentPosition, gameState, walls):
        allEmptyPositions = self.transformAllEmptyPositions(walls)
        centerEmptyCases = [x for x in allEmptyPositions if x[0] == 16] if isRed else [x for x in allEmptyPositions if x[0] == 17] 
        
        closestEmptyDistance = sys.maxsize
        closestEmptyPosition = (1,1) if gameState.isOnRedTeam(self.index) else (32,15)
        for pos in centerEmptyCases:
            dist = self.getMazeDistance(gameState.getAgentPosition(self.index), pos)
            if dist < closestEmptyDistance:
                closestEmptyDistance = dist
                closestEmptyPosition = pos
        return closestEmptyPosition

    def isBotInCenter(self, isRed, currentPosition):
        return currentPosition[0] == 17 if isRed else currentPosition[0] == 16

    def closestFood(self, foodList, gameState, capsulesPositions):
        allFoodPositions = self.transformAllFoodToPositions(foodList)
        allFoodPositions += capsulesPositions
        closestFoodDistance = sys.maxsize
        closestFoodPosition = (1,1) if gameState.isOnRedTeam(self.index) else (32,15)

        allFoodPositions = [x for x in allFoodPositions if x[1] > 7]

        if not self.finishQuarter:
            allFoodPositions = [x for x in allFoodPositions if x[0] <= 24] if gameState.isOnRedTeam(self.index) else [x for x in allFoodPositions if x[0] >= 8]
        
        if len(allFoodPositions) == 0 and not self.finishQuarter and not self.goingEndgame:
            closestFoodPosition = self.closestCenterCase(gameState.isOnRedTeam(self.index), gameState.getAgentPosition(self.index), gameState, gameState.getWalls())
        
        if len(allFoodPositions) == 0 and self.isBotInCenter(gameState.isOnRedTeam(self.index),gameState.getAgentPosition(self.index)):
            self.finishQuarter = True 
            self.goingEndgame = True
        
        
        for pos in allFoodPositions:
            dist = self.getMazeDistance(gameState.getAgentPosition(self.index), pos)
            if dist < closestFoodDistance:
                closestFoodDistance = dist
                closestFoodPosition = pos
        return closestFoodPosition

    def addPositions(self, pos1, pos2):
        return (pos1[0]+pos2[0], pos1[1]+pos2[1])

    def getBestActionToFood(self, closestFoodPosition, currentAgentPosition, possibleActions):
        cardinalToPositionChange = {
            "North": (0, 1),
            "Jump_North": (0, 2),
            "West": (-1, 0),
            "Jump_West": (-2, 0),
            "East": (1, 0),
            "Jump_East": (2, 0),
            "South": (0, -1),
            "Jump_South": (0, -2),
            "FROZEN": (0, 0),
            "FREEZE": (0, 0),
            "Stop": (0, 0)
        }

        bestAgentDistanceToFood = sys.maxsize
        bestAgentMove = random.choice(possibleActions)
        for action in possibleActions:
            newAgentPosition = self.addPositions(currentAgentPosition, cardinalToPositionChange[action])
            #print(action, currentAgentPosition, newAgentPosition)
            newAgentDistanceToFood = self.getMazeDistance(newAgentPosition, closestFoodPosition)

            if newAgentDistanceToFood < bestAgentDistanceToFood:
                bestAgentDistanceToFood = newAgentDistanceToFood
                bestAgentMove = action

        return bestAgentMove

    def getAvailableCapsules(self, capsules, isRed):
        if isRed:
            return [pos for pos in capsules if pos[0] > 15]
        else:
            return [pos for pos in capsules if pos[0] < 15]

    def strategyClosestFood(self, gameState):
        capsulesPositions = self.getAvailableCapsules(gameState.getCapsules(), gameState.isOnRedTeam(self.index))

        closestFoodPosition = self.closestFood(self.getFood(gameState), gameState, capsulesPositions)
        currentAgentPosition = gameState.getAgentPosition(self.index)
        possibleActions = gameState.getLegalActions(self.index)

        return self.getBestActionToFood(closestFoodPosition, currentAgentPosition, possibleActions)

    def chooseAction(self, gameState: GameState) -> str:
        return self.strategyClosestFood(gameState)