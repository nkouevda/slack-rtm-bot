from handlers.base import MessageHandler

class OwnersHandler(MessageHandler):

  TRIGGER_ANCHOR = ''
  TRIGGER_PREFIX = '@'
  TRIGGERS = ['owner', 'owners']
  HELP = 'notify channel owner(s)'

  _OWNERS = None

  def handle_message(self, event, query):
    if self._OWNERS is None:
      self._init_owners()

    return self._OWNERS.get(event['channel'])

  def _init_owners(self):
    self._OWNERS = {
        channel: ' '.join('@%s' % owner for owner in sorted(owners))
        for channel, owners in self.settings.CHANNEL_OWNERS.items()}
