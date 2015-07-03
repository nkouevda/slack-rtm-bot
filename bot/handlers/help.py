from handlers.base import Handler, handlers, message_handler

class HelpHandler(Handler):

  @property
  def help(self):
    return '!help [<command>] - help for <command>; default all commands'

  @message_handler(r'^!help\b')
  def handle(self, event, query):
    parts = [handler.help for handler in handlers]
    if query:
      for part in parts:
        trigger = part.split(None, 1)[0]
        if query in (trigger, trigger[1:]):
          return '```%s```' % part
    return '```%s```' % '\n'.join(sorted(parts))
