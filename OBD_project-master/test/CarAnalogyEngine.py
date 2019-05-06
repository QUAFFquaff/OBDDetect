#!/usr/bin/env python

# encoding: utf-8

'''

@author: Quaff

@contact: Quaff.lyu@gmail.com

@file: CarAnalogyEngine.py

@time: 2019/1/17 18:40

@desc:

'''
import pygame, sys
import time
import numpy as np


def testCarAnalogyEngine():
    pygame.init()
    vInfo = pygame.display.Info()
    size = width, height = vInfo.current_w, vInfo.current_h
    # size = width, height = 600, 400
    speed = [0, 0]
    BLACK = 0, 0, 0
    screen = pygame.display.set_mode(size)
    # screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    # screen = pygame.display.set_mode(size, pygame.NOFRAME)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption('Analogy')
    # ball = pygame.image.load("PYG02-ball.gif")

    ball = pygame.image.load("tire.png")
    ballrect = ball.get_rect()
    ballWidth = ball.get_rect()[2]
    ballHeight = ball.get_rect()[3]

    ballrect = ballrect.move(width/2-ballWidth/2, height/2)
    fps = 300
    fclock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speed[0] -= 1
                    # speed[0] = speed[0] if speed[0] == 0 else (abs(speed[0]) - 1) * int(speed[0] / abs(speed[0]))
                elif event.key == pygame.K_RIGHT:
                    speed[0] += 1
                    # speed[0] = speed[0] + 1 if speed[0] > 0 else speed[0] - 1
                elif event.key == pygame.K_DOWN:
                    speed[1] += 1
                    # speed[1] = speed[1] if speed[1] == 0 else (abs(speed[1]) - 1) * int(speed[1] / abs(speed[1]))
                elif event.key == pygame.K_UP:
                    speed[1] -= 1
                    # speed[1] = speed[1] + 1 if speed[1] > 0 else speed[1] - 1
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

        ballrect = ballrect.move(speed[0], speed[1])
        if ballrect.left < 0:
            ballrect = ballrect.move(width-ballWidth,0)
        if ballrect.right > width:
            ballrect = ballrect.move(ballWidth-width, 0)
        if ballrect.top < 0 :
            ballrect = ballrect.move(0, height-ballHeight)
        if ballrect.bottom > height:
            ballrect = ballrect.move(0, ballHeight - height)

        screen.fill(BLACK)
        screen.blit(ball, ballrect)
        pygame.display.update()
        fclock.tick(fps)

if __name__ == '__main__':
    # testCarAnalogyEngine()
    score_queue = []
    score_queue.append(1)
    score_queue.append(1)
    score_queue.append(0)
    score_queue.append(3)
    score_queue.pop()
    print(score_queue)
    print(np.average(score_queue))
