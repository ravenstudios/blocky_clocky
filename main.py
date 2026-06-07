import ds1302
from machine import Pin
import time
from sr_74hc595_bitbang import SR
from leds import *
import random


# ---------- HARDWARE ----------
rtc = ds1302.DS1302(Pin(18), Pin(19), Pin(20))

speed_button = Pin(6, Pin.IN, Pin.PULL_UP)
mode_button  = Pin(7, Pin.IN, Pin.PULL_UP)
up_button    = Pin(8, Pin.IN, Pin.PULL_UP)
down_button  = Pin(9, Pin.IN, Pin.PULL_UP)

ser   = Pin(2, Pin.OUT)
srclk = Pin(4, Pin.OUT)
rclk  = Pin(3, Pin.OUT)

sr = SR(ser, srclk, rclk)


# ---------- SETTINGS ----------
DEFAULT_TIME = [2026, 6, 7, 1, 12, 30, 0]

modes = ["run", "set_time", "set_12_24"]
mode = "run"

is_24_hour = True
set_field = "hours"

change_speeds = [100, 500, 1000, 2000, 10000]
change_speed_index = 2
change_speed_timer = 0

debounce_time = 200
mode_button_debounce_time = 0
speed_button_debounce_time = 0
up_button_debounce_time = 0
down_button_debounce_time = 0

hour = 0
minute = 0

tenth_hours_list = 0
hours_list = 0
tenth_minutes_list = 0
minutes_list = 0


# ---------- RTC ----------
def reset_rtc_default():
    print("Resetting RTC to default")
    rtc.date_time(DEFAULT_TIME)
    rtc.start()


def rtc_is_bad():
    dt = rtc.date_time()
    print("RTC:", dt)

    year, month, day, weekday, h, m, s = dt

    if year < 2024 or year > 2099:
        return True
    if month < 1 or month > 12:
        return True
    if day < 1 or day > 31:
        return True
    if h < 0 or h > 23:
        return True
    if m < 0 or m > 59:
        return True
    if s < 0 or s > 59:
        return True

    return False


