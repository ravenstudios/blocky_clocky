````md
# Random LED Clock

A random-pattern LED clock built using an RP2040, DS1302 RTC, and 74HC595 shift registers.

The clock displays the current time using randomized LED positions while maintaining the correct numeric value.

---

# Features

- Randomized LED clock display
- DS1302 RTC timekeeping
- 12-hour and 24-hour modes
- Adjustable LED animation speed
- Time setting mode
- RTC corruption protection
- RTC reset button combo
- 4-button interface

---

# Button Layout

Buttons are arranged vertically.

Top to bottom:

1. SPEED
2. MODE
3. UP
4. DOWN

---

# Modes

| Mode | Description |
|---|---|
| Run | Normal clock display |
| Set Time | Adjust hours and minutes |
| 12/24 | Select 12-hour or 24-hour display |

---

# Controls

## Run Mode

### Change LED Animation Speed

Press the **SPEED** button.

Available speeds:

- Very Fast
- Fast
- Medium
- Slow
- Very Slow

Each press cycles to the next speed.

---

## Set Time Mode

Press the **MODE** button until the clock enters time-setting mode.

### Select Hours or Minutes

Press the **SPEED** button to switch between:

- Hours
- Minutes

### Adjust Time

- **UP** increases value
- **DOWN** decreases value

### Save Time

Press **MODE** to exit time-setting mode.

The time is automatically saved to the RTC.

---

## 12/24 Hour Mode

Press **MODE** until the clock enters 12/24-hour mode.

- Press **UP** for 24-hour mode
- Press **DOWN** for 12-hour mode

Press **MODE** again to return to the clock.

---

# RTC Recovery

If the RTC loses power or becomes corrupted, invalid time values may appear.

## Reset RTC to Default Time

1. Power OFF the clock
2. Hold:
   - UP
   - DOWN
3. Power ON while holding both buttons

The RTC will reset to the programmed default time.

---

# LED Display

The LEDs are randomized every refresh cycle.

The quantity of illuminated LEDs represents the displayed number.

Example:
- 5 = five LEDs illuminated
- 2 = two LEDs illuminated

The positions change randomly while preserving the correct count.

---

# Hardware

## Main Components

- RP2040
- DS1302 RTC
- 74HC595 Shift Registers
- LEDs
- 4 Push Buttons

---

# File Structure

```text
main.py
ds1302.py
sr_74hc595_bitbang.py
leds.py
````

---

# Default RTC Time

```python
DEFAULT_TIME = [2026, 6, 7, 1, 12, 30, 0]
```

Format:

```python
[year, month, day, weekday, hour, minute, second]
```

---

# Troubleshooting

## Clock Shows Incorrect Time

Enter time-setting mode and adjust the time.

If the RTC data is corrupted:

* Perform the RTC reset procedure.

---

## LEDs Frozen

Restart the clock.

---

## RTC Does Not Keep Time

Check:

* RTC backup battery
* DS1302 wiring
* RTC module connections

---

# Wiring Notes

## RTC

```text
CLK  -> GPIO18
DIO  -> GPIO19
CS   -> GPIO20
```

## Shift Register

```text
SER   -> GPIO2
SRCLK -> GPIO4
RCLK  -> GPIO3
```

## Buttons

```text
SPEED -> GPIO6
MODE  -> GPIO7
UP    -> GPIO8
DOWN  -> GPIO9
```

Buttons use internal pull-up resistors.

Pressed state = LOW.

---

# License

MIT License

```
```
