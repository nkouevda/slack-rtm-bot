from plugins.base import message_handler, Plugin

class Rot13(Plugin):

  @property
  def help(self):
    return '!rot13 <query> - ROT13 applied to <query>'

  @message_handler(r'^!rot13\b')
  def handle(self, event, query):
    return query.encode('rot13')
