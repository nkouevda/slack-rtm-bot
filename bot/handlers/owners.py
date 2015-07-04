from handlers.base import MessageHandler

class OwnersHandler(MessageHandler):

  TRIGGER_ANCHOR = None
  TRIGGER_PREFIX = '@'
  TRIGGERS = ['owners']
  HELP = 'notify channel owners'

  _OWNERS = None

  def handle_message(self, event, query):
    if self._OWNERS is None:
      self._init_owners()

    return self._OWNERS.get(event['channel'])

  def _init_owners(self):
    self._OWNERS = {}
    for channel, owners in self.settings.CHANNEL_OWNERS.items():
      self._OWNERS[channel] = ' '.join('@%s' % owner for owner in owners)
