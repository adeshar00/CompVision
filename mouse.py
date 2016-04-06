import ctypes

mouse = ctypes.CDLL("mouse/libmouse.so")

def moveby(x,y):
	mouse.movemouse(ctypes.c_int(int(x)),ctypes.c_int(int(y)))

def leftbuttondown():
	mouse.mousebuttondown()

def leftbuttonup():
	mouse.mousebuttonup()
