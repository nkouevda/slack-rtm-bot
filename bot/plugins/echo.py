from plugins.base import message_handler, Plugin

class Echo(Plugin):

  @property
  def help(self):
    return '!echo <query> - <query>'

  @message_handler(r'^!echo\b')
  def handle(self, event, query):
    return query
