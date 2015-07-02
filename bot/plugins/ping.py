from plugins.base import message_handler, Plugin

class Ping(Plugin):

  @property
  def help(self):
    return '!ping - pong'

  @message_handler(r'^!ping\b')
  def handle(self, event, query):
    return 'pong'
