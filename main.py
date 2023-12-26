import ds1302
from machine import Pin
import time
from sr_74hc595_bitbang import SR
from leds import *
import random

ds = ds1302.DS1302(Pin(18),Pin(19),Pin(20))
# ds.date_time([2023, 3, 9, 4, 2, 41, 0])
# 
brightness_button = Pin(6, Pin.IN)
mode_button = Pin(7, Pin.IN)
down_button = Pin(8, Pin.IN)
up_button = Pin(9, Pin.IN)

up_button_debounce_time = 0
down_button_debounce_time = 0

modes = ["run", "set"]
is_24_hour = True
mode = modes[0]
set_mode_hours_mins = "hours"
debounce_time = 200

ser = Pin(2, Pin.OUT, machine.Pin.PULL_UP)
srclk = Pin(4, Pin.OUT, machine.Pin.PULL_UP)
rclk = Pin(3, Pin.OUT, machine.Pin.PULL_UP)


sr = SR(ser, srclk, rclk)
print(type(d1))

def change_mode(x):
    global mode, modes
    if mode == modes[0]:
        mode = modes[1]
    else:
        mode = modes[0]
    print(f"Mode:{mode}")



def change_brightness(x):
    global set_mode_hours_mins
    if mode == modes[1]:
        if set_mode_hours_mins == "hours":
            set_mode_hours_mins = "mins"
        else:
            set_mode_hours_mins = "hours"
    



        
        
def add_hour(ds):
    ds.hour(ds.hour() + 1)

def add_minute(ds):
    ds.minute(ds.minute() + 1)

def sub_hour(ds):
    ds.hour(ds.hour() + -1)

def sub_minute(ds):
    ds.minute(ds.minute() + -1)


def up_button_handler():
    global up_button_debounce_time, debounce_time
    if time.ticks_ms() - up_button_debounce_time > debounce_time:
        up_button_debounce_time = time.ticks_ms()
        if set_mode_hours_mins == "hours":
            add_hour(ds)
        else:
            add_minute(ds)
        
        
def down_button_handler():
    global down_button_debounce_time, debounce_time
    if time.ticks_ms() - down_button_debounce_time > debounce_time:
        down_button_debounce_time = time.ticks_ms()
        if set_mode_hours_mins == "hours":
            sub_hour(ds)
        else:
            sub_minute(ds)
        



def get_time(ds):
    dt = [0, 0, 0, 0]
    h = ds.date_time()[4]
    m = ds.date_time()[5]
    
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
    global sr
    sr.bits(0, 32, 1)
    sr.bits(data, 32, 1)
    


def shuffle_list(my_list):
    for i in range(len(my_list) - 1, 0, -1):
        j = random.randint(0, i)
        my_list[i], my_list[j] = my_list[j], my_list[i]
        
        

def get_random_leds(ammount, list_leds):
    temp_leds = list_leds
    shuffle_list(temp_leds)
    result = 0
    for i in range(ammount):
        result += temp_leds[i]
    return result


    
if __name__ == "__main__":
    brightness_button.irq(trigger=Pin.IRQ_FALLING, handler=change_brightness)
    mode_button.irq(trigger=Pin.IRQ_FALLING, handler=change_mode)
  
    ds.start()
    dt = get_time(ds)

    
    
    while True:
        dt = ds.date_time()
        tenth_hours = dt[4] // 10
        hours = dt[4] % 10
        tenth_minutes = dt[5] // 10
        minutes = dt[5] % 10
        
        tenth_hours_list = get_random_leds(tenth_hours, tenth_hours_leds)
        hours_list = get_random_leds(hours, hours_leds)
        
        tenth_minutes_list = get_random_leds(tenth_minutes, tenth_minutes_leds)
        minutes_list = get_random_leds(minutes, minutes_leds)
        
        x = sum([tenth_hours_list, hours_list, tenth_minutes_list, hours_list])
#         print(x)
        
        if ds.second() % 2 == 0:
            x += colon
        shift_update(x)
        time.sleep(1)


