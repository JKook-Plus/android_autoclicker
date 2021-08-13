import struct
from time import sleep

# https://android.googlesource.com/platform/frameworks/base.git/+/pie-release-2/core/java/android/view/SurfaceControl.java#305
#


# TYPE_INJECT_KEYCODE = 0
# TYPE_INJECT_TEXT = 1
# TYPE_INJECT_TOUCH_EVENT = 2
# TYPE_INJECT_SCROLL_EVENT = 3
# TYPE_BACK_OR_SCREEN_ON = 4
# TYPE_EXPAND_NOTIFICATION_PANEL = 5
# TYPE_EXPAND_SETTINGS_PANEL = 6
# TYPE_COLLAPSE_PANELS = 7
# TYPE_GET_CLIPBOARD = 8
# TYPE_SET_CLIPBOARD = 9
# TYPE_SET_SCREEN_POWER_MODE = 10 (9)
# TYPE_ROTATE_DEVICE = 11 (10)





# structure for messages (ControlMessage.java)
#
# union {
#     struct inject_keycode {
#         enum android_keyevent_action action;
#         enum android_keycode keycode;
#         uint32_t repeat;
#         enum android_metastate metastate;}
#
#     struct inject_text {
#         char *text; // owned, to be freed by free()}
#
#     struct inject_touch_event {
#         enum android_motionevent_action action;
#         enum android_motionevent_buttons buttons;
#         uint64_t pointer_id;
#         struct position position;
#         float pressure;}
#
#     struct inject_scroll_event {
#         struct position position;
#         int32_t hscroll;
#         int32_t vscroll;}
#
#     struct back_or_screen_on {
#         enum android_keyevent_action action; // action for the BACK key
#         // screen may only be turned on on ACTION_DOWN}
#
#     struct set_clipboard {
#         char *text; // owned, to be freed by free()
#         bool paste;}
#
#     struct set_screen_power_mode {
#         enum screen_power_mode mode;}





class ControlMixin:
    ACTION_MOVE = b'\x02'
    ACTION_DOWN = b'\x00'
    ACTION_UP = b'\x01'

    move_step_length = 5  # Move by 5 pixels in one iteration
    move_steps_delay = 0.005  # Delay between each move step

    # Define in base class
    resolution = None
    control_socket = None

    def _build_touch_message(self, x, y, action):
        b = bytearray(b'\x02')
        b += action
        b += b'\xff\xff\xff\xff\xff\xff\xff\xff'
        b += struct.pack('>I', int(x))
        b += struct.pack('>I', int(y))
        b += struct.pack('>h', int(self.resolution[0]))
        b += struct.pack('>h', int(self.resolution[1]))
        b += b'\xff\xff'  # Pressure
        b += b'\x00\x00\x00\x01'  # Event button primary
        # print(b)
        return bytes(b)

        # CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT,
        # 0x00, // AKEY_EVENT_ACTION_DOWN
        # 0x12, 0x34, 0x56, 0x78, 0x87, 0x65, 0x43, 0x21, // pointer id
        # 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0xc8, // 100 200
        # 0x04, 0x38, 0x07, 0x80, // 1080 1920
        # 0xff, 0xff, // pressure
        # 0x00, 0x00, 0x00, 0x01 // AMOTION_EVENT_BUTTON_PRIMARY





    def rotate_device(self):
        # TYPE_ROTATE_DEVICE (11) (\n)
        msg = bytearray(b'\012')
        self.control_socket.send(msg)

    def power_button(self):
        msg = bytearray(b'\005')
        self.control_socket.send(msg)

    def lock_device(self):
        msg = bytearray(b'\004')
        self.control_socket.send(msg)

    def set_screen_power_mode(self, power_mode=2):
        # TYPE_SET_SCREEN_POWER_MODE (10) (\t)
        if not (0 <= power_mode <= 4):
            print("aaaaa")
            return
        msg = bytearray(b'\t')
        msg += struct.pack('B', int(power_mode))
        self.control_socket.send(msg)


    def send_keycode(self, keycode):

        if not (keycode > 284):
            # print(keycode)
            b = bytearray(b'\x00')
            b += (b"\x00")
            b += struct.pack("!I", keycode)
            b += (b"\x00\x00\x00\x00")
            # print(b)
            self.control_socket.send(b)

        else:
            print("Keycode: {0} is not valid".format(keycode))

    def tap(self, x_coord, y_coord):
        self.control_socket.send(self._build_touch_message(x=x_coord, y=y_coord, action=self.ACTION_DOWN))
        self.control_socket.send(self._build_touch_message(x=x_coord, y=y_coord, action=self.ACTION_UP))

    def swipe(self, start_x, start_y, end_x, end_y):
        self.control_socket.send(self._build_touch_message(x=start_x, y=start_y, action=self.ACTION_DOWN))
        next_x = start_x
        next_y = start_y

        if end_x > self.resolution[0]:
            end_x = self.resolution[0]

        if end_y > self.resolution[1]:
            end_y = self.resolution[1]

        decrease_x = True if start_x > end_x else False
        decrease_y = True if start_y > end_y else False
        while True:
            if decrease_x:
                next_x -= self.move_step_length
                if next_x < end_x:
                    next_x = end_x
            else:
                next_x += self.move_step_length
                if next_x > end_x:
                    next_x = end_x

            if decrease_y:
                next_y -= self.move_step_length
                if next_y < end_y:
                    next_y = end_y
            else:
                next_y += self.move_step_length
                if next_y > end_y:
                    next_y = end_y

            self.control_socket.send(self._build_touch_message(x=next_x, y=next_y, action=self.ACTION_MOVE))

            if next_x == end_x and next_y == end_y:
                self.control_socket.send(self._build_touch_message(x=next_x, y=next_y, action=self.ACTION_UP))
                break
            sleep(self.move_steps_delay)
