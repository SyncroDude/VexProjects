# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       shea                                                         #
# 	Created:      3/2/2023, 12:51:13 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Brain should be defined by default
# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain_inertial = Inertial(Ports.PORT5)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
range_finder_a = Sonar(brain.three_wire_port.a)
motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

def midpointDetectAndDrive():
    # turn to the leftmost heading, then turn from the left until sensed distance is greater than 100. Once achiived, turn to the rightmost heading and do the same.
    # Take the two distances collected, give them coodrdinates based on your current location (0,0), then interpret output coodrinates so the robot drives to the midpoint of that line.
    # Version one, drive to the coordinates using components (easy)
    # Version two, drive to the coodinates by taking the shortest path (harder, with more hurtles to overcome. How do I know the previous heading?)
    
    brain.screen.print("Collecting Data for midpoint scan")
    brain.screen.next_row() 
    initialHeading = drivetrain.heading(DEGREES)
    distanceThreshold = 195
    pointA  = 1
    pointB = 1
    angleA  = 1
    angleB = 1

    
    # Scan for the two positions

    drivetrain.turn_for(RIGHT, 45)
    pointA = range_finder_a.distance(MM)
    angleA = drivetrain.heading(DEGREES)
    if (pointA >= distanceThreshold < 350): 
        brain.screen.print("A Wall has been Detected!")
        brain.screen.next_row() 
        
    else: 
        brain.screen.print("No wall detected!")
        brain.screen.next_row()
    drivetrain.turn_to_heading(initialHeading)
    drivetrain.turn_for(LEFT, 45)
    pointB = range_finder_a.distance(MM)
    angleB = drivetrain.heading(DEGREES)
    if (pointB >= distanceThreshold < 350): 
        brain.screen.print("A Wall has been Detected!")
        brain.screen.next_row() 
    else: 
        brain.screen.print("No wall detected!")
        brain.screen.next_row()
    
    # Calculate the coodinates from the scanned points
    pointAx = ((pointA) * math.cos(angleA)) 
    pointAy = ((pointA) * math.sin(angleA))
    pointBx = ((pointB) * math.cos(angleB))
    pointBy = ((pointB) * math.sin(angleB))
    midPointX = ((pointAx-pointBx)/2)+pointBx
    midPointY = ((pointAy-pointBy)/2)+pointBy

    # Drive to the midppint
    drivetrain.turn_to_heading (initialHeading+90)
    drivetrain.drive_for(FORWARD, midPointX)
    drivetrain.turn_to_heading (initialHeading)
    drivetrain.drive_for(FORWARD, midPointY)



def when_started1():
    global sensingDistance, drivingDistance, totalTravel, TravelLength
    drivingDistance = 0
    totalTravel = [] # For the totalTravel array, 0 means driving, 1 means turning (negative value represents turning left, while a positive value representss turing right), 2 means decision point
    motor_8.spin_for(REVERSE, 10, DEGREES)
    while (True == True):
      sensingDistance = range_finder_a.distance(MM)
      brain.screen.print(sensingDistance)
      brain.screen.next_row()
      drivingDistance = 0
      if(sensingDistance > 150 or drivingDistance > 200):
          midpointDetectAndDrive()
      else:
          drivetrain.stop()
          # Append driving distance to the totalTravel array
          addItem = [0,drivingDistance]
          totalTravel.append(addItem)
          addItem.clear()
          drivetrain.turn_for(RIGHT, 90, DEGREES)
          optionA = range_finder_a.distance(MM)
          drivetrain.turn_for(LEFT, 180, DEGREES)
          optionB = range_finder_a.distance(MM)
          drivetrain.turn_for(RIGHT, 90, DEGREES)
          if(optionA>150 and optionB>150):
              drivetrain.turn_for(RIGHT, 90, DEGREES)
              addItem = [2,90]
              totalTravel.append(addItem)
              addItem.clear()
          elif(optionA>150):
              drivetrain.turn_for(RIGHT, 90, DEGREES)
              addItem = [1,90]
              totalTravel.append(addItem)
              addItem.clear()
          elif(optionB>150):
              drivetrain.turn_for(LEFT, 90, DEGREES)
              addItem = [1,-90]
              totalTravel.append(addItem)
              addItem.clear()
          else: #turn around and return to last decision point
              TravelLength = totalTravel.count
              while (TravelLength != -1):
                TravelItem = totalTravel[TravelLength]
                TravelIdentifier = TravelItem [0]
                TravelValue = [1]
                if (TravelIdentifier == 0 ):
                    drivetrain.drive_for(REVERSE, TravelValue)
                    TravelLength =- 1
                elif (TravelIdentifier == 1):
                    drivetrain.turn_for(RIGHT, -1 * TravelItem)
                    TravelLength =- 1
                elif (TravelIdentifier == 2):
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    addItem = [1,-90]
                    totalTravel.insert(TravelLength, addItem)
                    totalTravel.pop(TravelLength+1)
                    addItem.clear
                    break

when_started1() 
