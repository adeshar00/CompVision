
movemouse = False

import numpy as np
import cv2
import math
if movemouse:
	import mouse

cap = cv2.VideoCapture(0)

mcount = 0;

resx = 640
resy = 480

tmx = resx/2
tmy = resy/2

drawdata = True # if true, draws dots n stuff around ball

mlastx = 0
mlasty = 0
mlastz = 0
mdown = False
mldown = False
mlactive= False
mdthreshold = 25 # depth at which "click" happens TODO currently arbitrary, have it be configurable
muthreshold = 30 # depth at which "unclick" happens (higher to avoid rapid clicking)
moutthreshold = 40 # mouse provides no input if ball beyond this range
mmaxvel = 1000 # distance (in findball x/y units) at which ball movement plateaus
mvscale = 0.05 # scale by how much to move mouse
mcap = 100 # most units mouse can move in a frame (to prevent big jumps when ball goes seen/unseen)


# Find Ball
#{{{
def findBall(redlist, res):

	# find center
	pi = 3.14159
	
	# find average of all red pixels
	tx = 0;
	ty = 0;
	rl = len(redlist)
	for i in redlist:
		tx+= i[0]
		ty+= i[1]
	if rl>0:
		tx/= rl
		ty/= rl

	# radius of a circle that would cover all pixels, squared
	d = 0
	for i in redlist:
		dx = i[0]-tx
		dy = i[1]-ty
		d+= dx*dx+dy*dy
	d = math.sqrt(4/pi*d*res*res) #xx

	# draw cyan circle with check radius
	if drawdata:
		spots = 32
		ds = math.sqrt(d)
		for i in xrange(spots):
			c = math.cos(float(i)/spots*2*pi)
			s = math.sin(float(i)/spots*2*pi)
			sq = 5
			for a in xrange(sq):
				for b in xrange(sq):
					rx = tx+c*ds+a-sq/2
					ry = ty+s*ds+b-sq/2
					if rx < resy and rx>=0 and ry < resx and ry >=0:
						frame[rx,ry] = [128,255,0]
	

	# find center of pixels that aren't far from center
	newlist = []
	for i in redlist:
		dx = i[0]-tx
		dy = i[1]-ty
		if dx*dx+dy*dy < d:
			newlist.append(i)
			
	# Put red dots over "red" pixels
	if drawdata:
		for i in newlist:
			sq = 2
			x = i[0]
			y = i[1]
			for a in xrange(sq):
				for b in xrange(sq):
					frame[x+a-sq/2,y+b-sq/2] = [0,0,0]

	# render green dot at center of mass (before adjustment)
	if drawdata:
		sq = 10
		for a in xrange(sq):
			for b in xrange(sq):
				frame[tx+a-sq/2,ty+b-sq/2] = [0,255,0]
	
	# compute center of shaved mass of pixels
	tx = 0;
	ty = 0;
	rl = len(newlist)
	for i in newlist:
		tx+= i[0]
		ty+= i[1]
	if rl > 0:
		tx/= rl
		ty/= rl

	# average distance of all pixels from center
	'''
	d = 0
	rl = len(newlist)
	for i in newlist:
		dx = i[0]-tx
		dy = i[1]-ty
		d+= dx*dx+dy*dy
	d/= rl
	'''
		
	# draw red dot at center of ball
	if drawdata:
		sq = 10
		for a in xrange(sq):
			for b in xrange(sq):
				frame[tx+a-sq/2,ty+b-sq/2] = [0,0,255]
			

	# draw yellow circle to outline ball
	sd = math.sqrt(len(newlist)/pi)*res
	if drawdata:
		spots = 32
		for i in xrange(spots):
			c = math.cos(float(i)/spots*2*pi)
			s = math.sin(float(i)/spots*2*pi)
			sq = 2
			for a in xrange(sq):
				for b in xrange(sq):
					rx = tx+c*sd+a-sq/2
					ry = ty+s*sd+b-sq/2
					if rx < resy and rx>=0 and ry < resx and ry >=0:
						frame[rx,ry] = [0,255,255]

	x = 0
	y = 0
	z = 0
	if sd >0:
		z = resx/sd
		x = (ty-resx/2)*z
		y = (tx-resy/2)*z
	
	return [x,y,z]
#}}}


while(True):

	# Capture frame-by-frame
#note: "frame" is a numpy.ndarray, apparently in BGR format
	ret, rframe = cap.read()
	frame = rframe
	frame = frame.swapaxes(0,1)
	frame = frame[::-1]
	frame = frame.swapaxes(0,1)

	
# TODO apparenty frame coordinates are in y,x order instead of x,y order, derp, fix below code so
#  it isn't ass backwards


	
	
	res = 8
	rwall = 16
	gwall = 0
	bwall = 16
	redlist = []
	bluelist = []

	for ii in xrange(0,resy/res-1):
		for jj in xrange(0,resx/res-1):#eventually take average of closest pixels, or over frames
			i = ii*res
			j = jj*res
			p = frame[i,j]
			r = int(p[2])
			g = int(p[1])
			b = int(p[0])
			sq = 1
			if r-g-b > rwall:
				redlist.append((i,j))
				if drawdata:
					for a in xrange(sq):
						for b in xrange(sq):
							frame[i+a-sq/2,j+b-sq/2] = [0,0,255]

	# Get ball vector
	v = findBall(redlist, res)

	temp = False

# Mouse code
#{{{

	if movemouse:
		# Change mouse coords
		if v[2] > 0 and v[2] < moutthreshold:
			if mlactive == True:
				temp = True
				# smooth mouse movement to look like 1-(x-1)^2 curve (plateuas at peak)
				dx = (v[0] - mlastx)
				dy = (v[1] - mlasty)
				dt = math.sqrt(dx*dx+dy*dy)
				if dt > mmaxvel:
					du = 1
				else:
					t = dt/mmaxvel-1
					du = 1-t*t
				dx = dx*du*mvscale
				dy = dy*du*mvscale
				dt = dx*dx+dy*dy
				if dt > mcap*mcap:
					print "CAP HIT",dx,dy
					dt = math.sqrt(dt)
					dx = dx/dt*mcap
					dy = dy/dt*mcap
				tmx+= dx
				tmy+= dy
				mouse.moveby(dx,dy)
				if mldown:
					mdown = v[2] < muthreshold
					if not mdown:
						mouse.leftbuttonup()
						print "UP"
				else:
					mdown = v[2] < mdthreshold
					if mdown:
						mouse.leftbuttondown()
						print "DOWN"
				if v[2] - mlastz > 3:
					print "TEST"
			mlactive = True
			mlastx = v[0]
			mlasty = v[1]
			mlastz = v[2]
			mldown = mdown
		else:
			mlactive = False
			mldown = False
			mouse.leftbuttonup()

		# Bounds tmouse coords to screen
		if tmx < 0:
			tmx = 0
		elif tmx >= resx:
			tmx = resx
		if tmy < 0:
			tmy = 0
		elif tmy >= resy:
			tmy = resy

		if temp:
			if mdown:
				col = 255
			else:
				col = 128
		else:
			col = 0

		sq = 20
		for a in xrange(sq):
			for b in xrange(sq):
				frame[a,b] = [col,col,col]
#}}}


	# Display the resulting frame
#cv2.imshow('rframe',rframe)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
