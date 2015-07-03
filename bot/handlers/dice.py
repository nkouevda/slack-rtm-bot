from collections import Counter
import logging
import random

from handlers.base import MessageHandler

class DiceHandler(MessageHandler):

  TRIGGERS = ['dice', 'roll']
  HELP = 'roll the given number of dice; default 1'

  def handle_message(self, event, query):
    try:
      times = int(query or 1)
    except Exception:
      logging.warning('failed to parse int: %s' % query, exc_info=True)
      times = 1

    dice_gen = (random.randrange(1, 7) for _ in xrange(times))
    if times > 10:
      counter = Counter(dice_gen)
      return ', '.join('%s: %s' % (k, counter[k]) for k in xrange(1, 7))
    else:
      return ', '.join(map(str, dice_gen))
