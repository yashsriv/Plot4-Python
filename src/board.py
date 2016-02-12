#!/usr/bin/env python3
import pygame
import random
import intelligence
from pygame.locals import *
from move import *
EMPTY = 'EMPTY_TILE';
RED = 'RED_COIN';
YELLOW = 'YELLOW_COIN';

#Color = (R  , G  , B   );
blue   = (33 , 150, 243 );
red    = (244, 67 , 54  );
yellow = (255, 235, 59  );


class Board:
  # Constructor to initialize stuff
  # @param void
  # @return void
  def __init__(self):
    self.board = [[EMPTY for i in range(7)] for j in range(6)];
    self.old_board = [ l[:] for l in self.board];
    self.prev = Move(-1, -1);
    self.current = RED;
    self.movecount = -1;
    self.moves = [];
    self.alive = True;
    self.winner = 'NONE';
    self.previous_score = 0;

  # display board for debugging
  def display(self):
    print(self.board);


  # Check if game is over
  # if number of moves = 0 , game has not started
  # if last move played by other player was a win, game is over
  #  if total no. of moves = 42, game is over
  def is_game_over(self):
    if len(self.moves) == 0:
      return False;
    if self.is_win(self.prev,self.other(self.current)):
      self.winner = self.other(self.current);
      return True;
    else :
      self.winner = 'NONE';
      return len(self.moves) == 42;


  # Other player
  def other(self,p):
    if(p == YELLOW):
      return RED;
    else :
      return YELLOW;

  # checks if it is a valid move
  def is_move(self,pos):
    return (pos >= 0 and pos <= 6 and self.board[0][pos] == EMPTY );

  # makes a move
  def make_move(self,pos):
    # self.display();
    for i in range(6):
      if(self.board[i][pos] != EMPTY):
        break;
    if self.board[i][pos] == EMPTY:
      i = i + 1;
    self.board[i - 1][pos] = self.current;
    self.movecount += 1;
    m = Move(i - 1,pos);
    self.moves.append(m);
    self.prev = m;
    self.current = self.other(self.current);

  # undo move
  def undo_move(self):
    m = self.moves.pop();
    self.board[m.row][m.col] = EMPTY;
    self.movecount -= 1;
    self.prev = self.moves.pop();
    self.moves.append(self.prev);
    self.current = self.other(self.current);

  # Finds maximum filled row for faster board evalualtion
  def find_row(self):
    r = 5;
    i = r;
    while i>=0 :
      counter = 0;
      for j in range(7):
        if(self.board[i][j] != EMPTY):
          counter += 1;
      if ( counter == 0):
        return i;
      i -= 1;
    return (0);

  # check if it is a win
  def is_win(self,m,k):
    row = m.row;
    col = m.col;
    check = k;
    vertical = 1;
    vertical = 1;
    horizontal = 1;
    diagonal1 = 1;
    diagonal2 = 1;
    i = row + 1;
    while i <= 5:
      if(self.board[i][col] != k):
        break;
      i += 1;
      vertical += 1;

    i = row - 1;
    while i >= 0:
      if(self.board[i][col] != k):
        break;
      i -= 1;
      vertical += 1;
    if ( vertical >= 4 ):
      return True;


    i = col + 1;
    while i <= 6:
      if(self.board[row][i] != k):
        break;
      i += 1;
      horizontal += 1;
    i = col - 1;
    while i >= 0:
      if(self.board[row][i] != k):
        break;
      i -= 1;
      horizontal += 1;
    if ( horizontal >= 4 ) :
      return True;

    j = col - 1;
    i = row - 1;
    while i>=0 and j >=0:
      if(self.board[i][j] != k):
        break;
      i -= 1;
      j -= 1;
      diagonal1 += 1;

    j = col + 1;
    i = row + 1;
    while i <= 5 and j <= 6:
      if(self.board[i][j] != k):
        break;
      i += 1;
      j += 1;
      diagonal1 += 1;

    if ( diagonal1 >= 4 ) :
      return True;

    j = col + 1;
    i = row - 1;
    while i >= 0 and j <= 6:
      if(self.board[i][j] != k):
        break;
      i -= 1;
      j += 1;
      diagonal2 += 1;

    j = col - 1;
    i = row + 1;
    while i <= 5 and j >= 0:
      if(self.board[i][j] != k):
        break;
      i += 1;
      j -= 1;
      diagonal2 += 1;

    if ( diagonal2 >= 4 ) :
      return True;
    return False;

  # evaluate function for the board
  def evaluate(self):
    if(self.is_win(self.prev,self.other(self.current))):
      score = -100;
    else :
      ctr1 = 0;
      ctr2 = 0;
      row = self.find_row();
      for j in range(7):
        i = 5;
        while i>= row:
          point1 = 0;
          point2 = 0;
          flag = False;
          if(self.board[i][j] == EMPTY):
            for k1 in [-1,0,1]:
              for k2 in [-1,0,1]:
                if ( ( ( i - k1 ) >= 0 and ( i - k1 ) < 6 ) and ( ( j - k2 ) >= 0 and ( j - k2 ) < 7 ) ):
                  if( self.board[i - k1][j - k2] != EMPTY):
                    flag = True;
            if (flag):
              self.board[i][j] = self.current;
              if ( self.is_win(Move(i,j),self.current)):
                ctr1 += 1;
                point1  = 1;
              self.board[i][j] = self.other(self.current);
              if(self.is_win(Move(i,j),self.other(self.current))):
                ctr2 += 1;
                point2 += 1;
              self.board[i][j] = EMPTY;
          if point1 == point2 and point1 == 1:
            break;
          i -= 1;
      score = ctr1 - ctr2;
    return score;

  def draw_init_board(self,surface):
    surface.fill(blue);
    for i in range(6):
      pygame.draw.line(surface,(0,0,0),(0,80*i),(560,80*i));
    for j in range(7):
      pygame.draw.line(surface,(0,0,0),(80*j, 0),(80*j, 480));
    for i in range(6):
      for j in range(7):
        r = Rect(10 + (80 * j), 10 + (80 * i), 80 - 20, 80 - 20);
        pygame.draw.ellipse(surface,(255,255,255),r,0);


  def draw_full_board(self,surface):
    surface.fill(blue);
    for i in range(6):
      pygame.draw.line(surface,(0,0,0),(0,80*i),(560,80*i));
    for j in range(7):
      pygame.draw.line(surface,(0,0,0),(80*j, 0),(80*j, 480));
    for i in range(6):
      for j in range(7):
        r = Rect(10 + (80 * j), 10 + (80 * i), 80 - 20, 80 - 20);
        col = (255, 255, 255);
        if self.board[i][j] == RED:
          col = red;
        elif self.board[i][j] == YELLOW:
          col = yellow;
        pygame.draw.ellipse(surface,col,r,0);

  def draw(self,surface,dirt):
    for i in range(6):
      for j in range(7):
        if(self.old_board[i][j] != self.board[i][j]):
          r = Rect(10 + (80 * j), 10 + (80 * i), 80 - 20, 80 - 20);
          col = (255, 255, 255);
          if(self.board[i][j] == RED):
            col = red;
          elif self.board[i][j] == YELLOW:
            col = yellow;
          pygame.draw.ellipse(surface,col,r,0);
          dirt.append(r);
    self.old_board = [ l[:] for l in self.board];


  def update(self,cord):
    if self.current == RED and self.is_move(cord) and self.alive:
      self.make_move(cord);
      if self.is_game_over():
        print(self.winner);
      else :
        self.next_move();
        if self.is_game_over():
          print(self.winner);

  def next_move(self):
    self.previous_score, m = intelligence.getBestMove(self,4,self.previous_score);
    self.make_move(m);
    # available_moves = [];
    # for j in range(7):
      # if self.is_move(j):
        # available_moves.append(j);
    # a = random.choice(available_moves);
    # self.make_move(a);










