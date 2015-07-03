from handlers.base import Handler, message_handler

class PingHandler(Handler):

  @property
  def help(self):
    return '!ping - pong'

  @message_handler(r'^!ping\b')
  def handle(self, event, query):
    return 'pong'
