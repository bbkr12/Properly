# adjust_run_and_action.py : regulate run speed and action speed as well

import math
import random
import json
from pico2d import *
import Player
import Bullet
import Monster
import Item

running = None
PlayerBullet = [] # 플레이어의 탄환 리스트 컨테이너
MonsterBullet = [] # 몬스터의 탄환 리스트 컨테이너
BoomBullet = [] # 플레이어의 폭탄 리스트 컨테이너
BoomB = [] # 폭탄의 탄환 리스트 컨테이너
Mop = [] # 몬스터 리스트 컨테이너
ITEM = []
BoomCount = []
Life = []
hero = None # 플레이어
LogoScene = None


ItemSound = None
MonsterDestorySound = None
Hit = None


class Title:
    Y = 0
    BGM = None
    Title = True
    Time = 0
    def __init__(self):
        self.x = 400
        self.y = 500
        self.image = load_image('Resource/Title/Logo.png')

    def update(self, frame_time):

        self.Time += frame_time
        if self.Time > 2 and self.Time < 2.1:
            self.image = load_image('Resource/Title/title.png')

        elif self.Time > 2.2:
            events = get_events()
            for event in events:
                if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                    self.Title = False


    def Render(self):
        self.image.draw(self.x, self.y)



class Field:
    Y = 0
    BGM = None
    Tile = True
    def __init__(self):
        self.image = load_image('Resource/Map/Background.bmp')
        self.BGM = load_music('Sound/BGM2.mp3')
        self.BGM.set_volume(30)
        self.BGM.repeat_play()

    def update(self, frame_time):
        self.Y += frame_time * 70

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



