from handlers.base import MessageHandler

class CornHandler(MessageHandler):

  TRIGGER_ANCHOR = None
  TRIGGER_PREFIX = None
  TRIGGERS = ['cron']

  def handle_message(self, event, query):
    self.client.api_call(
        'reactions.add',
        name='corn',
        channel=event['channel'],
        timestamp=event['ts'])
