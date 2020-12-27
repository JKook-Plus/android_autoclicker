# from ppadb.client import Client

from ppadb.client import Client
import time
from PIL import ImageDraw, ImageTk
import PIL.Image

import numpy as np

import cv2
from viewer import AndroidViewer


from tkinter import *

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
    for (x,y) in coords:
        draw.rectangle([x,y,x+dotSize2-1,y+dotSize2-1], fill="black")
        draw.rectangle([x,y,x+dotSize-1,y+dotSize-1], fill="yellow")


    # draw.line((0, 0) + im.size, fill=128)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)

    # write to stdout
    im.save("click_locations.png", "PNG")



android = AndroidViewer()


root = Tk()


lmain = Label(root, width=50, height=10)
lmain.grid()
root.title("Controls")

def video_stream():
    frames = android.get_next_frames()
    # print(frames)
    if frames is None:
        pass

    else:
        for frame in frames:

            scale_percent = 45

            #calculate the 50 percent of original dimensions
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)

            # dsize
            dsize = (width, height)


            # b,g,r = cv2.split(frame)
            # img = cv2.merge((r,g,b))

            # im = PIL.Image.fromarray(img)
            imS = cv2.resize(frame, dsize)

            cv2.imshow('Phone Viewer', imS)
            cv2.waitKey(1)
            for coord in coords:
                # if isinstance(button1.config('textvariable')[-1], str) == True:
                #     button1.config(text='OFF', bg="red",activebackground="red",textvariable=0)



                if button1.config('text')[-1] =='OFF':
                    # print(frame[168, 1034])
                    pass

                    # [229 191  15]
                else:

                    android.tap(coord[0], coord[1])
            # imgtk = ImageTk.PhotoImage(image=im)
            # lmain.imgtk = imgtk
            # lmain.configure(image=imgtk)
    lmain.after(1, video_stream)


# def clicker(frame):
# loop.call_soon_threadsafe(callback, *args)
#
# asyncio.run_coroutine_threadsafe(video_stream(), loop)



# await video_stream()
# asyncio.run()
video_stream()


# root = Tk()
#
# app = Frame(root, bg="white")
# app.grid()
# lmain = Label(app)
# lmain.grid()
# root.title("Controls")




def toggle1():
    if button1.config('text')[-1] =='ON':
        button1.config(text='OFF', bg="red",activebackground="red",textvariable=0)
        print(button1.config('textvariable')[-1])
    else:
        button1.config(text='ON', bg="green",activebackground="green",textvariable=1)
        print(button1.config('textvariable')[-1])

button1 = Button(
            root,
            text="OFF",
            width=12,
            height=1,
            borderwidth=0,
            command=toggle1 ,
            relief="raised",
            state="normal",
            bg="red",
            activebackground="red",
            repeatdelay=1)
button1.grid(pady=5)




root.mainloop() # Start the GUI
