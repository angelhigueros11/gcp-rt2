# Graficas por computador
# Angel Higueros - 20460
# RT1

import struct
from vector import *

# Métodos de escritura
def char(c): 
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __mul__(self, other):
        r = self.r
        g = self.g
        b = self.b

        if type(other) == int or type(other) == float64:
           r *= other
           g *= other
           b *= other
        else:
           r *= other.r
           g *= other.g
           b *= other.b
        
        r = min(255, max(r, 0))
        g = min(255, max(g, 0))
        b = min(255, max(b, 0))
        return color(r, g, b)

            
    def toBytes(self):
        return bytes([int(self.b), int(self.g), int(self.r)])

    def __repr__(self):
        return "color(%s, %s, %s)" % (self.r, self.g, self.b)

def writebmp(filename, width, height, framebuffer):
    f = open(filename, 'bw')

    # Pixel header
    f.write(char('B'))
    f.write(char('M'))
    # tamaño archivo = 14 header + 40  info header + resolucion
    f.write(dword(14 + 40 + width * height * 3)) 
    f.write(word(0))
    f.write(word(0))
    f.write(dword(14 + 40))

    # Info header
    f.write(dword(40)) # tamaño header
    f.write(dword(width)) # ancho
    f.write(dword(height)) # alto
    f.write(word(1)) # numero de planos (siempre 1)
    f.write(word(24)) # bits por pixel (24 - rgb)
    f.write(dword(0)) # compresion
    f.write(dword(width * height * 3)) # tamaño imagen sin header
    f.write(dword(0)) # resolucion
    f.write(dword(0)) # resolucion
    f.write(dword(0)) # resolucion
    f.write(dword(0)) # resolucion


    for y in range(height):
        for x in range(width):
            f.write(framebuffer[y][x].toBytes())
    
    f.close()
