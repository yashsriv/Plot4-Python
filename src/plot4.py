#!/usr/bin/env python3
import pygame, sys
import random
from pygame.locals import *
import board



def main():
  dirty = []
  # Init:
  pygame.init()
  FPS = 30
  fpsClock = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((560,480))
  pygame.display.set_caption('Connect 4!')
  b = board.Board()
  b.draw_init_board(DISPLAYSURF)
  pygame.display.update()
  while b.alive :
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        col = mousex // 80;
        b.update(col)
      elif event.type == KEYUP:
        if event.key in (K_q,) :
          pygame.quit()
          sys.exit()
      elif event.type == MOUSEMOTION:
        mousex, mousey = event.pos
        col = mousex // 80;
        b.mouseDisplay(col,DISPLAYSURF,dirty)
    b.draw(DISPLAYSURF,dirty)
    pygame.display.update(dirty)
    for i in range(len(dirty)) : dirty.pop()
    fpsClock.tick(FPS)
  b.draw_full_board(DISPLAYSURF)
  # if(b.winner == board.WHITE) :
    # img = pygame.image.load("../res/white_win.png")
  # else :
    # img = pygame.image.load("../res/black_win.png")
  # another = DISPLAYSURF.convert_alpha()
  # another.blit(img,(0,0))
  # DISPLAYSURF.blit(another,(0,0))
  pygame.display.update()

  while True :
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == KEYUP:
        if event.key in (K_q,) :
          pygame.quit()
          sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)

if __name__ == '__main__':
  main()
