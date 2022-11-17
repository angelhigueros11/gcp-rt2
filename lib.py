# Angel Higueros
# 20460
# RT2

import struct
from vector import *


def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(d):
    return struct.pack('=l', d)


def color(r, g, b):

    r = r * 255
    r = min(r, 255)
    r = max(r, 0)
    g = g * 255
    g = min(g, 255)
    g = max(g, 0)
    b = b * 255
    b = min(b, 255)
    b = max(b, 0)
    return bytes([int(b), int(g), int(r)])


def writebmp(filename, width, height, framebuffer):
    with open(filename, 'bw') as f:
        # Pixel header
        f.write(char('B'))
        f.write(char('M'))
        # tamaño archivo = 14 header + 40  info header + resolucion
        f.write(dword(14 + 40 + width * height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # Info header
        f.write(dword(40))  # tamaño header
        f.write(dword(width))  # ancho
        f.write(dword(height))  # alto
        f.write(word(1))  # numero de planos (siempre 1)
        f.write(word(24))  # bits por pixel (24 - rgb)
        f.write(dword(0))  # compresion
        f.write(dword(width * height * 3))  # tamaño imagen sin header
        f.write(dword(0))  # resolucion
        f.write(dword(0))  # resolucion
        f.write(dword(0))  # resolucion
        f.write(dword(0))  # resolucion

        for y in range(height):
            for x in range(width):
                f.write(framebuffer[y][x])
