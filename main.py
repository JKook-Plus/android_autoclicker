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

import dearpygui.dearpygui as dpg


coords = []

timer = 0



print(os.system(r'assets\adb\adb.exe devices'))

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


            if dpg.get_value(master_toggle) == True:

                global timer
                if dpg.get_value(autoclicker_toggle) == True and coords != []:
                    # print(timer)
                    if dpg.get_value(timer_toggle)  == True:
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


    # lmain.after(1, video_stream)




#
# video_stream()
#
#
#
# v_frame = Frame(root)
# v_frame.grid()
#
# volume_up_button = Button(master=v_frame, text='Volume Up', command= lambda: android.send_keycode(keycodes.AKEYCODE_VOLUME_UP))
# volume_up_button.pack(side="top")
# volume_down_button = Button(master=v_frame, text='Volume Down', command= lambda: android.send_keycode(keycodes.AKEYCODE_VOLUME_DOWN))
# volume_down_button.pack(side="bottom")






# root.mainloop() # Start the GUI

color_1_hex = "#202020"
color_2_hex = "#444444"
color_3_hex = "#546F8F"
color_4_hex = "#A58EA4"
color_5_hex = "#F7F2F2"

color_1 = tuple(int(color_1_hex.replace("#", "")[i:i+2], 16) for i in (0, 2, 4))
color_2 = tuple(int(color_2_hex.replace("#", "")[i:i+2], 16) for i in (0, 2, 4))
color_3 = tuple(int(color_3_hex.replace("#", "")[i:i+2], 16) for i in (0, 2, 4))
color_4 = tuple(int(color_4_hex.replace("#", "")[i:i+2], 16) for i in (0, 2, 4))
color_5 = tuple(int(color_5_hex.replace("#", "")[i:i+2], 16) for i in (0, 2, 4))




def save_callback():
    print("Save Clicked")

# dpg.set_main_window_size(500,500)
with dpg.window(label="Main Controls", width=426, height=900) as window_id:
    with dpg.theme() as theme:
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 25)
        dpg.add_theme_color(dpg.mvThemeCol_Button, color_2)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color_4)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color_2)
        dpg.add_theme_color(dpg.mvThemeCol_Border, color_2)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, color_2)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, color_1)


        # dpg.add_theme_style(dpg.mvStyleVar_FramePadding, i*3, i*3)

    master_toggle = dpg.add_checkbox(label="Master")
    autoclicker_toggle = dpg.add_checkbox(label="Autoclicker")
    timer_toggle = dpg.add_checkbox(label="Timer")
    volume_up_button = dpg.add_button(label="Volume Up", callback=lambda: android.send_keycode(keycodes.AKEYCODE_VOLUME_UP))
    volume_down_button = dpg.add_button(label="Volume Down", callback=lambda: android.send_keycode(keycodes.AKEYCODE_VOLUME_DOWN))
    dpg.set_item_theme(window_id, theme)

    with dpg.menu(label="Tools"):
        dpg.add_menu_item(label="Show Metrics", callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
dpg.setup_viewport()

cc = 0

while dpg.is_dearpygui_running():
    # print(cc)
    cc = cc+1
    video_stream()

    dpg.render_dearpygui_frame()
