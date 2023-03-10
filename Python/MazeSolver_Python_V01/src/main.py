"""
# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Shea Stanley                                                 #
# 	Created:      2/20/2023, 4:03:26 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
# ABOUT
# This code is designed to solve any given maze, ie one without set conditions. It will utilize an ultrasonic sensor in order to determine its location relative to the nearest barrier, as well as plot obsticles to avoid.
# The robot will achive this goal by identifying the area around itself, and identifying any area that may have a possible gap to drive through (as long as the width of the gap is larger than the width of the vehicle, it will attempt to drive through it)
# The robot will determine possible gaps by scanning a given area, and if a gap between scan points is large enough to fit the robot, it will rescan between those to points to create a higher resolution scan of the area.
# If the robot is given two optons of high resoution to drive to, it will create a decision point node and chose the leftmost path first. If it encounters a dead end or a perminant driving loop, return to the previous node.
# In the case that all directions of a given node are explored, return to the previous node and explore its addtional paths. 
# No goal contition is included as the maze does not have any specifc conditions that would communicate a completed maze.
"""
"""
# Functions to be included
    # Complete | Basic Scan Function
    # This has not been accounted for, as you need to input a starting and end angle, so this answer is not complete. Fix this issue and the function will be complete (for now) | High Resolution scan (could combine with the last one, possibly make the function scan between two given angles)
    # Completed | Basic hole in the wall testing. If the distance between two points is wide enough for a robot to fit, output the coordinates to rescan in between. Make sure to run this function after each scan.
    # In Progress | Note, find a way to identify the locations of these "holes" - DONE | Create wall structure to calculate more difficult holes. If two walls are colinear but have a gap between them to fit a robot, then it's a hole that can be driven through. 
        # If a wall and another scanned point has a gap between eachother at their closest point, and it's wide enough for a robot to fit, then it's a hole that can be driven through.
    # In Progress | Create ideal node that the robot can drive to, and assumes that a possible path to an exit is present. Output the coordinates of this node relative to the starting point.
    # In Progress | Return to Node of given variable
    # In Progress | At distances larger than 200mm, the ultrasonic sensor becomes unreliable. This could lead to bad data, so only plot datapoints that are reliable.

# Possible Optimization
    # Instead of collecting a ton of points via scanning and then calculating if a wall is present, try to calculate if the points are on the same axis, and plot a line for the wall. This can save space and possibly increase performance. 
    # This idea also removes the need of basic hole detection, since the scanning period would be calculating that on the fly.  | Not in testing, maybe in version two?
"""


# drivetrain.drive_for(FORWARD, 3000, MM, wait=True)

# drivetrain.turn_for(RIGHT, 89, DEGREES, wait=True)

#import Vex Library
import sys
import vex
from vex import * 
import math 

# Global Varables. NOTE: ORGANIZE VARIABLES BETWEEN INT AND FLOAT. Interpreted values from sensors can be int, but calculated values should be float.
global a, i, brain, front_distance, vehicleWidth, startingPoint, scanAreaOutput, scanSensorValue, currentPosition, desiredNode, positionNodes, holeFinderInput, dictA, dictB, dictXa, dictYa, dictXb, dictYb, wallLength, wallLengthLarger, coordinateSet, fitCoords, fitCheck, fitArray, fitXa, fitYa, fitXb, fitYb

# Hardwear Config
# This is where you can find all the ports and sensors connected to the robot. Clarify here where each part is connected
# NOTE: MAKE SURE ALL THE ITEMS MATCH THE RIGHT PORTS. FIX IN CLASS TOMORROW.
brain = vex.Brain
motor1 = vex.Motor(vex.Ports.PORT1, vex.GearSetting.RATIO_18_1, False) 
motor2 = vex.Motor(vex.Ports.PORT10, vex.GearSetting.RATIO_18_1, False)
motor3 = vex.Motor(vex.Ports.PORT5, vex.GearSetting.RATIO_18_1, False)
motor4 = vex.Motor(vex.Ports.PORT7, vex.GearSetting.RATIO_18_1, False)
vision_1 = vex.Sonar(vex.Ports.PORT2)
DrivenWheels = vex.DriveTrain(motor1,motor2)

vehicleWidth = 100 #Units in milimeters
startingPoint =[0,0]
currentPosition = [0,0]
front_distance=vision_1

