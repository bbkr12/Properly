import math
import random
import json
from pico2d import *
import Player
import Monster
import Game


class Item:
    image = None
    Death = False
    Speed = 150
    Power = 0
    x, y = 0, 100
    UpDwon = 1
    RightLeft = 1
    Type = 1 # 1 = 미사일 업그레이드 2 = 폭탄개수+1 3 = 폭탄개수 UI

    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.Type = Type

        if self.Type == 1:
            self.image = load_image('Resource/Item/Missileupgrade.png')

        else:
            self.image = load_image('Resource/Item/BoomPlus.png')

    def update(self, frame_time):
        if self.Type != 3:
            self.y += frame_time * self.Speed * self.UpDwon
            self.x += frame_time * self.Speed * self.RightLeft

            if self.y > 1000:
                self.UpDwon = -1
            if self.y < 10:
                self.UpDwon = 1

            if self.x < 5:
                self.RightLeft = 1
            if self.x > 795:
                self.RightLeft = -1



    def draw(self):
        self.image.clip_draw(0, 0, 38, 22, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.Type != 3:
            return self.x - 19, self.y - 11, self.x + 19, self.y + 11
        else:
            return 9999 - 19, 9999 - 11, 9999 + 19, 9999 + 11

