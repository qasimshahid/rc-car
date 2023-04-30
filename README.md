# RC_Car
Creating software to control a RC car remotely. Done entirely in Python, using a mix of procedural and object-oriented code.
Optimized to work with the BeagleBone Black, which is what this was built for. 

TO DO - Frontend

DONE - Acceleration, Steering, Reversing, Wireless Control, Video Streaming via UDP to RTSP server, Race Management Connection, Error Handling 


Steps:
Run the laptop server first (mainL.py) (make sure joystick is connected), afterwards run mainBBB.py in BBB.
If you for some reason lose connection on the BBB, use Ctrl-C to exit the program (this will stop the car) and run the mainBBB.py file again. Keep mainL running. Use the "start" button on your controller to re-establish the UDP connection. 
