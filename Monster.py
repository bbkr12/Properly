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
    BoosLunchTime = 0
    MiddleLunch = 0
    Type = 0
    Speed = 300
    hero = None
    Width = 0
    Height = 0
    Dis = 0
    Angle = 0
    MonsterBullet = None
    Red = False
    MonsterDestorySound = None




    BossPattern = 0
    BossPatternTime = 0
    Right = 1
    Right2 = 1
    Right3 = 1

    AddAngle = 0
    AddAngle2 = 90
    AddAngle3 = 180

    Weigh = 0

    def __init__(self,x , y, Type, hero, MonsterBullet):
        self.Type = Type
        self.x, self.y = x, y

        if self.Type == 0:
            self.image = load_image("Resource/Monster/Monster.png")

        elif self.Type == 1:
            self.image = load_image("Resource/Monster/RLMonster.png")

        elif self.Type == 2:
            self.image = load_image("Resource/Monster/LRMonster.png")

        elif self.Type == 3:
            self.image = load_image("Resource/Monster/MiddleBoss.png")
            self.Hp = 100

        elif self.Type == 4:
            self.image = load_image("Resource/Boss/boss.png")
            self.Hp = 800


        self.MonsterDestorySound = load_wav('Sound/explosion.wav')
        self.MonsterDestorySound.set_volume(32)

        self.hero = hero;
        self.MonsterBullet = MonsterBullet
        # fill here


    def update(self, frame_time):
        #죽음
        if self.Hp <= 0:
            if self.Type == 0 or self.Type == 1 or self.Type == 2:
                if self.Destroy == False:
                    self.Destroy = True
                    self.image = load_image('Resource/Effect/Destory.png')
                    #self.MonsterDestorySound.play()
                self.Time += frame_time
                if self.Time > 0.1:
                    self.Time = 0
                    self.Sprite += 60

                if self.Sprite >= 660:
                    self.Death = True
                return

            elif self.Type == 3 or self.Type == 4:
                if self.Destroy == False:
                    self.Destroy = True
                    self.image = load_image('Resource/Effect/Destory_large.png')
                self.Time += frame_time
                if self.Time > 0.1:
                    self.Time = 0
                    self.Sprite += 120

                if self.Sprite >= 1320:
                    self.Death = True
                return

