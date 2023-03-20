import pygame

pygame.init()

# Set up the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# ok, so on an xbox one controller, axis 5 is right trigger.
#axis 6 is left trigger.

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYAXISMOTION:
#                 #trigger_value = joystick.get_axis(5)
#                 #print("Right trigger value: ", trigger_value)
#                 #trigger_value2 = joystick.get_axis(4)
#                 #print("Left trigger value: ", trigger_value2)
#
#                 left_stick = joystick.get_axis(1)
#                 left_stick_x_norm = (left_stick + 1) / 2
#                 print("Left stick value: ", left_stick_x_norm)

while True:
    for event in pygame.event.get():  #left axis 
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0: # Left joystick x-axis
                left_stick_x_norm = -1 * joystick.get_axis(0)
                print("Left joystick x-axis value:", left_stick_x_norm)