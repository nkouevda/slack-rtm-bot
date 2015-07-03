import fnmatch
import functools
import importlib
import logging
import os
import re

import settings

_handler_classes = set()
handlers = set()

def init_handlers(client):
  handlers_dir = os.path.dirname(__file__)
  for filename in fnmatch.filter(os.listdir(handlers_dir), '[!_]*.py'):
    module = filename[:-3]
    try:
      importlib.import_module('handlers.%s' % module)
      logging.info('loaded handler module: %s' % module)
    except Exception:
      logging.exception('failed to load handler module: %s' % module)

  handlers.update(cls(settings, client) for cls in _handler_classes)

def message_handler(regex, flags=re.IGNORECASE):
  """Decorator factory for message handlers.

  The wrapped handler is called with each normal (i.e. no subtype) message event
  for which the message text matches the given regex. In addition to the event,
  the query (the message text with the first regex match removed, and
  surrounding whitespace stripped) is passed to the handler.

  An empty string regex can be used to receive all messages.
  """
  def decorator(func):
    @functools.wraps(func)
    def wrapper(self, event):
      if event['type'] == 'message' and 'subtype' not in event:
        text = event['text']
        match = re.search(regex, text, flags=flags)
        if match:
          query = (text[:match.start()] + text[match.end():]).strip()
          return func(self, event, query)

    return wrapper

  return decorator

class HandlerRegistry(type):

  def __init__(cls, name, bases, namespace):
    super(HandlerRegistry, cls).__init__(name, bases, namespace)
    _handler_classes.add(cls)
    _handler_classes.difference_update(bases)

class Handler(object):

  __metaclass__ = HandlerRegistry

  def __init__(self, settings, client):
    self.settings = settings
    self.client = client

  @property
  def help(self):
    raise NotImplementedError

  def handle(self, event):
    raise NotImplementedError
