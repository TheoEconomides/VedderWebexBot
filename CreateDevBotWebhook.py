from webexteamsbot import TeamsBot
import os

bot_token = os.environ.get('VP_BOT_TOKEN')
print("token:",bot_token)
bot_email = 'vp-tsiraki@webex.bot'
bot_url = "http://02c85ba0c44f.eu.ngrok.io/events"
bot_event_app_name = "eventBot"
bot_attach_app_name = "attachBot"
bot_secret = "BotSecret33"

MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"

# Create a Bot Object for messages
bot = TeamsBot(
    bot_event_app_name,
    teams_bot_token=bot_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    # teams_bot_secret=bot_secret,
    webhook_resource=MESSAGE_WEBHOOK_RESOURCE
)
# Create a Bot Object for attachments
botAttach = TeamsBot(
    bot_attach_app_name,
    teams_bot_token=bot_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    webhook_resource=CARDS_WEBHOOK_RESOURCE
)


# Add new commands to the box.
# bot.add_command("/dosomething", "help for do something", do_something)

