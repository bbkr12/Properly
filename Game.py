# adjust_run_and_action.py : regulate run speed and action speed as well

import math
import random
import json
from pico2d import *

running = None
PleyerBullet = []
MonsterBullet = []
BommBullet = []
BoomB = []
Mop = []



class Field:
    Y = 0
    def __init__(self):
        self.image = load_image('Background.bmp')

    def update(self, frame_time):
        self.Y += frame_time * 100

        if self.Y > 8000:
            self.Y = 0

    def draw(self):
        self.image.draw(400, +4850 - 600 - self.Y)



class Player:
    image = None
    BoomTime = 0
    Time = 0
    Speed = 300
    Sprite = 186
    Boom = False
    BoomSpriteX, BoomSpriteY = 0, 0
    RIGHT, LEFT, UP, DOWN = False, False, False, False

    LEFT_RUN, RIGHT_RUN = 0, 1

    def Key(self, frame_time):
        global PlayerBullet
        events = get_events()
        for event in events:
            if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
                self.RIGHT = True
            elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
                self.LEFT = True
            if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                self.UP = True
            elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
                self.DOWN= True

            if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
                self.RIGHT = False
                self.Sprite = 186
            elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
                self.LEFT = False
                self.Sprite = 186
            if event.type == SDL_KEYUP and event.key == SDLK_UP:
                self.UP = False
            elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
                self.DOWN= False

            if event.type == SDL_KEYDOWN and event.key == SDLK_a:
                PlayerBullet.append(MyBullet(self.x-1, self.y + 30))


            if event.type == SDL_KEYDOWN and event.key == SDLK_s:
                if self.Boom == False:
                    self.Boom = True
                    self.image = load_image('수정됨_Strike.png')
                    BoomBullet.append(Boom(False))

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        #self.frame = random.randint(0, 7)
        #self.total_frames = 0.0
        #self.dir = 1
        #self.state = self.RIGHT_RUN
        self.image = load_image('수정됨_Player.png')
        # fill here


    def update(self, frame_time):
        # fill here
        self.frame = 0
        self.Key(frame_time)
        #math.sqrt(100) #수학함수

        if self.Boom == True:
            self.BoomTime += frame_time
            if self.BoomTime > 0.05:
                if self.BoomSpriteX > 46:
                    self.BoomSpriteX = 0
                    self.image = load_image('수정됨_Player.png')
                    self.Boom = False

                self.BoomTime = 0
                self.BoomSpriteX += 1

            return


        self.Time += frame_time
        if self.Time > 0.1:
            self.Time = 0
            if self.RIGHT == True:
                self.Sprite += 62
                if self.Sprite >= 373:
                    self.Sprite = 373
            if self.LEFT == True:
                self.Sprite -= 62
                if self.Sprite <= 0:
                    self.Sprite = 0



        if self.RIGHT == True:
            self.x += frame_time * self.Speed
            if self.x >= 799:
                self.x = 799

        if self.LEFT == True:
            self.x -= frame_time * self.Speed
            if self.x <= 10:
                self.x = 10

        if self.UP == True:
            self.y += frame_time * self.Speed
            if self.y > 995:
                self.y = 995

        if self.DOWN == True:
            self.y -= frame_time * self.Speed
            if self.y < 5:
                self.y = 5


    def draw(self):
        # fill here
        #Boy.font.draw(self.x - 40, self.y + 50, 'Time : %3.2f' %get_time(), (255, 255, 0))
        #self.image.opacify(1)
        #self.image.clip_draw(self.frame * 64, self.state * 64, 64, 64, self.x, self.y + 150)
        if self.Boom == True:
            self.image.clip_draw(180 * self.BoomSpriteX, 0, 180, 398, self.x, self.y)
        else:
            self.image.clip_draw(self.Sprite, 0, 62, 96, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.Boom == False:
            return self.x - 15, self.y - 32.5, self.x + 15, self.y + 32.5
        else:
            return self.x+ 9999 - 15, self.y+ 9999 - 32.5, self.x+ 9999 + 15, self.y+ 9999 + 32.5

class MyBullet:
    image = None
    Death = False
    Speed = 900
    Power = 0
    x, y = 0, 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('PBullet.png')

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

    def __init__(self, Death):
        print("미사일 생성")
        self.image = load_image('Boom.png')
        self.Death = Death

    def update(self, frame_time):
        if self.Death == True:
            return


        self.Time += frame_time

        if self.Time < 3:
            self.LunchTime += frame_time
            self.Speed = 50

            if self.LunchTime > 0.1:
                self.LunchTime = 0
                BoomB.append(BBB(self.x, self.y + 120, 0))
                BoomB.append(BBB(self.x - 75, self.y + 50, 1))
                BoomB.append(BBB(self.x - 150, self.y, 2))
                BoomB.append(BBB(self.x + 75, self.y + 50, 3))
                BoomB.append(BBB(self.x + 150, self.y, 4))
        elif self.Time < 7:
            self.Speed = 0
            self.LunchTime += frame_time
            if self.LunchTime > 0.1:
                self.LunchTime = 0
                BoomB.append(BBB(self.x, self.y + 120, 0))
                BoomB.append(BBB(self.x - 75, self.y + 50, 1))
                BoomB.append(BBB(self.x - 150, self.y, 2))
                BoomB.append(BBB(self.x + 75, self.y + 50, 3))
                BoomB.append(BBB(self.x + 150, self.y, 4))
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
        self.image = load_image('BoomMis.png')

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
        return self.x - 5, self.y - 5, self.x + 5, self.y + 5


class MonBullet:
    image = None
    Death = False
    Speed = 400
    x, y = 0, 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('mBullet.jpg')

    def update(self, frame_time):
        self.y -= frame_time * self.Speed
        if self.y < 5:
            self.Death = True

    def draw(self):
        self.image.clip_draw(0, 0, 13, 13, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 5, self.y - 5, self.x + 5, self.y + 5

class Monster:
    Hp = 2
    image = None
    Death = False
    Destroy = False
    Time = 0;
    Sprite = 0
    Lunchtime = 0
    Type = 0
    def __init__(self,x , y, Type):
        self.Type = Type
        self.x, self.y = x, y
        if self.Type == 0:
            Monster.image = load_image('Monster.png')
        if self.Type == 1:
            Monster.image = load_image('RLMonster.png')
        if self.Type == 2:
            Monster.image = load_image('LRMonster.png')
        # fill here


    def update(self, frame_time):
        # fill here

        self.Lunchtime += frame_time
        if self.Lunchtime > 1:
            self.Lunchtime = 0
            #MonsterBullet.append(MonBullet(self.x, self.y))

        if self.Hp <= 0:
            self.Destroy = True
            self.Time += frame_time
            if self.Time > 0.1:
                self.Time = 0
                self.Sprite += 60

            if self.Sprite >= 660:
                self.Death = True

        if self.Destroy == True:
            self.image = load_image('Destory.png')




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
    PlayerBullet = [MyBullet(9000, 300)]
    MonsterBullet = [MonBullet(-10, 300)]
    BoomB = [BBB(1000, 1000, 0)]
    BoomBullet = [Boom(True)]

    Progress = 0

    Mop = [Monster(100 + (i * 100), 900, 0) for i in range(0, 7)]
    hero = Player()
    field = Field()

    running = True
    current_time = get_time()

    # 반복문
    while running:

        # Game Logic
        # Update
        frame_time = get_frame_time()
        Progress += frame_time
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