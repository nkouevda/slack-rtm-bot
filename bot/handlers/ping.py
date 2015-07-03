from handlers.base import MessageHandler

class PingHandler(MessageHandler):

  TRIGGERS = ['ping']
  HELP = 'pong'

  def handle_message(self, event, query):
    return 'pong'
