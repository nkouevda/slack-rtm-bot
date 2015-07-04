import fnmatch
import importlib
import logging
import os
import re

import settings

_handler_classes = set()
handlers = set()

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

  def handle(self, event):
    raise NotImplementedError

class MessageHandler(Handler):

  TRIGGER_ANCHOR = '^'
  TRIGGER_PREFIX = '!'
  TRIGGERS = []
  HELP = None

  def __init__(self, *args, **kwargs):
    super(MessageHandler, self).__init__(*args, **kwargs)
    pattern = r'%s(?:%s)' % (self.TRIGGER_PREFIX, '|'.join(self.TRIGGERS))
    if self.TRIGGER_ANCHOR == '^':
      pattern = r'^%s(?!\S)' % pattern
    elif self.TRIGGER_ANCHOR == '$':
      pattern = r'(?<!\S)%s$' % pattern
    self.TEXT_RE = re.compile(pattern, flags=re.IGNORECASE)

  def handle(self, event):
    if event['type'] == 'message' and 'subtype' not in event:
      match = self.TEXT_RE.search(event['text'])
      if match:
        query = self.TEXT_RE.sub('', event['text'], count=1)
        return self.handle_message(event, query)

  def handle_message(self, event, query):
    raise NotImplementedError

def init_handlers(client):
  handlers_dir = os.path.dirname(__file__)
  for filename in fnmatch.filter(os.listdir(handlers_dir), '[!_]*.py'):
    module = filename[:-3]
    try:
      importlib.import_module('handlers.%s' % module)
      logging.info('loaded handler module: %s' % module)
    except Exception:
      logging.exception('failed to load handler module: %s' % module)

  for handler_class in _handler_classes:
    try:
      handler = handler_class(settings, client)
      handlers.add(handler)
      logging.info('initialized handler: %s' % handler)
    except Exception:
      logging.exception('failed to initialize handler: %s' % handler_class)
      continue

    if isinstance(handler, MessageHandler):
      if not handler.TRIGGERS:
        logging.warning('message handler with no triggers: %s' % handler)
      if not handler.HELP:
        logging.warning('message handler with no help: %s' % handler)
