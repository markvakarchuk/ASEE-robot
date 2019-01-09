# *******************************************************************
# * DUAL MOTOR DRIVER USING A Wii REMOTE CONTROL AND THE GPIO BUS   *
# *******************************************************************
# * This program is designed to control the L298N Dual Full Bridge  *
# * Driver IC, which in turn drives two DC motors.  These could be  *
# * the left and right hand wheels of a small motorised vehicle.    *
# * The L298N has 6 control signals: In1, In2, In3, In4, EnA & EnB. *
# * All of the signals are active high.  See the manufacturers data *
# * sheet for full details of the L298N device.                     *
# *                                                                 *
# * Run the program from a Terminal window (root user).  It will    *
# * not run from within the Python Shell GUI.                       *
# *                                                                 *
# * List of the GPIO pins used:                                     *
# * GPIO25 - Motor 1 (left motor) Enable - EnA - (output - bit 0)   *
# * GPIO24 - Motor 1 (left motor) Forward - In1 -(output - bit 1)   *
# * GPIO23 - Motor 1 (left motor) Reverse - In2 -(output - bit 2)   *
# *                                                                 *
# * GPIO22 - Motor 2 (right motor) Enable - EnB - (output - bit 3)  *
# * GPIO27 - Motor 2 (right motor) Forward - In3 - (output - bit 4) *
# * GPIO18 - Motor 2 (right motor) Reverse - In4 - (output - bit 5) *
# *                                                                 *
# * GPIO17 - Trigger for the ultrasonic sensor (output - bit 6)     *
# *                                                                 *
# * GPIO11 - Spare GPIO output pin (output - bit 7)                 *
# *                                                                 *
# * GPIO10 - Echo input from the ultrasonic sensor (input - bit 8)  *
# *                                                                 *
# * GPIO9  - Spare GPIO Input pin (input - bit 9)                   *
# * GPIO8  - Spare GPIO Input pin (input - bit 10)                  *
# * GPIO7  - Spare GPIO Input pin (input - bit 11)                  *
# *******************************************************************

import RPi.GPIO as GPIO                                                 # Import the GPIO module as 'GPIO'

import cwiid                                                            # Import the Nintendo Wii controller module

import time                                                             # Import the 'time' module

import random

GPIO.setmode (GPIO.BCM)                                                 # Set the GPIO mode to BCM numbering


# *******************************************************************
# *                       DEFINE THE CONSTANTS                      *
# *******************************************************************
# *  IMPORTANT: For a Rev 1 RPi, replace 27 below with 21 instead   *
# *******************************************************************

output_ports = [25, 24, 23, 22, 27, 18, 17, 11]                         # Define the GPIO output port numbers
input_ports = [10, 9, 8, 7]                                             # Define the GPIO input port numbers

m1_en = 1                                                               # Motor 1 Enable (left motor)
m1_fwd = 2                                                              # Motor 1 Forward (left motor)
m1_rev = 4                                                              # Motor 1 Reverse (left motor)
m2_en = 8                                                               # Motor 2 Enable (right motor)
m2_fwd = 16                                                             # Motor 2 Forward (right motor)
m2_rev = 32                                                             # Motor 2 Reverse (right motor)
trig = 17                                                               # Trigger output for the ultrasonic sensor
echo = 10                                                               # Echo return from the ultrasonic sensor

stop = 0                                                                # Drive value for no movement
left = m1_en + m1_rev + m2_en + m2_fwd                                  # Drive value for turning left
right = m1_en + m1_fwd + m2_en + m2_rev                                 # Drive value for turning right
fwd = m1_en + m1_fwd + m2_en + m2_fwd                                   # Drive value for moving forwards
rev = m1_en + m1_rev + m2_en + m2_rev                                   # Drive value for moving backwards
auto = -1                                                               # Drive value for automatic mode


# *******************************************************************
# *      FUNCTION TO DRIVE THE MOTORS USING THE SUPPLIED VALUE      *
# *******************************************************************
# * Although the 'global' command is used, this is simply to allow  *
# * access to the program variables outside the function.  These    *
# * are never altered by any function throughout the entire program *
# * On exit, 'b' contains a 12-bit binary string representing the   *
# * states of the 12 GPIO pins - all eight outputs - 0 to 7 and all *
# * four inputs - 8 to 11                                           *
# *******************************************************************

