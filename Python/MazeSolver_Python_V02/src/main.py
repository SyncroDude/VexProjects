#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration
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
      if(sensingDistance > 100):
          drivingDistance = 0
          while(range_finder_a.distance(MM) > 100):
            drivetrain.drive_for(FORWARD, 10)
            brain.screen.print(range_finder_a.distance(MM))
            brain.screen.print(" ,")
            brain.screen.print(drivingDistance)
            brain.screen.next_row()
            drivingDistance = drivingDistance + 10
            if (drivingDistance >= 70):
                drivetrain.turn_for(RIGHT, 90, DEGREES)
                optionA = range_finder_a.distance(MM)
                brain.screen.print(optionA)
                brain.screen.next_row()
                drivetrain.turn_for(LEFT, 180, DEGREES)
                optionB = range_finder_a.distance(MM)
                brain.screen.print(optionB)
                brain.screen.next_row()
                drivetrain.turn_for(RIGHT, 90, DEGREES)
                if (optionA>0 and optionB>0):
                    brain.screen.print("Centering Function!")
                    brain.screen.next_row()
                    centering = (50+optionA+optionB)/2
                    brain.screen.print(centering)
                    brain.screen.next_row()
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, centering-optionA, MM)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivingDistance = int(000)
                    brain.screen.clear_screen()
                    brain.screen.set_cursor(1,1)
                    brain.screen.print("DISTANCE VALUE = ")
                    brain.screen.print(drivingDistance)
                    brain.screen.next_row()


      else:
          drivetrain.stop()
          # Append driving distance to the totalTravel array
          addItem = [0,drivingDistance]
          brain.screen.print("Array Items: ")
          brain.screen.print(addItem[0])
          brain.screen.print(",")
          brain.screen.print(addItem[0])
          brain.screen.next_row()
          totalTravel.append(addItem)
          addItem.clear()
          brain.screen.print("Option Testing")
          brain.screen.next_row()
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
              TravelLength = len(totalTravel)
              brain.screen.print("Array Length: ")
              brain.screen.print(TravelLength)
              brain.screen.next_row()
              while (TravelLength > 0):
                TravelItem = totalTravel[TravelLength-1]
                brain.screen.print("Array Length: ")
                brain.screen.print(len(TravelItem))
                brain.screen.next_row()
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
