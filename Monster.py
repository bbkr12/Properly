import math
import random
import json
from pico2d import *
import Player
import Game
import Bullet

class Monster:
    Hp = 2
    image = None
    Death = False
    Destroy = False
    Time = 0;
    Sprite = 0
    Lunchtime = 0
    Type = 0
    Speed = 300
    hero = None
    Width = 0
    Height = 0
    Dis = 0
    Angle = 0
    MonsterBullet = None
    Red = False


    def __init__(self,x , y, Type, hero, MonsterBullet):
        self.Type = Type
        self.x, self.y = x, y

        if self.Type == 0:
                Monster.image = load_image("Resource/Monster/Monster.png")
        if self.Type == 1:
            if self.Red == True:
                Monster.image = load_image("Resource/Monster/RLMonster_Red.png")
            else:
                Monster.image = load_image("Resource/Monster/RLMonster.png")
        if self.Type == 2:
            if self.Red == True:
                Monster.image = load_image("Resource/Monster/LRMonster_Red.png")
            else:
                Monster.image = load_image("Resource/Monster/LRMonster.png")

        self.hero = hero;
        self.MonsterBullet = MonsterBullet
        # fill here


    def update(self, frame_time):
        #죽음
        if self.Hp <= 0:
            if self.Destroy == False:
                self.Destroy = True
                self.image = load_image('Resource/Effect/Destory.png')
            self.Time += frame_time
            if self.Time > 0.1:
                self.Time = 0
                self.Sprite += 60

            if self.Sprite >= 660:
                self.Death = True
            return

#############################################################################################

        # 타입별 AI
        if self.Type == 1:
            self.x -= frame_time * self.Speed;
            self.y -= frame_time * self.Speed;
            if self.y < -50:
                self.Death = True;

            if self.x < -50:
                self.Death = True

        elif self.Type == 2:
            self.x += frame_time * self.Speed;
            self.y -= frame_time * self.Speed;
            if self.y < -50:
                self.Death = True;

            if self.x > 850:
                self.Death = True


        #몬스터 공통사항
        self.Height = self.hero.y - self.y
        self.Width = self.hero.x - self.x
        self.Dis = math.sqrt((self.Width * self.Width) + (self.Height * self.Height))
        self.Angle = math.acos(self.Width / self.Dis)
        if (self.hero.y >= self.y):
            self.Angle = 2 * 3.141592 - self.Angle
        self.Lunchtime += frame_time
        if self.Lunchtime > 2.2:
            self.Lunchtime = 0
            self.MonsterBullet.append(Bullet.MonBullet(self.x, self.y, self.Angle))


    def draw(self):
        # fill here
        if self.Destroy == False:
            self.image.clip_draw(0, 0, 82, 82, self.x, self.y)
        else:
            self.image.clip_draw(self.Sprite, 0, 60, 54, self.x, self.y)

        draw_rectangle(*self.get_bb())
    def get_bb(self):
        if self.Destroy == False:
            return self.x - 31, self.y - 10, self.x + 31, self.y + 10
        else:
            return 9999 - 31, 9999 - 10, 9999 + 31, 9999 + 10
