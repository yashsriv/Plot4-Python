#!/usr/bin/env python3
import board

def getBestMove(b, maxdep, prev):
  score,mov = aspiration(b, maxdep, prev);
  b.is_game_over(profile=True);
  b.is_move(profile=True);
  b.make_move(profile=True);
  b.undo_move(profile=True);
  b.is_win(profile=True);
  b.find_row(profile=True);
  b.evaluate(profile=True);
  return score,mov;

def aspiration(b, maxdep, prev):
  if prev == 0:
    alpha = -1000;
    beta = 1000;
  else:
    alpha = prev - 100;
    beta = prev + 100;

  while True:
    score,mov = ABnegamax(b, maxdep, 0, alpha, beta);
    if score <= alpha:
      alpha = -1000;
    elif score >= beta:
      beta = 1000;
    else :
      return score,mov;


def ABnegamax(b, maxdep, curdep, alpha, beta):
  if b.is_game_over() or curdep == maxdep:
    score = b.evaluate() + curdep;
    # score = curdep;
    mov = -1;
    return score,mov;
  bmov = -1;
  bscore = -1000;
  for i in range(7):
    if b.is_move(i):
      b.make_move(i);
      if alpha > bscore:
        m = alpha;
      else :
        m = bscore;
      rsco,rmov = ABnegamax(b, maxdep, curdep + 1, -beta, -m);
      csco = -rsco;
      cmov = rmov;
      if csco > bscore:
        bscore = csco;
        bmov = i;
        if bscore >= beta:
          b.undo_move();
          return bscore,bmov;
      b.undo_move();
  return bscore, bmov;



