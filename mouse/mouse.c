#include <X11/Xlib.h>
#include <X11/Xutil.h>

void movemouse(int x, int y)
{
	Display* d = XOpenDisplay(0);

	if(d)
	{
		XWarpPointer(d,0,0,0,0,0,0,x,y);
	}

	XCloseDisplay(d);
}

void mousebuttondown()
{
	// source: http://www.linuxquestions.org/questions/programming-9/simulating-a-mouse-click-594576/
	Display *display = XOpenDisplay(NULL);

	XEvent event;
	
	if(display == NULL)
	{
		return;
	}
	
	memset(&event, 0x00, sizeof(event));
	
	event.type = ButtonPress;
	event.xbutton.button = Button1;
	event.xbutton.same_screen = True;
	
	XQueryPointer(display, RootWindow(display, DefaultScreen(display)), &event.xbutton.root, &event.xbutton.window, &event.xbutton.x_root, &event.xbutton.y_root, &event.xbutton.x, &event.xbutton.y, &event.xbutton.state);
	
	event.xbutton.subwindow = event.xbutton.window;
	
	while(event.xbutton.subwindow)
	{
		event.xbutton.window = event.xbutton.subwindow;
		
		XQueryPointer(display, event.xbutton.window, &event.xbutton.root, &event.xbutton.subwindow, &event.xbutton.x_root, &event.xbutton.y_root, &event.xbutton.x, &event.xbutton.y, &event.xbutton.state);
	}
	
	if(XSendEvent(display, PointerWindow, True, 0xfff, &event) == 0) ;
	
	XFlush(display);
	
	usleep(100000);
	
	event.type = ButtonRelease;
	event.xbutton.state = 0x100;
	
	if(XSendEvent(display, PointerWindow, True, 0xfff, &event) == 0) ;
	
	XFlush(display);
	
	XCloseDisplay(display);

}

void mousebuttonup()
{
	// source: http://www.linuxquestions.org/questions/programming-9/simulating-a-mouse-click-594576/
	Display *display = XOpenDisplay(NULL);

	XEvent event;
	
	if(display == NULL)
	{
		return;
	}
	
	memset(&event, 0x00, sizeof(event));
	
	event.type = ButtonRelease;
	event.xbutton.state = 0x100;
	
	if(XSendEvent(display, PointerWindow, True, 0xfff, &event) == 0) ;
	
	XFlush(display);
	
	XCloseDisplay(display);

}
