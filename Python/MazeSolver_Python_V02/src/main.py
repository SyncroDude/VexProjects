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

# Brain should be defined by default
# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
drivetrain_inertial = Inertial(Ports.PORT5)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
range_finder_a = Sonar(brain.three_wire_port.a)

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

def when_started1():
    global sensingDistance, drivingDistance, totalTravel, TravelLength,
    drivingDistance = 0
    totalTravel = [] # For the totalTravel array, 0 means driving, 1 means turning (negative value represents turning left, while a positive value representss turing right), 2 means decision point
    while (True == True):
      sensingDistance = range_finder_a.distance(MM)
      drivingDistance = 0
      if(sensingDistance > 50):
          drivetrain.drive(FORWARD)
          drivingDistance += 1
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
          if(optionA>50 & optionB>50):
              drivetrain.turn_for(RIGHT, 90, DEGREES)
              addItem = [2,90]
              totalTravel.append(addItem)
              addItem.clear()
          elif(optionA>50):
              drivetrain.turn_for(RIGHT, 90, DEGREES)
              addItem = [1,90]
              totalTravel.append(addItem)
              addItem.clear()
          elif(optionB>50):
              drivetrain.turn_for(LEFT, 90, DEGREES)
              addItem = [1,-90]
              totalTravel.append(addItem)
              addItem.clear()
          else: #turn around and return to last decision point
              TravelLength = totalTravel.count()
              while (TravelLength != -1):
                TravelItem = totalTravel(TravelLength)
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
    if (brain.screen.pressed(callback) == True):
        brain.screen.print("Stopping Program")
        wait(3, SECONDS)
        stop_project()

when_started1() 