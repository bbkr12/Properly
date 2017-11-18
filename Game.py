# adjust_run_and_action.py : regulate run speed and action speed as well

import random
import json
from pico2d import *

running = None

class Field:
    Y = 0
    def __init__(self):
        self.image = load_image('Background.bmp')

    def update(self, frame_time):
        self.Y += frame_time * 200

        if self.Y > 8000:
            self.Y = 0

    def draw(self):
        self.image.draw(400, +4850 - 600 - self.Y)


class Boy:


    font = None
    image = None

    LEFT_RUN, RIGHT_RUN = 0, 1

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        #self.frame = random.randint(0, 7)
        #self.total_frames = 0.0
        #self.dir = 1
        #self.state = self.RIGHT_RUN
        self.image = load_image('Player.png')
        # fill here


    def update(self, frame_time):
        # fill here
        self.frame = 0



    def draw(self):
        # fill here
        #Boy.font.draw(self.x - 40, self.y + 50, 'Time : %3.2f' %get_time(), (255, 255, 0))
        #self.image.opacify(1)
        #self.image.clip_draw(self.frame * 64, self.state * 64, 64, 64, self.x, self.y + 150)
        self.image.clip_draw(225, 0, 75, 75, self.x, self.y)




class Bird:

    # fill here
    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 60.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    font = None
    image = None

    LEFT_RUN, RIGHT_RUN = 0, 1

    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = random.randint(0, 7)
        self.total_frames = 0.0
        self.dir = 1
        self.state = self.RIGHT_RUN
        if Bird.image == None:
            Bird.image = load_image('Bird.png')
        if Bird.font == None:
            Bird.font = load_font('ENCR10B.TTF', 16)
        # fill here


    def update(self, frame_time):
        # fill here
        distance = Bird.RUN_SPEED_PPS * frame_time
        self.total_frames += Bird.FRAMES_PER_ACTION * Bird.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        self.total_frames += 1.0
        self.frame = (self.frame + 1) % 8
        self.x += (self.dir * distance)

        if self.x > 960 :
            self.dir = -1
            self.x = 960
            self.state = self.LEFT_RUN
            print("Change Time : %f, Total Frames : %d" %(get_time(), self.total_frames))

        elif self.x < 0 :
            self.dir = 1
            self.x = 0
            self.state = self.RIGHT_RUN
            print("Change Time : %f, Total Frames : %d" %(get_time(), self.total_frames))


    def draw(self):
        # fill here
        Bird.font.draw(self.x - 40, self.y + 160, 'Time : %3.2f' %get_time(), (255, 255, 0))
        self.image.opacify(1)
        self.image.clip_draw(self.frame * 64, self.state * 64, 64, 64, self.x, self.y + 150)






# 여기서부터 실제 구동부이다.


def handle_events(frame_time):
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


current_time = 0.0


def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def main():

    open_canvas(800, 600)

    global running
    global current_time


    hero = Boy()
    bird = Bird()
    field = Field()

    running = True
    current_time = get_time()

    # 반복문
    while running:

        # Game Logic
        # Update
        frame_time = get_frame_time()
        handle_events(frame_time)
        field.update(frame_time)
        hero.update(frame_time)
        bird.update(frame_time)



        # Render
        clear_canvas()
        field.draw()
        hero.draw()
        bird.draw()
        update_canvas()


    close_canvas()


if __name__ == '__main__':
    main()