def motor_drive (value):                                                # Accept the motor drive value
    global input_ports, output_ports                                    # Allow acces to the assigned GPIO ports
    b = bin (value)                                                     # Create a binary string from the supplied value
    b = b [2:len(b)]                                                    # Strip off the '0b' from the start of the string
    b = b.zfill(8)                                                      # Make sure the string is eight bits long

    output_pointer = len (b) -1                                         # Start with the LSB of Binary string
    for port in output_ports:                                           # Pick out the individual GPIO port required
        output_state = int (b[output_pointer])                          # Select whether it needs to be on or off (1 or 0)
        GPIO.output (port,output_state)                                 # Turn on or off the relevant GPIO bit
        output_pointer = output_pointer - 1                             # Move to the next bit in the string
    for port in input_ports:                                            # Get the status of the four input bits
        b = str (GPIO.input (port)) + b                                 # Add the bit values to the Binary string
    return (b)                                                          # Exit with the Binary string in 'b'


# *******************************************************************
# *   FUNCTION TO REVERSE THE CAR TO AVOID OBJECTS IN FRONT OF IT   *
# *******************************************************************
# * If an obstruction is detected in front of the car which is less *
# * than 15cm away, then back away from it to a distance of 20cm.   *
# * This happens irrespective of whether the car is being driven    *
# * manually or autonomously.  To prevent excess current surges and *
# * sudden 'unnatural' reversing, stop the car first, then wait for *
# * half a second before and after backing up                       *
# *******************************************************************

def back_away (direction):
    movement = motor_drive (False)                                      # First of all, stop the car
    time.sleep (0.5)                                                    # Wait for half a second
    distance = get_distance()                                           # Get the current object distance
    while distance < 20:                                                # Whilst it's less than 20cm 
        movement = motor_drive (direction)                              # keep reversing the car
        distance = get_distance ()                                      # and checking the distance
    movement = motor_drive (False)                                      # Otherwise, stop the car,
    time.sleep (0.5)                                                    # wait for half a second,
    return (False)                                                      # then exit with no direction (stop)


# *******************************************************************
# *              FUNCTION TO DRIVE THE CAR AUTONOMOUSLY             *
# *******************************************************************
# * This function is called if the 'A' button, and ONLY the 'A'     *
# * button on the Wii Remote Control is being held down.  The car   *
# * will normally attempt to drive forwards.  If an obstruction is  *
# * detected in front of it then the 'back_away' function is called.*
# * The car will then turn either left or right - depending on a    *
# * random number between 0 and 7.  Between 0 and 3 the the car     *
# * will turn left.  Between 4 and 7 and the car will turn right.   *
# * It will then attempt to continue in a forwards direction        *
# *******************************************************************

def automatic (buttons):
    global stop, left, right, fwd, rev                                  # Allow access to the direction constants

    while (buttons - cwiid.BTN_A == 0):                                 # Run autonomously only while 'A' pressed
        direction = fwd                                                 # Set the initial direction to forwards
        distance = get_distance ()                                      # Check the distance
        if direction == fwd and distance < 15:                          # If the distance is less than 15cm then
            movement = back_away (rev)                                  # reverse the car if driving forward
            direction = right                                           # Set initial turn direction to 'right'
            turn = random.randint (0,7)                                 # Generate a random number between 0 and 7
            if turn < 4:                                                # If the random number is less than 4
                direction = left                                        # then turn left instead
            movement = motor_drive (direction)                          # Now turn in that direction
            time.sleep (0.5)                                            # for half a second
            movement = motor_drive (stop)                               # Then stop for half a second
            time.sleep (0.5)
            
        movement = motor_drive (direction)                              # Continue moving in a forwards direction
        buttons = wii.state['buttons']                                  # Get the button data from the Wii remote

    return ()                                                           # Exit if the 'A' button isn't being pressed
    