#############################################################################################

        # 타입별 AI
        if self.Type == 1: #RL몬스터
            self.x -= frame_time * self.Speed
            self.y -= frame_time * self.Speed
            if self.y < -50:
                self.Death = True
            if self.x < -50:
                self.Death = True

        elif self.Type == 2: # LR 몬스터
            self.x += frame_time * self.Speed
            self.y -= frame_time * self.Speed
            if self.y < -50:
                self.Death = True
            if self.x > 850:
                self.Death = True

        elif self.Type == 0: # 직선 몬스터
            self.y -= frame_time * self.Speed / 1.5
            if self.y < -50:
                self.Death = True

        elif self.Type == 3: # 중간보스
            self.y += frame_time * self.Speed / 5
            self.x += frame_time * self.Speed * self.Right / 3
            self.MiddleLunch += frame_time
            if self.Right == 1:
                if self.x > 225:
                    self.x = 225

            elif self.Right == -1:
                if self.x < 575:
                    self.x = 575

            if self.y > 900:
                self.y = 900

        elif self.Type == 4:  #\보스
            self.y -= frame_time * self.Speed / 5
            self.MiddleLunch += frame_time
            if self.y < 800:
                self.y = 800




        #몬스터 공통사항
        self.Height = self.hero.y - self.y
        self.Width = self.hero.x - self.x
        self.Dis = math.sqrt((self.Width * self.Width) + (self.Height * self.Height))
        self.Angle = math.acos(self.Width / self.Dis)
        if (self.hero.y >= self.y):
            self.Angle = 2 * 3.141592 - self.Angle
        self.Lunchtime += frame_time

        if self.Type == 4:
            self.BossPatternTime += frame_time;


        if self.BossPatternTime > 5:
            self.BossPatternTime = 0
            self.AddAngle = 0
            self.AddAngle2 = 90
            self.AddAngle3 = 180
            Temp = self.BossPattern
            self.BossPattern = random.randint(0, 2)


            if self.BossPattern == 2:
                self.BoosLunchTime = 2

        self.BoosLunchTime += frame_time;

        if self.BossPattern == 0:
            if self.Type == 4 and self.BoosLunchTime > 0.05:
                self.BoosLunchTime = 0
                self.AddAngle += 5;
                if self.AddAngle > 360:
                    self.AddAngle = 0
                self.MonsterBullet.append(Bullet.MonBossBullet(self.x, self.y, math.radians(0 + self.AddAngle)))
                self.MonsterBullet.append(Bullet.MonBossBullet(self.x, self.y, math.radians(120 + self.AddAngle)))
                self.MonsterBullet.append(Bullet.MonBossBullet(self.x, self.y, math.radians(240 + self.AddAngle)))

        elif self.BossPattern == 1:
            if self.Type == 4 and self.BoosLunchTime > 0.05:
                self.BoosLunchTime = 0


                self.AddAngle += 5 * self.Right;
                #if self.AddAngle > 270 or self.AddAngle < 91:
                    #self.Right *= -1


                self.AddAngle2 += 5 * self.Right2;
                #if self.AddAngle2 > 360 or self.AddAngle2 < 1:
                    #self.Right2 *= -1

                self.AddAngle3 += 5 * self.Right3;
                #if self.AddAngle3 > 360 or self.AddAngle3 < 1:
                    #self.Right3 *= -1


                self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90 + self.AddAngle)))
                self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90 +-self.AddAngle)))

                self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90 + self.AddAngle2)))
                self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90 -self.AddAngle2)))

                self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90 + self.AddAngle3)))
                self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians( 90 -self.AddAngle3)))

        elif self.BossPattern == 2:
            if self.Type == 4 and self.BoosLunchTime > 2:
                self.BoosLunchTime = 0
                #self.Weigh += frame_time * 1000

                for i in range(0, 20):
                        self.MonsterBullet.append(Bullet.SpecialBullet(self.x + math.cos(math.radians(108)) * (i * 10) , self.y + 50 - math.sin(math.radians(108)) * (i * 10), math.radians( 108 + (i * 10))))

                for i in range(0, 20):
                    X1 = self.x + math.cos(math.radians(108)) * (19 * 10)
                    Y1 = self.y + 50 - math.sin(math.radians(108)) * (19 * 10)
                    self.MonsterBullet.append(Bullet.SpecialBullet(X1 + math.cos(math.radians(324)) * (i * 10),Y1 - math.sin(math.radians(324)) * (i * 10) ,math.radians( 324 + (i * 10))))

                for i in range(0, 20):
                    X2 =  X1 + math.cos(math.radians(324)) * (19 * 10)
                    Y2 =  Y1 - math.sin(math.radians(324)) * (19 * 10)
                    self.MonsterBullet.append(Bullet.SpecialBullet(X2 + math.cos(math.radians(180)) * (i * 10),Y2 - math.sin(math.radians(180)) * (i * 10),math.radians( 180 + (i * 10))))

                for i in range(0, 20):
                    X3 = X2 + math.cos(math.radians(180)) * (19 * 10)
                    Y3 = Y2 - math.sin(math.radians(180)) * (19 * 10)
                    self.MonsterBullet.append(Bullet.SpecialBullet(X3 + math.cos(math.radians(36)) * (i * 10),Y3 - math.sin(math.radians(36)) * (i * 10), math.radians( 36 + (i * 10))))

                for i in range(0, 20):
                    X4 = X3 + math.cos(math.radians(36)) * (19 * 10)
                    Y4 = Y3 - math.sin(math.radians(36)) * (19 * 10)
                    self.MonsterBullet.append(Bullet.SpecialBullet(X4 + math.cos(math.radians(252)) * (i * 10), Y4 - math.sin(math.radians(252)) * (i * 10), math.radians( 252 + (i * 10))))






                for i in range(0, 20):
                       self.MonsterBullet.append(Bullet.SpecialBullet(self.x + math.cos(math.radians(-108)) * (i * 20) , self.y - 250 - math.sin(math.radians(-108)) * (i * 20), math.radians( -108 + (i * 20))))

                for i in range(0, 20):
                   X1 = self.x + math.cos(math.radians(-108)) * (19 * 20)
                   Y1 = self.y - 250 - math.sin(math.radians(-108)) * (19 * 20)
                   self.MonsterBullet.append(Bullet.SpecialBullet(X1 + math.cos(math.radians(-324)) * (i * 20),Y1 - math.sin(math.radians(-324)) * (i * 20) ,math.radians( -324 + (i * 20))))

                for i in range(0, 20):
                   X2 =  X1 + math.cos(math.radians(-324)) * (19 * 20)
                   Y2 =  Y1 - math.sin(math.radians(-324)) * (19 * 20)
                   self.MonsterBullet.append(Bullet.SpecialBullet(X2 + math.cos(math.radians(-180)) * (i * 20),Y2 - math.sin(math.radians(-180)) * (i * 20),math.radians( -180 + (i * 20))))

                for i in range(0, 20):
                   X3 = X2 + math.cos(math.radians(-180)) * (19 * 20)
                   Y3 = Y2 - math.sin(math.radians(-180)) * (19 * 20)
                   self.MonsterBullet.append(Bullet.SpecialBullet(X3 + math.cos(math.radians(-36)) * (i * 20),Y3 - math.sin(math.radians(-36)) * (i * 20), math.radians( -36 + (i * 20))))


                for i in range(0, 20):
                   X4 = X3 + math.cos(math.radians(-36)) * (19 * 20)
                   Y4 = Y3 - math.sin(math.radians(-36)) * (19 * 20)
                   self.MonsterBullet.append(Bullet.SpecialBullet(X4 + math.cos(math.radians(-252)) * (i * 20), Y4 - math.sin(math.radians(-252)) * (i * 20), math.radians( -252 + (i * 20))))



                    # self.y -= math.sin(self.Angle) * frame_time * self.Speed
                    # self.x += math.cos(self.Angle)


        if self.Lunchtime > 1 and self.Type != 0:
            self.Lunchtime = 0
            if self.Type == 3:
                self.MonsterBullet.append(Bullet.MonBullet(self.x, self.y-50, self.Angle))
                #패턴미사일
                if self.MiddleLunch > 3:
                    self.MiddleLunch = 0
                    if self.Right == 1:
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(10)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(20)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(30)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(40)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(50)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(60)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(80)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(90)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(100)))

                    else:
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(10) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(20) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(30) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(40) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(50) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(60) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(70) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(80) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(90) + math.radians(70)))
                        self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(100) + math.radians(70)))

            elif self.Type == 4:
                self.MonsterBullet.append(Bullet.MonBullet(self.x, self.y - 50, self.Angle))
                if self.MiddleLunch > 2 and self.BossPattern == 0:
                    self.MiddleLunch = 0
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(10)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(20)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(30)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(40)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(50)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(60)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(80)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(90)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(100)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(10) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(20) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(30) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(40) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(50) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(60) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(70) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(80) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(90) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y - 50, math.radians(100) + math.radians(70)))

                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(10)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(20)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(30)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(40)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(50)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(60)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(80)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(100)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(10) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(20) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(30) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(40) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(50) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(60) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(70) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(80) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(90) + math.radians(70)))
                    self.MonsterBullet.append(Bullet.MonMiddleBullet(self.x, self.y, math.radians(100) + math.radians(70)))








            else:
                self.MonsterBullet.append(Bullet.MonBullet(self.x, self.y, self.Angle))

        elif self.Lunchtime > 2 and self.Type == 0:
            self.Lunchtime = 0
            if self.y < 1000 and self.Type != 4:
                self.MonsterBullet.append(Bullet.MonBullet(self.x, self.y, self.Angle))


    def draw(self):
        # fill here
        if self.Destroy == False:
            if self.Type == 0 or self.Type == 1 or self.Type == 2:
                self.image.clip_draw(0, 0, 82, 82, self.x, self.y)
            elif self.Type == 3:
                self.image.clip_draw(0, 0, 177, 180, self.x, self.y)
            elif self.Type == 4:
                self.image.clip_draw(0, 0, 800, 480, self.x - 10, self.y)

        else:
            if self.Type == 0 or self.Type == 1 or self.Type == 2:
                self.image.clip_draw(self.Sprite, 0, 60, 54, self.x, self.y)
            elif self.Type == 3:
                self.image.clip_draw(self.Sprite, 0, 120, 108, self.x, self.y)
            elif self.Type == 4:
                self.image.clip_draw(self.Sprite, 0, 120, 108, self.x, self.y)
                print("보스 그림")




        #draw_rectangle(*self.get_bb())
    def  get_bb(self):
        if self.Destroy == False:
            if self.Type == 3:
                return self.x - 31, self.y - 31, self.x + 31, self.y + 31

            elif self.Type == 4:
                return self.x - 300, self.y + 10, self.x + 300, self.y + 100
            else:
                return self.x - 31, self.y - 10, self.x + 31, self.y + 10
        else:
            return 9999 - 31, 9999 - 10, 9999 + 31, 9999 + 10
