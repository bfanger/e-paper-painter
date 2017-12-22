# pylint-disable: uppercase
"""Send images to the e-paper screen"""
from sys import argv, stderr
from epd2in13b import EPD
import Image

if len(argv) < 3:
    stderr.write("Not enough parameters.\n")
    exit(1)
print("Rendering to display...\n")
display = EPD()
display.init()

# display image
BLACK = display.get_frame_buffer(Image.open(argv[1]))
RED = display.get_frame_buffer(Image.open(argv[1]))
display.display_frame(BLACK, RED)

display.sleep()

print("Done.\n")
