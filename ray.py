from lib import *
from numpy import *
from sphere import *
from material import *
from light import *

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color =color(0, 0, 0)
        self.current_color = color(255, 255, 255)
        self.scene = []
        self.light = Light(V3(0, 0, 0), 1)
        self.clear()
    
    def clear(self):
        self.framebuffer = [
            [self.background_color for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def point(self, x, y, color=None):
        if y >= 0 and y < self.height and x >= 0 and x < self.width:
            self.framebuffer[y][x] = color or self.current_color

    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)
    
    def render(self):

        fov = int(pi / 2)
        ar = self.width / self.height
        tana = tan(fov / 2)

        for y in range(self.height):
            for x in range(self.width):
                i = ((2 *  (x + 0.5) / self.width) - 1) * ar * tana
                j = ( 1 - (2 *  (y + 0.5) / self.height)) * tana

                origin = V3(0, 0, 0)
                direction = V3(i, j, -1).norm()
                c = self.cast_ray(origin, direction)

                self.point(x, y, c)

    def cast_ray(self, origin, direction, recursion = 0):
        material, intersect = self.scene_intersect(origin, direction)

        if material is None or recursion >= 3:  # break recursion of reflections after n iterations
            return self.background_color

        offset_normal = intersect.normal @ 1.1

        if material.albedo[2] > 0:
            reverse_direction = direction * -1
            reflect_dir = (reverse_direction, intersect.normal).reflect
            reflect_orig = (intersect.point -  offset_normal) if dot(reflect_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
            reflect_color = self.cast_ray(reflect_orig, reflect_dir, recursion + 1)
        else:
            reflect_color = color(0, 0, 0)

        light_dir = (self.light.position -  intersect.point).norm()
        light_distance = (self.light.position - intersect.point).length()

        shadow_orig = (intersect.point - offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        shadow_intensity = 0

        if shadow_material and (shadow_intersect.point -  shadow_orig).length() < light_distance:
            shadow_intensity = 0.9

        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

        reflection = (light_dir, intersect.normal).reflect()
        specular_intensity = self.light.intensity * (
        max(0, -dot(reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        reflection = reflect_color * material.albedo[2]

        return diffuse + specular + reflection
        
            

    def scene_intersect(self, origin, direction):
        zbuffer = 999999
        material = None
        intersect = None

        for o in self.scene:
            object_intersect = o.ray_intersect(origin, direction)
            if object_intersect:
                if object_intersect.distance < zbuffer:
                    zbuffer = object_intersect.distance
                    material = o.material
                    intersect = object_intersect
            
        return material, intersect


# IMPLEMENTACION
red = Material(diffuse=color(255, 0 , 0))
white = Material(diffuse=color(255, 255, 255))

# corregir
ivory = Material(diffuse=color(100, 100, 80), albedo=(0.6,  0.3, 0.1), spec=50)
rubber = Material(diffuse=color(80, 0, 0), albedo=(0.9,  0.1, 0), spec=10)
mirror = Material(diffuse=color(255, 255, 255), albedo=(0, 10, 0.8), spec=1425)
glass = Material(diffuse=color(150, 180, 200), albedo=[0,0.5,0.8])

r = Raytracer(800, 600)
r.light = Light(
  position=V3(-20, 20, 20),
  intensity=1.5
)
r.scene = [
    Sphere(V3(0, -1.5, -10), 1.5, ivory),
    Sphere(V3(0, 0, -5), 0.5, glass),
    Sphere(V3(1, 1, -8), 1.7, rubber),
    Sphere(V3(-2, 1, -10), 2, mirror),
]
r.render()
r.write('rt1.bmp')
