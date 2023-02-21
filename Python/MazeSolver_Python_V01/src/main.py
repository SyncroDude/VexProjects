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

# Functions to be included
# Scan Function DONE
# High Resolution scan (could combine with the last one, possibly make the function scan between two given angles) Nearly Done
# Create wall structure using datapoints to calculate possible holes in walls. If an area needs higher resolution, rescan that specific area and recreate the calculation to include said area. Make sure to run this function after each scan. In progress
# Create ideal node that the robot can drive to, and assumes that a possible path to an exit is present. Output the coordinates of this node relative to the starting point. In Progress
# Return to Node of given variable In Progress

# drivetrain.drive_for(FORWARD, 3000, MM, wait=True)

# drivetrain.turn_for(RIGHT, 89, DEGREES, wait=True)

#import Vex Library
from vex import *

# Global Varables
global a,i,vehicleWidth,startingPoint,scanAreaOutput,scanSensorValue,currentPosition,desiredNode,positionNodes

vehicleWidth = 100 #Units in milimeters
startingPoint =[0,0]

def scanArea(a): #return list of distances from scanning point given a selected angle range to scan
        i = 0
        
        scanAreaOutput = []
        # Scan a given range and add the variables to an array twenty times
        for i-1 in range(19){
            # Turning and scanning
            DriveTrain.turn_for(RIGHT, a/20, DEGREES, wait=True)
            scanSensorValue = front_distance.get_distance(MM)
            # Create a dictionary to assign values for easy access. Just clarify what value you want from stating the string (text) associated with each variable
            # FIX X AND Y COORDINATES TO BE BASED OFF ORIGIN NOT BASED OFF CURRENT POSITION
            scannedPoint = {
                "angle": i*(a/20),
                "distance": scanSensorValue,
                "xCoordinate": (front_distance.get_distance(MM)+150) * math.cos(i*(a/20)/ 180.0 * math.pi),
                "yCoordinate": (front_distance.get_distance(MM)+150) * math.sin(i*(a/20)/ 180.0 * math.pi),
            }
        # Add the dictionary item to an array for output
        append.scanAreaOutput(scannedPoint)
        # Add to variable until condition is met
        i=i++
        }
        # Return the completed array
        return scanAreaOutput

def holeFinder():
      # Take all scanned points
      # Create virtual walls between each point. This doesn't neccisarily mean that a wall actually exists there, the robot will assume it is. 
      # The lines must be built consecutively or else this won't make sense. Walls must be created from point 0 to 1, 1 to 2, 2 to 3, ect.
      # If a point on a wall is too long between two points, output the angles between those two points for rescan.
      # If hole finder does not find a hole, return none

def nodeCreator():
      # Somehow find an ideal spot for a node to be
      # Mark its coordinates relative to the origin

def driveToNode(desiredNode):
      # Take Current Position
      # Find out how many nodes away the desired node is based off current location
      # Plan out a path to each node
      # Drive the path until the robot has reached its destination

    
def when_started1():
# Brain should be defined by default
    positionNodes = [] #creates a list for collecting position nodes.
#positionNodes.append adds item to the end of the list. 


        
