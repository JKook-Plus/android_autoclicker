# from ppadb.client import Client

from ppadb.client import Client
import time
from PIL import Image, ImageDraw

import cv2
from viewer import AndroidViewer


import subprocess


from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import tkinter.simpledialog

# client = Client(host="127.0.0.1", port=5037)
# print(client)
# device = client.device("emulator-5554")
# print(device)
# result = device.screencap()
# with open("screen.png", "wb") as fp:
#     fp.write(result)

coords = []





def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    return devices[0]

def take_screenshot(device):

    image = device.screencap()

    with open('screen.png', 'wb') as f:
        f.write(image)


device = connect_device()
take_screenshot(device)





#
# for i in range(10):
#     device.shell(f'input tap 500 200')
#     time.sleep(0.75)






root = Tk()

basewidth = 450

File = "screen.png"
img = Image.open(File)

org_w = img.width
org_h = img.height

print("Original Width:", org_w, "\nOriginal Height:", org_h)


wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)

image_width = img.width
image_height = img.height

print("\nEdited Width:", img.width, "\nEdited Height:",img.height)


w = Canvas(root, width=img.width, height=img.height)
w.pack()


img = ImageTk.PhotoImage(img)
w.create_image(0, 0, image=img, anchor="nw")





def on_click(event):
    x, y = event.x, event.y
    x1, y1 = (((event.x) * (org_w)) / (image_width)), (((event.y) * (org_h)) / (image_height))

    (((event.x) * (org_w)) / (image_width))
    print('{}, {}'.format(x1, y1))
    coords.append((x1, y1))


root.bind('<Button-1>', on_click)


root.mainloop()










print(coords)

with Image.open("screen.png") as im:

    draw = ImageDraw.Draw(im)

    # coords = [(900,1200)]
    dotSize = 30
    dotSize2 = 40
    for (x,y) in coords:
        draw.rectangle([x,y,x+dotSize2-1,y+dotSize2-1], fill="black")
        draw.rectangle([x,y,x+dotSize-1,y+dotSize-1], fill="yellow")


    # draw.line((0, 0) + im.size, fill=128)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)

    # write to stdout
    im.save("click_locations.png", "PNG")


# for i in range(50):
#     for coord in coords:
#         device.shell('input tap %s %s && input tap %s %s '%(coord[0], coord[1], coord[0], coord[1]))
#         # subprocess.call("adb shell input tap %s %s"%(coord[0], coord[1]), shell = True)
#
#         print(coord[0], coord[1])



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
        for coord in coords:
            # android.swipe(coord[0], coord[1], coord[0], coord[1])tap
            android.tap(coord[0], coord[1])
