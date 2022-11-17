# Angel Higueros
# 20460
# RT2

import struct


class Mapp(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        with open(self.filename, "rb") as image:
            image.seek(10)
            size = struct.unpack('=l', image.read(4))[0]

            image.seek(14 + 4)
            self.width = size
            self.height = size

            image.seek(size)

            self.framebuffer = []

            for y in range(self.height):
                self.framebuffer.append([])
                for _ in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255

                    self.framebuffer[y].append((r, g, b))
