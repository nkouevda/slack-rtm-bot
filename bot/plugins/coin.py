from collections import Counter
import logging
import random

from plugins.base import message_handler, Plugin

class Coin(Plugin):

  @property
  def help(self):
    return '!coin [<number>] - flip <number> coins; default 1'

  @message_handler(r'^!coin\b')
  def handle(self, event, query):
    try:
      times = int(query or 1)
    except Exception:
      logging.warning('failed to parse int: %s' % query, exc_info=True)
      times = 1

    flips_gen = (random.choice(('heads', 'tails')) for _ in xrange(times))
    if times > 10:
      counter = Counter(flips_gen)
      return '%s heads, %s tails' % (counter['heads'], counter['tails'])
    else:
      return ', '.join(flips_gen)