def scanArea(a): #return list of distances from scanning point given a selected angle range to scan
        # This can me optomized. This could help find small 
        
        scanAreaOutput = []
        i = 0
        # Scan a given range and add the variables to an array twenty times
        for i in range(19):
            # Turning and scanning
            DrivenWheels.turn_for(RIGHT, a/20, DEGREES, wait=True)
            scanSensorValue = front_distance.distance(vex.DistanceUnits.MM)
            # Create a dictionary to assign values for easy access. Just clarify what value you want from stating the string (text) associated with each variable
            # Each coorinate is based off off the origin, instead of being relative to the robot
            if(scanSensorValue > 200):
                scannedPoint = {
                "angle": i*(a/20),
                "distance": scanSensorValue,
                "xCoordinate": (((scanSensorValue+150) * math.cos(i*(a/20)) + currentPosition[0])/ 180.0 * math.pi),
                "yCoordinate": (((scanSensorValue+150) * math.sin(i*(a/20)) + currentPosition[1])/ 180.0 * math.pi),
                "reliable": False,
                }
            else:   
                scannedPoint = {
                    "angle": i*(a/20),
                    "distance": scanSensorValue,
                    "xCoordinate": (((scanSensorValue+150) * math.cos(i*(a/20)) + currentPosition[0])/ 180.0 * math.pi),
                    "yCoordinate": (((scanSensorValue+150) * math.sin(i*(a/20)) + currentPosition[1])/ 180.0 * math.pi),
                    "reliable": True,
                }
            # Add the dictionary item to an array for output
            scanAreaOutput.append(scannedPoint)
            # Add to variable until condition is met
            i += 1
        
        # Return the completed array
        return scanAreaOutput

def holeTester(holeFinderInput): #Input array of dictionary inputs
      i = 0
      wallLength = 0 
      wallLengthLarger = []
      coordinateSet = []
      # Take all scanned points
      for i in holeFinderInput.length():
        a_i = 0
        for a_i in holeFinderInput.length():
            dictA=holeFinderInput[i];  
            dictB=holeFinderInput[a_i]
            dictXa= dictA["xCoordinate"]; #scannedPoint["xCoordinate"]
            dictYa= dictA["yCoordinate"]; #scannedPoint["yCoordinate"] 
            dictXb= dictB["xCoordinate"]; #scannedPoint["xCoordinate"]
            dictYb= dictB["yCoordinate"]; #scannedPoint["yCoordinate"]
            # Draw walls for each set of coordinates. This doesn't neccisarily mean that a wall actually exists there, the robot will assume it is. 
            wallLength = (dictXb-dictXa)/(dictYb-dictYa)
            # Take the walls and measure the distance of said wall. If the wall is long enough, add it to an array to rescan. 
            if (wallLength > (vehicleWidth + 100 ) ):
                    # If a point on a wall is too long between two points, output the angles between those two points for rescan.
                    coordinateSet = [1,dictXa,dictYa,dictXb,dictYb]
                    wallLengthLarger.append(coordinateSet)
            else: 
                # If hole finder does not find a hole, return none
                wallLengthLarger.append(None)
            a_i += 1 
        i =+ 1
      
      return wallLengthLarger
      
def nodeCreator():
     i = 0
    # Make triangles from the origin to build walls
      # Somehow find an ideal spot for a node to be
      # Mark its coordinates relative to the origin
      # If the node is in the same region as another node, do not create a new node.
      # If you can avoid adding another item to the array, do so. 

def driveToNode(desiredNode):
     i = 0
      # Take Current Position
      # Find out how many nodes away the desired node is based off current location
      # Plan out a path to each node
      # Drive the path until the robot has reached its destination

