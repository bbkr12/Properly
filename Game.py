# adjust_run_and_action.py : regulate run speed and action speed as well

import math
import random
import json
from pico2d import *
import Player
import Bullet
import Monster

running = None
PlayerBullet = []
MonsterBullet = []
BoomBullet = []
BoomB = []
Mop = []
hero = None



class Field:
    Y = 0
    def __init__(self):
        self.image = load_image('Resource/Map/Background.bmp')

    def update(self, frame_time):
        self.Y += frame_time * 100

        if self.Y > 8000:
            self.Y = 0

    def draw(self):
        self.image.draw(400, +4850 - 600 - self.Y)


# 여기서부터 실제 구동부이다.


def Collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def Distance(a, b):
    Width = a.x - b.x
    Height = a.y - b.y
    Dis = math.sqrt((Width * Width) + (Height * Height))
    return Dis



current_time = 0.0
Progress = 0



def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def main():

    open_canvas(800, 1000)

    global running
    global current_time
    global Progress
    global PlayerBullet
    global BoomBullet
    global Mop
    global MonsterBullet
    global BoomB
    global hero
    PlayerBullet = [Bullet.MyBullet(9000, 300)]
    MonsterBullet = [Bullet.MonBullet(-10, -999, -90)]
    BoomB = [Bullet.BBB(1000, 1000, 0)]
    BoomBullet = [Bullet.Boom(True, BoomB)]

    Progress = 0


    hero = Player.Player(PlayerBullet, BoomBullet, BoomB)
    field = Field()


    running = True
    current_time = get_time()
    #Mop = [Monster(400, 600, 1, hero) for i in range(0, 2)]
    # 반복문
    while running:

        #print(current_time)

        if current_time > 3 and Progress == 0:
            Mop = [Monster.Monster(800 + (i * 100), 1000 + (i * 100), 1, hero, MonsterBullet) for i in range(0, 5)]
            Progress += 1

        if current_time > 8 and Progress == 1:
            Mop = [Monster.Monster(0 - (i * 100), 1000 + (i * 100), 2, hero, MonsterBullet) for i in range(0, 5)]
            Progress += 1


        # Game Logic
        # Update
        frame_time = get_frame_time()
        #handle_events(frame_time)
        field.update(frame_time)
        hero.update(frame_time)

        for mBullet in MonsterBullet:
            mBullet.update(frame_time)
            if mBullet.Death == True:
                MonsterBullet.remove(mBullet)

        for bBullet in BoomB:
            bBullet.update(frame_time)
            if bBullet .Death == True:
                BoomB.remove(bBullet )

        for mBullet in BoomBullet:
            mBullet.update(frame_time)
            if mBullet.Death == True:
                BoomBullet.remove(mBullet)

        for pBullet in PlayerBullet:
            pBullet.update(frame_time)
            if pBullet.Death == True:
                PlayerBullet.remove(pBullet)



        for mop in Mop:
            mop.update(frame_time)
            if mop.Death == True:
                Mop.remove(mop)
            for pBullet in PlayerBullet:
                if Collide(pBullet, mop) :
                    mop.Hp -= 1 + pBullet.Power
                    PlayerBullet.remove(pBullet)

        for pBullet in MonsterBullet:
            if Collide(pBullet, hero):
                MonsterBullet.remove(pBullet)


        # Render
        clear_canvas()
        field.draw()


        for mBullet in MonsterBullet:
            mBullet.draw()
        for mop in Mop:
            mop.draw()

        for bBullet in BoomB:
            bBullet.draw()

        for mBullet in BoomBullet:
            mBullet.draw()



        hero.draw()
        for pBullet in PlayerBullet:
            pBullet.draw()


        update_canvas()



    close_canvas()


if __name__ == '__main__':
    main()