def get_time_digits():
    h = rtc.hour()
    m = rtc.minute()

    if h > 23 or m > 59:
        reset_rtc_default()
        h = rtc.hour()
        m = rtc.minute()

    if not is_24_hour:
        if h > 12:
            h -= 12
        if h == 0:
            h = 12

    return [h // 10, h % 10, m // 10, m % 10]


# ---------- LED HELPERS ----------
def shift_update(data):
    sr.bits(0, 32, True)
    sr.bits(data, 32, True)


def shuffle_list(my_list):
    for i in range(len(my_list) - 1, 0, -1):
        j = random.randint(0, i)
        my_list[i], my_list[j] = my_list[j], my_list[i]


def get_random_leds(amount, list_leds):
    if amount > len(list_leds):
        print("LED amount too high:", amount, "max:", len(list_leds))
        amount = len(list_leds)

    temp_leds = list_leds.copy()
    shuffle_list(temp_leds)

    result = 0
    for i in range(amount):
        result += temp_leds[i]

    return result


def get_leds(amount, list_leds):
    if amount > len(list_leds):
        amount = len(list_leds)

    result = 0
    for i in range(amount):
        result += list_leds[i]

    return result


# ---------- DISPLAY MODES ----------
def run_clock():
    global change_speed_timer
    global tenth_hours_list, hours_list, tenth_minutes_list, minutes_list

    dt = get_time_digits()

    tenth_hours = dt[0]
    hours = dt[1]
    tenth_minutes = dt[2]
    minutes = dt[3]

    if time.ticks_ms() - change_speed_timer > change_speeds[change_speed_index]:
        change_speed_timer = time.ticks_ms()

        tenth_hours_list = get_random_leds(tenth_hours, tenth_hours_leds)
        hours_list = get_random_leds(hours, hours_leds)
        tenth_minutes_list = get_random_leds(tenth_minutes, tenth_minutes_leds)
        minutes_list = get_random_leds(minutes, minutes_leds)

    x = tenth_hours_list + hours_list + tenth_minutes_list + minutes_list

    if rtc.second() % 2 == 0:
        x += colon

    shift_update(x)


def show_set_time():
    tenth_hours = hour // 10
    hours = hour % 10
    tenth_minutes = minute // 10
    minutes = minute % 10

    h_leds = get_leds(tenth_hours, tenth_hours_leds) + get_leds(hours, hours_leds)
    m_leds = get_leds(tenth_minutes, tenth_minutes_leds) + get_leds(minutes, minutes_leds)

    if set_field == "hours":
        shift_update(h_leds)
    else:
        shift_update(m_leds)


def show_12_24():
    if is_24_hour:
        shift_update(d1 + d4 + d7 + colon)
    else:
        shift_update(d1 + d2 + d4 + d7 + d10 + d5 + colon)


# ---------- BUTTON HANDLERS ----------
def mode_button_handler(pin):
    global mode, hour, minute

    global mode_button_debounce_time
    now = time.ticks_ms()

    if now - mode_button_debounce_time < debounce_time:
        return

    mode_button_debounce_time = now

    old_mode = mode
    next_index = (modes.index(mode) + 1) % len(modes)
    mode = modes[next_index]

    if old_mode == "set_time":
        print("Saving time:", hour, minute)
        rtc.hour(hour)
        rtc.minute(minute)
        rtc.second(0)

    if mode == "set_time":
        hour = rtc.hour()
        minute = rtc.minute()


def speed_button_handler(pin):
    global set_field, change_speed_index
    global speed_button_debounce_time

    now = time.ticks_ms()

    if now - speed_button_debounce_time < debounce_time:
        return

    speed_button_debounce_time = now

    if mode == "run":
        change_speed_index = (change_speed_index + 1) % len(change_speeds)
        print("LED speed:", change_speeds[change_speed_index])

    elif mode == "set_time":
        if set_field == "hours":
            set_field = "mins"
        else:
            set_field = "hours"

        print("Set field:", set_field)


def up_button_handler(pin):
    global hour, minute, is_24_hour
    global up_button_debounce_time

    now = time.ticks_ms()

    if now - up_button_debounce_time < debounce_time:
        return

    up_button_debounce_time = now

    if mode == "set_time":
        if set_field == "hours":
            hour = (hour + 1) % 24
        else:
            minute = (minute + 1) % 60

    elif mode == "set_12_24":
        is_24_hour = True
        print("24 hour mode")


def down_button_handler(pin):
    global hour, minute, is_24_hour
    global down_button_debounce_time

    now = time.ticks_ms()

    if now - down_button_debounce_time < debounce_time:
        return

    down_button_debounce_time = now

    if mode == "set_time":
        if set_field == "hours":
            hour = (hour - 1) % 24
        else:
            minute = (minute - 1) % 60

    elif mode == "set_12_24":
        is_24_hour = False
        print("12 hour mode")


# ---------- STARTUP ----------
time.sleep(0.2)

# Hold UP + DOWN while powering on to reset RTC
if up_button.value() == 0 and down_button.value() == 0:
    reset_rtc_default()

rtc.start()

if rtc_is_bad():
    reset_rtc_default()

hour = rtc.hour()
minute = rtc.minute()

speed_button.irq(trigger=Pin.IRQ_FALLING, handler=speed_button_handler)
mode_button.irq(trigger=Pin.IRQ_FALLING, handler=mode_button_handler)
up_button.irq(trigger=Pin.IRQ_FALLING, handler=up_button_handler)
down_button.irq(trigger=Pin.IRQ_FALLING, handler=down_button_handler)


# ---------- MAIN LOOP ----------
while True:
    if mode == "run":
        run_clock()

    elif mode == "set_time":
        show_set_time()

    elif mode == "set_12_24":
        show_12_24()