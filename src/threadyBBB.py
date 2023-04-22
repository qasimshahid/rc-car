import threading
import subprocess
import cv2


# This file runs the video and the controller script together, so we can steer the car and record a video as well.
def script1():
    subprocess.call(['python3', 'cameraBBB.py'])


def script2():
    subprocess.call(['python3', 'mainBBB.py'])


if __name__ == '__main__':
    t1 = threading.Thread(target=script1)
    t2 = threading.Thread(target=script2)
    t1.start()
    t2.start()
