import math
import random
import json
from pico2d import *
import Player
import Monster
import Game


class MyBullet:
    image = None
    Death = False
    Speed = 900
    Power = 0
    x, y = 0, 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('Resource/Missile/PBullet.png')

    def update(self, frame_time):
        self.y += frame_time * self.Speed
        if self.y > 995:
            self.Death = True

    def draw(self):
        self.image.clip_draw(self.Power, 0, 15, 28, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 5, self.y - 5, self.x + 5, self.y + 5

class Boom:
    image = None
    Death = False
    Speed = 100
    x, y = 400, 0
    LunchTime = 0
    Time = 0
    BoomB = None

    def __init__(self, Death, BoomB):
        print("미사일 생성")
        self.image = load_image('Resource/Effect/Boom.png')
        self.Death = Death
        self.BoomB = BoomB

    def update(self, frame_time):
        if self.Death == True:
            return


        self.Time += frame_time

        if self.Time < 3:
            self.LunchTime += frame_time
            self.Speed = 50

            if self.LunchTime > 0.1:
                self.LunchTime = 0
                self.BoomB.append(BBB(self.x, self.y + 120, 0))
                self.BoomB.append(BBB(self.x - 75, self.y + 50, 1))
                self.BoomB.append(BBB(self.x - 150, self.y, 2))
                self.BoomB.append(BBB(self.x + 75, self.y + 50, 3))
                self.BoomB.append(BBB(self.x + 150, self.y, 4))
        elif self.Time < 7:
            self.Speed = 0
            self.LunchTime += frame_time
            if self.LunchTime > 0.1:
                self.LunchTime = 0
                self.BoomB.append(BBB(self.x, self.y + 120, 0))
                self.BoomB.append(BBB(self.x - 75, self.y + 50, 1))
                self.BoomB.append(BBB(self.x - 150, self.y, 2))
                self.BoomB.append(BBB(self.x + 75, self.y + 50, 3))
                self.BoomB.append(BBB(self.x + 150, self.y, 4))
        elif self.Time > 7:
            self.Speed = 600

        self.y += frame_time * self.Speed
        if self.y > 1100:
            self.Death = True

    def draw(self):
        self.image.clip_draw(0, 0, 500, 250, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 250, self.y - 125, self.x + 250, self.y + 10

class BBB:
    image = None
    Death = False
    Speed = 700
    Postion = 0
    x, y = 0, 100
    Time = 0
    Sprite = 0

    def __init__(self, x, y, Postion):
        self.Postion = Postion
        self.x = x
        self.y = y
        self.image = load_image('Resource/Missile/BoomMis.png')

    def update(self, frame_time):

        if self.Postion == 0:
            self.y += frame_time * self.Speed
        elif self.Postion == 1:
            self.x -= frame_time * (self.Speed/4)
            self.y += frame_time * self.Speed

        elif self.Postion == 3:
            self.x += frame_time * (self.Speed / 4)
            self.y += frame_time * self.Speed

        elif self.Postion == 2:
            self.x -= frame_time * (self.Speed/2)
            self.y += frame_time * self.Speed

        elif self.Postion == 4:
            self.x += frame_time * (self.Speed / 2)
            self.y += frame_time * self.Speed


        if self.y > 1000:
            self.Death = True

        self.Time += frame_time
        if self.Time > 0.1:
            self.Time = 0
            self.Sprite += 1
            if self.Sprite > 2:
                self.Sprite = 0

    def draw(self):
        self.image.clip_draw(36 * self.Sprite, 0, 36, 38, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10


class MonBullet:
    image = None
    Death = False
    Speed = 400
    x, y = 0, 100
    Angle = 0

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.image = load_image('Resource/Missile/mBullet.jpg')
        self.Angle = angle

    def update(self, frame_time):
        self.y -= math.sin(self.Angle) * frame_time * self.Speed
        self.x += math.cos(self.Angle) * frame_time * self.Speed
        if self.y < 5:
            self.Death = True

    def draw(self):
        self.image.clip_draw(0, 0, 13, 13, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 5, self.y - 5, self.x + 5, self.y + 5