# *******************************************************************
# *  FUNCTION TO CALCULATE THE DISTANCE FROM OBSTRUCTIONS IN FRONT  *
# *******************************************************************
# *        THIS USES THE HC-SR04 ULTRASONIC DISTANCE SENSOR         *
# *******************************************************************
# * Unfortunately, the HC-SR04 suffers from some inherent built-in  *
# * flaws, particularly if the reflected sound waves bounce off     *
# * objects at a distance and/or at oblique angles.  This results   *
# * in very erratic signals being generated on the 'Echo' pin.      *
# * Since we're only interested in short distances up to 20cm, we   *
# * need to trap these errors within this function, otherwise the   *
# * program would be very slow to respond to the Wii Remote buttons.*
# * In worst-case situations the program could simply 'hang' whilst *
# * waiting for an echo signal which never ends!  On exit, if a     *
# * valid short distance is calculated, then 'distance' contains    *
# * the value in centimetres.  If a sensor error occurs, then a     *
# * value of 100 is returned instead.                               *
# *******************************************************************

def get_distance ():
    global trig, echo                                                   # Allow access to 'trig' and 'echo' constants

    if GPIO.input (echo):                                               # If the 'Echo' pin is already high
        return (100)                                                    # then exit with 100 (sensor fault)

    distance = 0                                                        # Set initial distance to zero

    GPIO.output (trig,False)                                            # Ensure the 'Trig' pin is low for at
    time.sleep (0.05)                                                   # least 50mS (recommended re-sample time)

    GPIO.output (trig,True)                                             # Turn on the 'Trig' pin for 10uS (ish!)
    dummy_variable = 0                                                  # No need to use the 'time' module here,
    dummy_variable = 0                                                  # a couple of 'dummy' statements will do fine
    
    GPIO.output (trig,False)                                            # Turn off the 'Trig' pin
    time1, time2 = time.time(), time.time()                             # Set inital time values to current time
    
    while not GPIO.input (echo):                                        # Wait for the start of the 'Echo' pulse
        time1 = time.time()                                             # Get the time the 'Echo' pin goes high
        if time1 - time2 > 0.02:                                        # If the 'Echo' pin doesn't go high after 20mS
            distance = 100                                              # then set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
    
    while GPIO.input (echo):                                            # Otherwise, wait for the 'Echo' pin to go low
        time2 = time.time()                                             # Get the time the 'Echo' pin goes low
        if time2 - time1 > 0.02:                                        # If the 'Echo' pin doesn't go low after 20mS
            distance = 100                                              # then ignore it and set 'distance' to 100
            break                                                       # and break out of the loop
        
    if distance == 100:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
        
                                                                        # Sound travels at approximately 2.95uS per mm
                                                                        # and the reflected sound has travelled twice
                                                                        # the distance we need to measure (sound out,
                                                                        # bounced off object, sound returned)
                                                                        
    distance = (time2 - time1) / 0.00000295 / 2 / 10                    # Convert the timer values into centimetres
    return (distance)                                                   # Exit with the distance in centimetres
    

# *******************************************************************
# *              FUNCTION TO EXIT THE PROGRAM CLEANLY               *
# *******************************************************************
# * Use this function to turn off both motor and to ensure the GPIO *
# * ports are reset properly on exit, or if a controllable error    *
# * occurs within the program.  Note: This will not work if CTRL-C  *
# * is used to quit the program prematurely.  In such case, a GPIO  *
# * error message will be displayed when the program is run again.  *
# * However, the program will continue to function as normal        *
# *******************************************************************

def exit_program():
    z = motor_drive (False)                                             # Turn off all the GPIO outputs
    print ("\n\n")                                                      # Print a couple of blank lines
    GPIO.cleanup()                                                      # Clean up the GPIO ports
    exit()                                                              # And quit the program


# *******************************************************************
# *                    START OF THE MAIN PROGRAM                    *
# *******************************************************************

for bit in output_ports:                                                # Set up the six output bits
    GPIO.setup (bit,GPIO.OUT)
    GPIO.output (bit,False)                                             # Initially turn them all off
    
for bit in input_ports:                                                 # Set up the six input bits
    GPIO.setup (bit,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)              # Set the inputs as normally low
    

