import ds1302
from machine import Pin
import time
from sr_74hc595_bitbang import SR
from leds import *
import random

ds1302 = ds1302.DS1302(Pin(18),Pin(19),Pin(20))
 
speed_button = Pin(6, Pin.IN)
mode_button = Pin(7, Pin.IN)
down_button = Pin(9, Pin.IN)
up_button = Pin(8, Pin.IN)

up_button_debounce_time = 0
down_button_debounce_time = 0
speed_button_debounce_time = 0
mode_button_debounce_time = 0

change_speeds = [100, 500, 1000, 2000, 10000]
change_speed = change_speeds[2]
change_speed_timer = 0

modes = ["run", "set_time", "set_12-24"]
is_24_hour = True
set_time = False
prev_mode = modes[0]
mode = modes[0]
set_mode_hours_mins = "hours"
debounce_time = 200
hour, minute = 0, 0


tenth_hours_list = []
hours_list = get_random_leds = []
tenth_minutes_list = []
minutes_list = []

ser = Pin(2, Pin.OUT, machine.Pin.PULL_UP)
srclk = Pin(4, Pin.OUT, machine.Pin.PULL_UP)
rclk = Pin(3, Pin.OUT, machine.Pin.PULL_UP)



def mode_button_handler(x):
    global mode, modes, prev_mode, mode_button_debounce_time, debounce_time, hour, set_time, ds1302
    
    if time.ticks_ms() - mode_button_debounce_time > debounce_time:
        mode_button_debounce_time = time.ticks_ms()
        if mode == modes[2] and set_time == True:
            ds1302.hour(hour)
            ds1302.minute(minute)
            set_time = False
        
        
        id = modes.index(mode) + 1
        if id >= len(modes):
            id = 0
        mode = modes[id]


def speed_button_handler(x):
    
    global set_mode_hours_mins, speed_button_debounce_time, debounce_time, change_speeds, change_speed
    if time.ticks_ms() - speed_button_debounce_time > debounce_time:
        speed_button_debounce_time = time.ticks_ms()
        
        if mode == modes[0]:
           id =  change_speeds.index(change_speed) + 1
           change_speed = change_speeds[id % len(change_speeds)]
           
        if mode == modes[1]:
            if set_mode_hours_mins == "hours":
                set_mode_hours_mins = "mins"
            else:
                set_mode_hours_mins = "hours"
                
                

def up_button_handler(x):
    global mode, up_button_debounce_time, debounce_time, hour, minute, is_24_hour
    if time.ticks_ms() - up_button_debounce_time > debounce_time:
        up_button_debounce_time = time.ticks_ms()
        if mode == modes[1]:
            if set_mode_hours_mins == "hours":
                hour += 1
                hour = hour % 24
            else:
                minute += 1
                minute = minute % 60
                
        if mode == modes[2]:
            is_24_hour = True
           
        
        
        
def down_button_handler(x):
    global down_button_debounce_time, debounce_time, hour, minute, is_24_hour
    if time.ticks_ms() - down_button_debounce_time > debounce_time:
        down_button_debounce_time = time.ticks_ms()
        if mode == modes[1]:
            if set_mode_hours_mins == "hours":
                hour -= 1
                hour = hour % 24
            else:
                minute -= 1
                minute = minute % 60
        if mode == modes[2]:
            is_24_hour = False
        


def get_time():
    global is_24_hour, ds1302
    dt = [0, 0, 0, 0]
    h = ds1302.date_time()[4]
    m = ds1302.date_time()[5]
    
    if is_24_hour:
        if h > 12:
            h = h - 12
        if h == 0:
            h = 12
            
    dt[0] = h // 10
    dt[1] = h % 10
    dt[2] = m // 10
    dt[3] = m % 10
    
    return dt



def shift_update(data):
    sr = SR(ser, srclk, rclk)
    sr.bits(0, 32, 1)
    sr.bits(data, 32, 1)
    


def shuffle_list(my_list):
    for i in range(len(my_list) - 1, 0, -1):
        j = random.randint(0, i)
        my_list[i], my_list[j] = my_list[j], my_list[i]
        
        

def get_random_leds(ammount, list_leds):
    temp_leds = list_leds.copy()
    shuffle_list(temp_leds)
    result = 0
    for i in range(ammount):
        result += temp_leds[i]
    return result



def get_leds(ammount, list_leds):
    temp_leds = list_leds.copy()
    
    result = 0
    for i in range(ammount):
        result += temp_leds[i]
    return result




def set_clock():
    global hour, minutes, set_time
    
    tenth_hours = hour // 10
    hours = hour % 10
    tenth_minutes = minute // 10
    minutes = minute % 10
    x = 0
    
    tenth_hours_list = get_leds(tenth_hours, tenth_hours_leds)
    hours_list = get_leds(hours, hours_leds)
    tenth_minutes_list = get_leds(tenth_minutes, tenth_minutes_leds)
    minutes_list = get_leds(minutes, minutes_leds)
    
    if set_mode_hours_mins == "hours":
        x = sum([tenth_hours_list, hours_list])
    else:
        x = sum([tenth_minutes_list, minutes_list])
    shift_update(x)
    set_time = True
    
    
def clock():
    global prev_mode, hour, minute, set_time, is_24_hour, change_speed, change_speed_timer, tenth_hours_list, hours_list, tenth_minutes_list, minutes_list
    dt = get_time()
#     if is_24_hour:
#         h = dt[0] * 10 + dt[1]
#         if h > 12:
#             h = h - 12
#         if h == 0:
#             h == 12
#         dt[0] = h // 10
#         dt[1] = h % 10
    
    tenth_hours = dt[0]
    hours = dt[1]
    tenth_minutes = dt[2]
    minutes = dt[3]
    
    if time.ticks_ms() - change_speed_timer > change_speed:
        change_speed_timer = time.ticks_ms()
    
        tenth_hours_list = get_random_leds(tenth_hours, tenth_hours_leds)
        hours_list = get_random_leds(hours, hours_leds)
        
        tenth_minutes_list = get_random_leds(tenth_minutes, tenth_minutes_leds)
        minutes_list = get_random_leds(minutes, minutes_leds)
    
    x = sum([tenth_hours_list, hours_list, tenth_minutes_list, minutes_list])
    if ds1302.second() % 2 == 0:
        x += colon
    shift_update(x)
#     time.sleep(change_speed)



def set_12_24():
    global is_24_hour
    x = 0
    shift_update(x)
    
    if is_24_hour == False:
        x = sum([d1, d2, d4, d7, d10, d5, colon])
    else:
        
        x = sum([d1, d4, d7, colon])
    shift_update(x)
        
    
if __name__ == "__main__":
    ds1302
    speed_button.irq(trigger=Pin.IRQ_FALLING, handler=speed_button_handler)
    mode_button.irq(trigger=Pin.IRQ_FALLING, handler=mode_button_handler)
    up_button.irq(trigger=Pin.IRQ_FALLING, handler=up_button_handler)
    down_button.irq(trigger=Pin.IRQ_FALLING, handler=down_button_handler)
  
    ds1302.start()
    
    hour = ds1302.hour()
    minute = ds1302.minute()
    
    
    while True:
        if mode == "run":
            clock()
        if mode == "set_time":
            set_clock()
        if mode == "set_12-24":
            set_12_24()
