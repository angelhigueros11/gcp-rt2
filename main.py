# Angel Higueros
# 20460
# RT2

import math
from material import *
from light import *
from lib import *
from vector import *
from plane import *
from sphere import *
from mapp import *


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_color = color(1, 1, 1)
        self.background_color = color(1, 1, 1)
        self.framebuffer = [[]]
        self.scene = []
        self.light = None
        self.mapp_background = None
        self.clear()

    def clear(self):
        self.framebuffer = [[self.clear_color for _ in range(
            self.width)] for _ in range(self.height)]

    def set_light(self, position: V3, intensity, color):
        self.light = Light(position, intensity,  color)

    def point(self, x, y, color=None):
        if y >= 0 and y < self.height and x >= 0 and x < self.width:
            self.framebuffer[y][x] = color or self.current_color

    def set_sphere(self, center: V3, radius, material):
        self.scene.append(Sphere(center, radius, material))

    def set_plane(self, radius, material):
        self.scene.append(Plane(radius, material))

    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)

    def reflect(self, I, N):
        return (I - (N * 2 * (N @ I))).norm()

    def render(self):
        fov = int(math.pi / 2)
        ar = self.width / self.height
        tana = math.tan(fov / 2)

        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) - 1) * tana * ar
                j = (1 - (2 * (y + 0.5) / self.height)) * tana * ar

                direction = V3(i, j, -1).norm()
                origin = V3(0, 0, 0)
                c = self.cast_ray(origin, direction)

                self.point(x, y, c)

    def scene_intersect(self, origin, direction):
        zBuffer = 999999
        material = None
        intersect = None

        for o in self.scene:
            if obj_intersect := o.ray_intersect(origin, direction):
                if obj_intersect.distance < zBuffer:
                    zBuffer = obj_intersect.distance
                    material = o.material
                    intersect = obj_intersect

        return material, intersect

    def set_paint(self, r, g, b):
        self.background_color = color(r, g, b)

    def set_clear(self, r, g, b):
        self.clear_color = color(r, g, b)

    def cast_ray(self, origin, direction):
        material, intersect = self.scene_intersect(origin, direction)

        if material is None:
            return self.clear_color

        if intersect is None:
            return self.mapp_background.getColor(dir) if self.mapp_background else self.clear_color

        light_direction = (
            self.light.position - intersect.point
        ).norm()
        diffuse_intensity = light_direction @ intersect.normal

        diffuse = (
            material.diffuse[2] * diffuse_intensity * material.albedo[0],
            material.diffuse[1] * diffuse_intensity * material.albedo[0],
            material.diffuse[0] * diffuse_intensity * material.albedo[0]
        )

        intensity_specular = self.light.intensity * \
            max(0, self.reflect(light_direction, intersect.normal) @
                direction
                ) ** material.spec

        intensity = (
            self.light.color[2] * intensity_specular * material.albedo[1],
            self.light.color[1] * intensity_specular * material.albedo[1],
            self.light.color[0] * intensity_specular * material.albedo[1]
        )

        return color(
            diffuse[2] + intensity[2],
            diffuse[1] + intensity[1],
            diffuse[0] + intensity[0]
        )


# IMPLEMENTACIÓN
r = Raytracer(800, 800)
r.set_paint(1, 0, 0)
gray = Material(diffuse=(200/255, 200/255, 200/255),
                albedo=[0.9, 0.1], spec=10)
ivory = Material(diffuse=color(100, 100, 80), albedo=(0.6,  0.3, 0.1), spec=50)
rubber = Material(diffuse=color(80, 0, 0), albedo=(0.9,  0.1, 0), spec=10)
mirror = Material(diffuse=color(255, 255, 255), albedo=(0, 10, 0.8), spec=1425)
glass = Material(diffuse=color(150, 180, 200), albedo=[0, 0.5, 0.8], spec=1425)

r.set_light(V3(0, 1, -4), 10, (2, 2, 1))
r.set_sphere(V3(0, 0, 2), 3, mirror)

r.render()
r.write('rt2 .bmp')
