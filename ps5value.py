# import pygame
# import pygame

# pygame.init()
# pygame.joystick.init()

# joystick = pygame.joystick.Joystick(0)
# joystick.init()

# def get_inputs():
#     pygame.event.pump()
#     axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
#     buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
#     return axes, buttons

import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No controller detected")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("✅ Controller detected:", joystick.get_name())
print("Start interacting with controller...\n")

while True:
    for event in pygame.event.get():

        # Axis movement (sticks/triggers)
        if event.type == pygame.JOYAXISMOTION:
            value = round(event.value, 2)

            # Ignore tiny noise
            if abs(value) > 0.05:
                axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]
                buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

                print("Axes:", axes)
                print("Buttons:", buttons)
                print("-" * 40)

        # Button press
        elif event.type == pygame.JOYBUTTONDOWN:
            axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]
            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

            print("Axes:", axes)
            print("Buttons:", buttons)
            print("-" * 40)

        # Button release
        elif event.type == pygame.JOYBUTTONUP:
            axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]
            buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

            print("Axes:", axes)
            print("Buttons:", buttons)
            print("-" * 40)