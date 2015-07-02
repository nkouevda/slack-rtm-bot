from collections import Counter
import logging
import random

from plugins.base import message_handler, Plugin

class Dice(Plugin):

  @property
  def help(self):
    return '!dice [<number>] - roll <number> dice; default 1'

  @message_handler(r'^!dice\b')
  def handle(self, event, query):
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
