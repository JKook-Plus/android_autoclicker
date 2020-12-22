import cv2
from viewer import AndroidViewer


# This will deploy and run server on android device connected to USB
android = AndroidViewer()

while True:
    frames = android.get_next_frames()
    # if frames != None:
    #     print(frames)
    if frames is None:
        continue

    for frame in frames:
        # cv2.imshow('game', frame)
        # cv2.waitKey(1)

        #percent by which the image is resized
        scale_percent = 45

        #calculate the 50 percent of original dimensions
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)

        # dsize
        dsize = (width, height)


        # cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
        # im = cv2.imread("earth.jpg")                        # Read image
        imS = cv2.resize(frame, dsize)                    # Resize image
        cv2.imshow("Phone Viewer", imS)                            # Show image
        cv2.waitKey(1)

        android.swipe(660, 739, 660, 739)
