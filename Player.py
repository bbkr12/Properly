import math
import random
import json
from pico2d import *
import Game
import Bullet

class Player:
    image = None
    BoomTime = 0
    Time = 0
    Speed = 300
    Sprite = 186
    Boom = False
    BoomSpriteX, BoomSpriteY = 0, 0
    PlayerBullet = None
    BoomBullet = None
    BoomB = None
    RIGHT, LEFT, UP, DOWN = False, False, False, False

    LEFT_RUN, RIGHT_RUN = 0, 1

    def Key(self, frame_time):

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
                self.PlayerBullet.append(Bullet.MyBullet(self.x-1, self.y + 30))


            if event.type == SDL_KEYDOWN and event.key == SDLK_s:
                if self.Boom == False:
                    self.Boom = True
                    self.image = load_image('Resource/Effect/수정됨_Strike.png')
                    self.BoomBullet.append(Bullet.Boom(False, self.BoomB))

    def __init__(self, PlayerBullet, BoomBullet, BoomB):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('Resource/Player/수정됨_Player.png')
        self.PlayerBullet = PlayerBullet
        self.BoomBullet = BoomBullet
        self.BoomB = BoomB
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
                    self.image = load_image('Resource/Player/수정됨_Player.png')
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
