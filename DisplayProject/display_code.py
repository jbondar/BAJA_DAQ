# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_ssd1325

displayio.release_displays()

# SPI Initialization Code
spi = board.SPI()
oled_cs = board.D10
oled_dc = board.D13
display_bus = displayio.FourWire(
    spi, command=oled_dc, chip_select=oled_cs, baudrate=1000000, reset=board.D9
)
# width & height of screen in pixels
WIDTH = 128
HEIGHT = 64
BORDER = 1
FONTSCALE = 1

display = adafruit_ssd1325.SSD1325(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

# Creates a tile grid at upper left corner of screen
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a first inner rectangle
inner_bitmap = displayio.Bitmap(41,20, 1) # .Bitmap(width, height, )
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=1, y=1) # draws at (1,1)
splash.append(inner_sprite)

# Draw a second inner rectangle
inner_bitmap = displayio.Bitmap(41,20, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=43, y=1)
splash.append(inner_sprite)

# Draw a third inner rectangle
inner_bitmap = displayio.Bitmap(42,20, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=85, y=1)
splash.append(inner_sprite)

# Draw a fourth lower inner rectangle
inner_bitmap = displayio.Bitmap(126,41, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=1, y=22)
splash.append(inner_sprite)


text = "Hi     Bye    hello"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_width = text_area.bounding_box[2]*FONTSCALE
text_group = displayio.Group(
    max_size=10,
    scale=1,
    x=2,
    y=20 // 3,
)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)


text = "42 mph"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_width = text_area.bounding_box[2]*FONTSCALE
text_group = displayio.Group(
    max_size=10,
    scale=3,
    x=display.width // 2 - text_width // 2, #text_width is correct!
    y=22 + 42 // 3,
)

text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

while True:
    pass