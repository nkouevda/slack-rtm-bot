from handlers.base import Handler, message_handler

class EchoHandler(Handler):

  @property
  def help(self):
    return '!echo <query> - <query>'

  @message_handler(r'^!echo\b')
  def handle(self, event, query):
    return query
