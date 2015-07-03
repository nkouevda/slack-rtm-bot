from handlers.base import handlers, MessageHandler

class HelpHandler(MessageHandler):

  TRIGGERS = ['help']
  HELP = 'help for the given command; default all commands'

  _RESPONSES = None

  def handle_message(self, event, query):
    if self._RESPONSES is None:
      self._init_responses()

    if query.startswith('!'):
      query = query[1:]

    return self._RESPONSES.get(query, self._RESPONSES[None])

  def _init_responses(self):
    self._RESPONSES = {}
    parts = set()
    for handler in handlers:
      triggers = ', '.join('!%s' % trigger for trigger in handler.TRIGGERS)
      part = '%s - %s' % (triggers, handler.HELP)
      parts.add(part)
      for trigger in handler.TRIGGERS:
        self._RESPONSES[trigger] = '```%s```' % part

    self._RESPONSES[None] = '```%s```' % '\n'.join(sorted(parts))