# *******************************************************************
# * CONNECT TO THE Wii REMOTE CONTROL. QUIT IF IT TIMES OUT 3 TRIES *
# *******************************************************************
# * The Wii Remote Control is connected via a bluetooth adaptor and *
# * by importing the 'cwiid' module.  To connect, press and release *
# * the '1' and '2' buttons simultaneously on the Wii Remote.  The  *
# * program will try to connect up to 3 times.  If it fails the     *
# * program will terminate                                          *
# *******************************************************************

print ("\n\n\n\nPress 1 & 2 together on your Wii Remote now ...")       # Print some instructions

attempt = ['first', 'second', 'last']                                   # Make them a bit informative
word = 0                                                                # Number of attempts to connect
while True:                                                             # Start an infinite loop
    try:
        print ("\n\nTrying to connect for the"), attempt [word],
        print ("time...\n\nAttempt"), word+1                            # Print current attempt
    
        wii=cwiid.Wiimote()                                             # Wait for a response from the Wii remote
        break                                                           # If successful then exit the loop

    except RuntimeError:                                                # If it times out...
        word = word + 1                                                 # Try again
        if word == 3:                                                   # If it fails after 3 attempts...
            print ("\n\nFailed to connect to the Wii remote control")   # Print a failure message
            print ("\nProgram Terminated\n")
            print ("Please restart the program to begin again\n\n")

            terminate = exit_program()                                  # And exit the program


# *******************************************************************
# *        SUCCESSFULLY CONNECTED TO THE Wii REMOTE CONTROL         *
# *******************************************************************

wii.rumble = 1                                                          # Briefly vibrate the Wii remote
time.sleep(0.2)
wii.rumble = 0
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC                            # Report button and accelerometer data

print ("\n\n\n\nThe Wii Remote is now connected...\n")                  # Print a few instructions
print ("Use the direction pad to steer the car\n")
print ("or...\n")
print ("Hold the 'B' button and tilt the Wii Remote to steer\n")
print ("or...\n")
print ("Press and hold down the 'A' button for Autonomous Mode\n")
print ("Press '+' and '-' buttons at the same time quit.\n")

while True:                                                             # Begin an infinite loop
    direction = stop                                                    # Set the initial direction to none (stop)
    buttons = wii.state['buttons']                                      # Get the button data from the Wii remote
    x, y, z = wii.state['acc']                                          # Also get the accelerometer data
    if not (buttons & cwiid.BTN_B):                                     # Only use accelerometer data if
        x, y, z = 125, 125, 125                                         # the 'B' button is being pressed

    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):               # Are both the '+' and '-' buttons pressed?
        print ("\nThe Wii Remote connection has been closed\n")
        print ("Please restart the program to begin again\n")           # Yes - Print a message
        wii.rumble = 1                                                  # Briefly vibrate the Wii remote
        time.sleep(0.2)
        wii.rumble = 0
        terminate = exit_program()                                      # And quit the program

    if (buttons - cwiid.BTN_A == 0):                                    # If ONLY the 'A' button is pressed
        movement = automatic (buttons)                                  # then run autonomously

# *******************************************************************
# * Using the data from the Wii Remote Control, check which buttons *
# * are pressed using a bitwise AND of the buttons bit value and    *
# * the predefined 'cwiid' constant for each button.  If more than  *
# * one button is pressed, only the last one in the sequence 'left',*
# * 'right', 'up' or 'down' will be selected.  It has to be done    *
# * this way because the L298N controller cannot drive the motors   *
# * in two directions at the same time - eg: forwards and left      *
# *******************************************************************

    if (buttons & cwiid.BTN_LEFT) or x < 110:
        direction = left                                                # Prepare to turn the car to the left

    if(buttons & cwiid.BTN_RIGHT) or x > 130:
        direction = right                                               # Prepare to turn the car to the right

    if (buttons & cwiid.BTN_UP) or y > 130:
        direction = fwd                                                 # Prepare to drive the car forwards
    
    if (buttons & cwiid.BTN_DOWN) or y < 110:
        direction = rev                                                 # Prepare to drive the car backwards

    distance = get_distance ()                                          # Get object distance in centimetres

    if direction == fwd and distance < 15:                              # If the distance is less than 15cm then
        direction = back_away (rev)                                     # reverse the car if driving forward

    movement = motor_drive (direction)                                  # Otherwise get the car moving (if needs be)

