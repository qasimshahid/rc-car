import cv2

# Create an object to read from camera
video = cv2.VideoCapture(0)

# We need to check if camera is opened previously or not
if not video.isOpened():
    print("Error reading video file")

# We need to set resolutions.
# So, convert them from float to integer.
frame_width = int(video.get(3))  # width
frame_height = int(video.get(4))  # height
size = (frame_width, frame_height)
print(size)

# Below VideoWriter object will create
# a frame of above defined size.
# The output is stored in 'filename.avi' file.
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
result = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 8, size)

# Record for 10 seconds

i = 0
while i < 100000:
    ret, frame = video.read()

    if ret:

        # Write the frame into the file 'filename.avi'
        result.write(frame)

        # Display the frame
        # saved in the file
        # cv2.imshow('Frame', frame)
        i = i + 1
        print(i)

    # Break the loop
    else:
        break

video.release()
result.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")
