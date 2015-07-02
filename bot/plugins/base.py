import fnmatch
import functools
import importlib
import logging
import os
import re

import settings

_plugin_classes = set()
plugins = set()

def init_plugins(client):
  plugins_dir = os.path.dirname(__file__)
  for filename in fnmatch.filter(os.listdir(plugins_dir), '[!_]*.py'):
    module = filename[:-3]
    try:
      importlib.import_module('plugins.%s' % module)
      logging.info('loaded plugin module: %s' % module)
    except Exception:
      logging.exception('failed to load plugin module: %s' % module)

  plugins.update(cls(settings, client) for cls in _plugin_classes)

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

class PluginRegistry(type):

  def __init__(cls, name, bases, namespace):
    super(PluginRegistry, cls).__init__(name, bases, namespace)
    _plugin_classes.add(cls)
    _plugin_classes.difference_update(bases)

class Plugin(object):

  __metaclass__ = PluginRegistry

  def __init__(self, settings, client):
    self.settings = settings
    self.client = client

  @property
  def help(self):
    raise NotImplementedError

  def handle(self, event):
    raise NotImplementedError