def caniFits(fitCoords, mapCoords):
     # Will check to see if the robot can fit within a gap. Check out important notes below
     # Make sure these values are floating point, that's super important
     # Returns an array of boolean values
    i = 0
    canItFit = []

    for i in fitCoords.length():
        if fitCoords(i)!=None:
             fitArray = fitCoords(i)
             if fitArray(0)==1: # After this if statement, determine what system must be used to find holes (Triangle method or Square method)
                fitXa = fitArray(1)
                fitYa = fitArray(2)
                fitXb = fitArray(3)
                fitYb = fitArray(4)
                m = (fitYa-fitYb)/(fitXa-fitXb)
                tanAngle = math.atan(1/m)
                midPointX = ((fitXa-fitXb)/2)+fitXb
                midPointY = ((fitYa-fitYb)/2)+fitYb
                heightAx = vehicleWidth*math.cos(tanAngle)+midPointX
                heightAy = -vehicleWidth*math.sin(tanAngle)+midPointY
                heightBx = -vehicleWidth*math.cos(tanAngle)+midPointX
                heightBy = vehicleWidth*math.sin(tanAngle)+midPointY

                if (abs(tanAngle)==90 or tanAngle==0):
                    # As of right now, no clue how to handle this edge case. This is a crappy way to handle it. 
                    tanAngle += 1
                bA = -((-1/m) * midPointX) + midPointY
                bB = -((m) * heightAx) + heightAy
                bC = -((m) * heightBx) + heightBy
                bD = -((-1/m) * fitXa) + fitYa
                bE = -((-1/m) * fitXb) + fitYb
                a_i = 0
                if(): # if box method is true, run function below (How can I test for this, do I need to?)
                    for a_i in mapCoords.length():
                        itemDict = mapCoords(i)
                        itemCoordsX = itemDict("xCoordinate")
                        itemCoordsY = itemDict("yCoordinate")
                        if(bA > 0 and bC > 0): # bA and bC is positive
                        # functions 27 & 28 on the graphs
                            if (itemCoordsY<=m*itemCoordsX+bC and itemCoordsY>=m*itemCoordsX+bB and itemCoordsY>=(-1/m)*itemCoordsX+bE and itemCoordsY<=(-1/m)*itemCoordsX+bD): # if point is found within bounding area, return false
                                fitAtMidpoint = [False, midPointX, midPointY]
                                canItFit.append(fitAtMidpoint)
                            elif(bA < 0 and bC < 0): # bA and bC is negative
                        # functions 29 & 30 on the graph
                                if (itemCoordsY<=m*itemCoordsX+bB and itemCoordsY>=m*itemCoordsX+bC and itemCoordsY<=(-1/m)*itemCoordsX+bE and itemCoordsY>=(-1/m)*itemCoordsX+bD): # if point is found within bounding area, return false
                                    fitAtMidpoint = [False, midPointX, midPointY]
                                    canItFit.append(fitAtMidpoint)
                            elif(bA < 0 and bC > 0): # bA is negative and bC is positive
                        # functions 31 & 32 on the graph
                                if (itemCoordsY>=m*itemCoordsX+bB and itemCoordsY<=m*itemCoordsX+bC and itemCoordsY<=(-1/m)*itemCoordsX+bE and itemCoordsY>=(-1/m)*itemCoordsX+bD): # if point is found within bounding area, return false
                                    fitAtMidpoint = [False, midPointX, midPointY]
                                    canItFit.append(fitAtMidpoint)
                            elif(bA > 0 and bC < 0): # bA is positive and bC is negative   
                        # functions 33 & 34 on the graph
                                if (itemCoordsY>=m*itemCoordsX+bC and itemCoordsY<=m*itemCoordsX+bB and itemCoordsY<=(-1/m)*itemCoordsX+bE and itemCoordsY>=(-1/m)*itemCoordsX+bD): # if point is found within bounding area, return false
                                    fitAtMidpoint = [False, midPointX, midPointY]
                                    canItFit.append(fitAtMidpoint)
                            else: # if no conditions are met, meaning that there were no points present in the bounding area, return true
                                fitAtMidpoint = [True, midPointX, midPointY]
                                canItFit.append(fitAtMidpoint)
                    a_i =+ 1
                #else: #triangle function, is this needed?
    return canItFit



    #IMPORTANT NOTES
    # Use triangle function found here: https://www.desmos.com/calculator/r60rgtoaid to look for a hole between a barrier and a wall. If you find the shortest point between the barrier and the wall, you've found the width of the hole
    # Test for two points to be colinear if there's no barrier between two points
    # Use these formulas to calculate if there's any obstructions between two points. https://www.desmos.com/calculator/qkmmkabvl7
    # Don't forget to account for if tangent is 90, -90 and 0, as that could cause an error 
    # If you have two holes near you, position yourself directly between them to navigate to them easily. 
    
    # What if there are curves present in the path? Think of a chicane for example, or a hairpin turn. Can the program calculate a path successfully aka without hitting the inside wall (or the Apex) of the corner?
    
def when_started1():
# Brain should be defined by default
    positionNodes = [] #creates a list for collecting position nodes.
#positionNodes.append adds item to the end of the list. 