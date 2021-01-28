# from ppadb.client import Client

from ppadb.client import Client
import time
from PIL import ImageDraw, ImageTk
import PIL.Image

import numpy as np

import cv2
from viewer import AndroidViewer

from tkinter import *


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
# root = Tk()
basewidth = 450
"""
File = "screen.png"
img = PIL.Image.open(File)

org_w = img.width
org_h = img.height

print("Original Width:", org_w, "\nOriginal Height:", org_h)


wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)

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

"""

print(coords)

with PIL.Image.open("screen.png") as im:

    draw = ImageDraw.Draw(im)

    # coords = [(900,1200)]
    dotSize = 30
    dotSize2 = 40
    for (x,y) in coords:
        draw.rectangle([x,y,x+dotSize2-1,y+dotSize2-1], fill="black")
        draw.rectangle([x,y,x+dotSize-1,y+dotSize-1], fill="yellow")

    # write to stdout
    im.save("click_locations.png", "PNG")

def resizer(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    dsize = (width, height)
    imS = cv2.resize(image, dsize)
    return imS


def masking(view, ra, name):
    lower = np.array(ra[0])
    upper = np.array(ra[1])
    hsv = cv2.cvtColor(view, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    view_height, view_width, _ = view.shape

    # print(view_height, view_width)
    # 1026 486

    # print(cv2.countNonZero(mask), mask.size, cv2.countNonZero(mask)/mask.size*100)


    cv2.imshow(name, mask)

    cv2.waitKey(1)
    return(round(cv2.countNonZero(mask)/mask.size*100,0))




android = AndroidViewer()


root = Tk()


lmain = Label(root, width=50, height=10)
lmain.grid()
root.title("Controls")

def video_stream():
    frames = android.get_next_frames()
    if frames is None:
        pass

    else:
        # print(len(frames))

        for frame in frames:


            imS = resizer(frame, 45)

            sc = cv2.cvtColor(imS, cv2.COLOR_BGR2RGB)


            crop_coords = [
            [[55,85],[380,478]],
            [[610, 666],[97, 389]]
            ]


            color_range = [
            [[16,200,220],[18,255,255]],
            [[90,220,150],[100,250,255]]
            ]

            name = [
            "Level Up",
            "No, Thanks Bird"
            ]

            percentages = []

            for cc, c, n in zip(crop_coords, color_range, name):
                x, y = cc
                t = sc[ x[0]:x[1], y[0]:y[1] ]
                percentages.append(masking(t, c, n))


            print(percentages)



            if percentages[0] >= 70:
                # android.tap(1034, 155)
                print("clicked Level Up")

            # No thanks Bird
            if percentages[1] >= 80:
                # android.tap(782, 1413)
                print("clicked No thanks Bird")


            # Collect
            if np.all(frame[1195, 782] == [229, 191, 15]):
                # android.tap(782, 1195)
                print("clicked Collect")


            print(ac_switch_variable.get())

            # cv2.imshow('Phone Viewer', imS)
            # cv2.waitKey(1)
            for coord in coords:
                if button1.config('text')[-1] =='OFF':
                    pass

                else:
                    pass
                    # Level Up Checker


                    # android.tap(coord[0], coord[1])

    lmain.after(1, video_stream)



video_stream()


ac_switch_frame = Frame(root)
ac_switch_frame.grid()

ac_switch_variable = StringVar(value="off")

ac_switch_label = Label(ac_switch_frame, text="Autoclicker Toggle ")
ac_off_button = Radiobutton(ac_switch_frame, text="Off", variable=ac_switch_variable,
                            indicatoron=False, value="off", width=8)
ac_low_button = Radiobutton(ac_switch_frame, text="On", variable=ac_switch_variable,
                            indicatoron=False, value="on", width=8)
ac_switch_label.pack(side="left")
ac_off_button.pack(side="left")
ac_low_button.pack(side="left")



lu_switch_frame = Frame(root)
lu_switch_frame.grid()

lu_switch_variable = StringVar(value="off")

lu_switch_label = Label(lu_switch_frame, text="Level Up Toggle ")
lu_off_button = Radiobutton(lu_switch_frame, text="Off", variable=lu_switch_variable,
                            indicatoron=False, value="off", width=8)
lu_on_button = Radiobutton(lu_switch_frame, text="On", variable=lu_switch_variable,
                            indicatoron=False, value="on", width=8)
lu_switch_label.pack(side="left")
lu_off_button.pack(side="left")
lu_on_button.pack(side="left")



root.mainloop() # Start the GUI