current_time = 0.0 # 진행 시간
Progress = 0 # 진행 단계
ProgressTime = 0.0



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
    global ProgressTime
    global ITEM
    global BoomCount
    global Timer
    global ItemSound
    global Hit
    global MonsterDestorySound
    global LogoScene

    LogoScene = Title()


    while True:
        clear_canvas()
        frame_time = get_frame_time()
        LogoScene.update(frame_time)
        LogoScene.Render()
        update_canvas()
        if LogoScene.Title == False:
            break;







    PlayerBullet = [Bullet.MyBullet(9000, 300, 1)]
    MonsterBullet = [Bullet.MonBullet(-10, -999, -90)]
    BoomB = [Bullet.BBB(1000, 1000, 0)]
    BoomBullet = [Bullet.Boom(True, BoomB)]
    ITEM = [Item.Item( 400, 500, 1)]

    BoomCount = [Item.Item(50, 50, 3)]
    BoomCount.append(Item.Item(100, 50, 3))
    BoomCount.append(Item.Item(150, 50, 3))

    for i in range(0 , 10):
        Life.append(Item.Item(50 + (i * 50), 900, 4))


    Progress = 0

    hero = Player.Player(PlayerBullet, BoomBullet, BoomB)
    field = Field()


    running = True
    current_time = get_time()
    ProgressTime = get_time()

    ItemSound = load_wav('Sound/missile up.wav')
    ItemSound.set_volume(32)

    Hit = load_wav('Sound/hit.wav')
    Hit.set_volume(32)

    Timer = 0
    #Mop = [Monster(400, 600, 1, hero) for i in range(0, 2)]
    # 반복문

    #Progress = 3
    #ProgressTime += 20
    #current_time = 80
    #Progress = 13
    while running:
        ProgressTime += ProgressTime
        #######################################################
        #Game Progress
        if current_time > 3 and Progress == 0:
            Mop = [Monster.Monster(800 + (i * 100), 1000 + (i * 100), 1, hero, MonsterBullet) for i in range(0, 5)]
            Mop[4].Red = True
            Mop[4].image = load_image("Resource/Monster/RLMonster_Red.png")
            Progress += 1

        elif current_time > 8 and Progress == 1:
            Mop = [Monster.Monster(0 - (i * 100), 1000 + (i * 100), 2, hero, MonsterBullet) for i in range(0, 5)]
            Mop[4].Red = True
            Mop[4].image = load_image("Resource/Monster/LRMonster_Red.png")
            Progress += 1

        elif current_time > 12 and Progress == 2:
            Mop = [Monster.Monster(random.randint(50, 750), random.randint(1000, 2000), 0, hero, MonsterBullet) for i in range(0, 40)]
            Mop[4].Red = True
            Mop[4].image = load_image("Resource/Monster/Monster_Red.png")
            Progress += 1


        elif current_time > 18 and Progress == 3:
            for i in range(0, 20):
                Mop.append(Monster.Monster(random.randint(50, 750), random.randint(1000, 1400), 0, hero, MonsterBullet))
            Progress += 1


        elif current_time > 30 and Progress == 4:
            Mop = [Monster.Monster(800 + (i * 100), 1000 + (i * 100), 1, hero, MonsterBullet) for i in range(0, 5)]
            Progress += 1

        elif current_time > 35 and Progress == 5:
            Mop = [Monster.Monster(0 - (i * 100), 1000 + (i * 100), 2, hero, MonsterBullet) for i in range(0, 5)]
            Progress += 1


        elif current_time > 42 and Progress == 6:
            Mop.append(Monster.Monster(0, 750, 3, hero, MonsterBullet))
            Mop.append(Monster.Monster(800, 750, 3, hero, MonsterBullet))
            Mop[-1].Right = -1
            Progress += 1

        elif current_time > 45 and Progress == 7:
            for i in range(0, 10):
                Mop.append(Monster.Monster(random.randint(50, 750), random.randint(1000, 1400), 0, hero, MonsterBullet))

            Progress += 1


        elif current_time > 52 and Progress == 8:
            for i in range(0, 10):
                Mop.append(Monster.Monster(random.randint(50, 750), random.randint(1000, 1400), 0, hero, MonsterBullet))
            Progress += 1


        elif current_time > 59 and Progress == 9:
            for i in range(0, 10):
                Mop.append(Monster.Monster(random.randint(50, 750), random.randint(1000, 1400), 0, hero, MonsterBullet))
            Progress += 1

        elif current_time > 66 and Progress == 10:
            for i in range(0, 10):
                Mop.append(Monster.Monster(random.randint(50, 750), random.randint(1000, 1400), 0, hero, MonsterBullet))
            Progress += 1


        elif Progress == 11:
            index = 0;
            for i in Mop:
                index += 1;

            if index == 0:
                Timer = current_time
                Progress += 1


        elif current_time > Timer + 1 and Progress == 12:
                Mop.append(Monster.Monster(400, 1200, 4, hero, MonsterBullet))
                Progress += 1




        ######################################################

        # Update
        frame_time = get_frame_time()
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
                if mop.Red == True:
                    if mop.Type == 1 or mop.Type == 2:
                        print("아이템생성")
                        ITEM.append(Item.Item(mop.x, mop.y, 1))
                    else:
                        ITEM.append(Item.Item(mop.x, mop.y, 2))
                Mop.remove(mop)


        for item in ITEM:
            item.update(frame_time)






        #Collide
        for mop in Mop: # 몬스터 <-> 플레이어 총알
            for pBullet in PlayerBullet:
                if Collide(pBullet, mop) :
                    mop.Hp -= pBullet.Power
                    Hit.play()
                    PlayerBullet.remove(pBullet)

        for mop in Mop: # 몬스터 <-> 폭탄의 총알
            for boomb in BoomB:
                if Collide(boomb, mop) :
                    mop.Hp -= 1
                    BoomB.remove(boomb)
                    Hit.play()

        for mop in Mop: # 몬스터 <-> 폭탄
            for boombullet in BoomBullet:
                if Collide(boombullet, mop):
                    mop.Hp -= 1

        for pBullet in MonsterBullet: # 몬스터 총알 <-> 플레이어
            if Collide(pBullet, hero):
                MonsterBullet.remove(pBullet)
                if hero.Death == False and hero.PlayerLife != 0:
                    hero.PlayerLife -= 1
                    hero.Death = True
                    hero.DeathTime = 0
                    hero.x = 400
                    hero.y = 100
                    if hero.PlayerLife < 0:
                        hero.PlayerLife = 0

        for pBullet in MonsterBullet: # 폭탄 <-> 몬스터 총알
            for boombullet in BoomBullet:
                if Collide(pBullet, boombullet):
                    MonsterBullet.remove(pBullet)

        for item in ITEM:  # 아이템 <-> 플레이어
            if Collide(item, hero):
                if item.Type == 1:
                    hero.Power += 1
                    ItemSound.play()
                elif item.Type == 2:
                    hero.BoomCount += 1
                    ItemSound.play()
                ITEM.remove(item)






        # Render
        clear_canvas()
        field.draw()


        for mop in Mop:
            mop.draw()

        for mBullet in MonsterBullet:
            mBullet.draw()

        for bBullet in BoomB:
            bBullet.draw()

        for mBullet in BoomBullet:
            mBullet.draw()

        for pBullet in PlayerBullet:
            pBullet.draw()



        for item in ITEM:
            item.draw()

        for i in range(0,hero.BoomCount):
            BoomCount[i].draw()

        for i in range(0,hero.PlayerLife):
            Life[i].draw()


        hero.draw()

        update_canvas()



    close_canvas()


if __name__ == '__main__':
    main()