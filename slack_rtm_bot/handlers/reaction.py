from .base import MessageHandler
from .. import settings

class ReactionHandler(MessageHandler):

  TRIGGER_ANCHOR = ''
  TRIGGER_PREFIX = ''
  TRIGGERS = sorted(settings.EMOJI_REACTIONS.keys() +
                    settings.IMAGE_REACTIONS.keys())
  HELP = 'add reactions'

  def handle_message(self, event, triggers, query):
    for trigger in triggers:
      trigger = trigger.lower()
      self._try_handle_emoji(event, trigger, query)
      self._try_handle_image(event, trigger, query)

  def _get_reaction(self, reactions, trigger):
    reactions = reactions.get(trigger)
    if isinstance(reactions, basestring):
      reactions = [reactions]
    return reactions

  def _try_handle_emoji(self, event, trigger, query):
    reactions = self._get_reaction(settings.EMOJI_REACTIONS, trigger)
    if not reactions:
      return

    for reaction in reactions:
      self.client.api_call(
        'reactions.add',
        name=reaction,
        channel=event['channel'],
        timestamp=event['ts'])

  def _try_handle_image(self, event, trigger, query):
    reactions = self._get_reaction(settings.IMAGE_REACTIONS, trigger)
    if not reactions:
      return

    for reaction in reactions:
      self.client.api_call(
        'chat.postMessage',
        channel=event['channel'],
        text='<%s>' % reaction
      )

