# from ppadb.client import Client

from ppadb.client import Client
import time
from PIL import ImageDraw, ImageTk
import PIL.Image

import numpy as np

import cv2
from assets.viewer import AndroidViewer
import assets.keycodes as keycodes

from tkinter import *

import os

coords = []

timer = 0



print(os.system('adb\\adb.exe devices'))

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
root = Tk()
basewidth = 450

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



print(coords)

with PIL.Image.open("screen.png") as im:

    draw = ImageDraw.Draw(im)

    # coords = [(900,1200)]
    dotSize = 30
    dotSize2 = 40
    for (x, y) in coords:
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

    # cv2.imshow(name, mask)

    # cv2.waitKey(1)
    return(round(cv2.countNonZero(mask)/mask.size*100,0))


android = AndroidViewer()


root = Tk()


lmain = Label(root, width=50, height=10)
root.title("Controls")

def midpoint(_dict, index):
    return (np.mean(_dict[index][0][1]), np.mean(_dict[index][0][0]))

toggle_screen = 0
def toggle_display():
    global toggle_screen
    if toggle_screen == 0:
        android.set_screen_power_mode(0)
        toggle_screen = 1
    else:
        android.set_screen_power_mode(1)
        toggle_screen = 0




def video_stream():

    blue_1 = [[90,220,150],[100,250,255]]
    orange_1 = [[16,200,220], [18,255,255]]

    resize_size = 30

    tot_before = {
    "Level Up":
                [[[164, 252], [1132, 1413]],
                orange_1],
    "No, Thanks Bird":
                [[[1803, 1973],[288, 1150]],
                blue_1
                ],
    # 742, 1596 (45)
    "Collect":
                [[[1513, 1683],[288, 1150]],
                blue_1
                ]
    }



    tot = {}
    for key in tot_before:
        tot[key] = [[(np.multiply(tot_before[key][0][0], resize_size/100)).astype(int), (np.multiply(tot_before[key][0][1], resize_size/100)).astype(int)], tot_before[key][1]]


    # print(tot)



    frames = android.get_next_frames()
    if frames is None:
        pass

    else:
        # print(len(frames))

        for frame in frames:


            imS = resizer(frame, resize_size)
            # print(imS.shape[0], imS.shape[1])
            sc = cv2.cvtColor(imS, cv2.COLOR_BGR2RGB)
            percentages = []


            # for key in tot:
            #     x, y = tot[key][0]
            #     color_r = tot[key][1]
            #     selection = sc[ x[0]:x[1], y[0]:y[1] ]
            #
            #
            #     percentages.append(masking(selection, color_r, key))


            if m_switch_variable.get() == "on":

                # if ra_switch_variable.get() == "on":
                    # if percentages[1] >= 80:
                    #     # 700 1875
                    #     ntb_l = midpoint(tot_before, "No, Thanks Bird")
                    #     android.tap(ntb_l[0], ntb_l[1])
                    #     print("Clicked No thanks Bird")
                    #
                    # if percentages[2] >= 80:
                    #     c_l = midpoint(tot_before, "Collect")
                    #     android.tap(c_l[0], c_l[1])
                    #     print("Clicked Collect")


                # if lu_switch_variable.get() == "on" and percentages[0] >= 70:
                #     lu_l = midpoint(tot_before, "Level Up")
                #     android.tap(lu_l[0], lu_l[1])
                #     print("Clicked Level Up")



                global timer
                if ac_switch_variable.get() == "on" and coords != []:
                    # print(timer)
                    if timer_switch_variable.get() == "on":
                        timer = timer +1
                        if timer > 0 and timer < 80:
                            for coord in coords:
                                android.tap(coord[0], coord[1])


                        if timer > 330:
                            timer = 0
                    else:
                        # android.build_blackout_screen()
                        for coord in coords:
                            android.tap(coord[0], coord[1])



            # print(ac_switch_variable.get())

            cv2.imshow('Phone Viewer', imS)
            cv2.waitKey(1)


    lmain.after(1, video_stream)



video_stream()

m_switch_frame = Frame(root)
m_switch_frame.grid()

m_switch_variable = StringVar(value="on")

m_switch_label = Label(m_switch_frame, text="Master Toggle")
m_off_button = Radiobutton(m_switch_frame, text="Off", variable=m_switch_variable,
                            indicatoron=False, value="off", width=8)
m_on_button = Radiobutton(m_switch_frame, text="On", variable=m_switch_variable,
                            indicatoron=False, value="on", width=8)

m_switch_label.pack(side="left")
m_off_button.pack(side="left")
m_on_button.pack(side="left")




ra_switch_frame = Frame(root)
ra_switch_frame.grid()

ra_switch_variable = StringVar(value="on")

ra_switch_label = Label(ra_switch_frame, text="Remove Adds")
ra_off_button = Radiobutton(ra_switch_frame, text="Off", variable=ra_switch_variable,
                            indicatoron=False, value="off", width=8)
ra_on_button = Radiobutton(ra_switch_frame, text="On", variable=ra_switch_variable,
                            indicatoron=False, value="on", width=8)
ra_switch_label.pack(side="left")
ra_off_button.pack(side="left")
ra_on_button.pack(side="left")






ac_switch_frame = Frame(root)
ac_switch_frame.grid()

ac_switch_variable = StringVar(value="off")

ac_switch_label = Label(ac_switch_frame, text="Autoclicker Toggle")
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

lu_switch_label = Label(lu_switch_frame, text="Level Up Toggle")
lu_off_button = Radiobutton(lu_switch_frame, text="Off", variable=lu_switch_variable,
                            indicatoron=False, value="off", width=8)
lu_on_button = Radiobutton(lu_switch_frame, text="On", variable=lu_switch_variable,
                            indicatoron=False, value="on", width=8)
lu_switch_label.pack(side="left")
lu_off_button.pack(side="left")
lu_on_button.pack(side="left")


timer_switch_frame = Frame(root)
timer_switch_frame.grid()

timer_switch_variable = StringVar(value="off")

timer_switch_label = Label(timer_switch_frame, text="Timer Toggle")
timer_off_button = Radiobutton(timer_switch_frame, text="Off", variable=timer_switch_variable,
                            indicatoron=False, value="off", width=8)
timer_on_button = Radiobutton(timer_switch_frame, text="On", variable=timer_switch_variable,
                            indicatoron=False, value="on", width=8)
timer_switch_label.pack(side="left")
timer_off_button.pack(side="left")
timer_on_button.pack(side="left")

w_frame = Frame(root)
w_frame.grid()

w = Button(w_frame, text ="Toggle display", command = toggle_display)
w.pack(side="left")



v_frame = Frame(root)
v_frame.grid()

volume_up_button = Button(master=v_frame, text='Volume Up', command= lambda: android.send_keycode(keycodes.AKEYCODE_VOLUME_UP))
volume_up_button.pack(side="top")
volume_down_button = Button(master=v_frame, text='Volume Down', command= lambda: android.send_keycode(keycodes.AKEYCODE_VOLUME_DOWN))
volume_down_button.pack(side="bottom")






root.mainloop() # Start the GUI
