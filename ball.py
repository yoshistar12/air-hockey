from vector import *

# I denne filen setter vi fram noen egenskaper av en airhockey "ball"

d_mass = 0.50
d_rad = 40

class Ball:
    def __init__(self, pos, vel = Vector(0, 0), acc = Vector(0, 0), mass = 0.5, rad = 15.83):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = mass
        self.rad = rad
        self.is_checked = False
    def speed(self):
        return self.vel.mag()
    def dir(self):
        return self.vel.normalize()
    def mom(self):
        return self.mass * self.speed()

