#About

This is a simple computer-vision program that takes feed from a webcam, and draws a circle on the video around a red ball (assuming that a red ball is being held in front of the camera).  It uses OpenCV to get the webcam feed, but the parts that find the ball and highlight it are written from scratch.

I also began playing with using the red ball to control the mouse cursor on the screen (moving the ball close enough to the screen would count as a click), and got a very crude prototype working.  It felt pretty awkward to use though, so I didn't pursue it any further (if you're on Linux, you can test it out by building the source in the "mouse" directory, and then changing the first line of main.py from "mousemove = False" to "mousemove = True").


#Dependencies

OpenCV and Numpy.  On Debian systems they can be installed with the following commands:

'''
sudo apt-get install python-numpy
sudo apt-get install python-opencv
'''


#How it works

The algorithm finds the center of mass of all the red pixels (those with RGB values that are tucked so far into the red corner of the color cube), then considers the red pixels near the center of mass (to mitigate the influence of noise) and finds *their* center of mass (which is considered to be the true center of the ball at this point), and then determines the radius by considering the number of red pixels near the center of mass (if you consider a pixel to be a unit of area, and the area of a circle is equal to `PI*(radius^2)`, then the radius in pixels will be `sqrt((pixelcount)/PI)` )
