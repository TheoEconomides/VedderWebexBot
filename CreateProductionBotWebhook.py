from webexteamsbot import TeamsBot

# This script installs the webhooks for the production bot, and is intended to be run from the developer's
# workstation, not from the production web site.  Thus the "VP_BOT_TOKEN" environment variable on the
# developer's local machine, which contains the token for the development bot, is not used here. Rather,
# the token is expressed literally in the variable, below.
bot_token = 'ZjQ3NThlZTItNjA4Zi00OTE0LWFmZDAtMTUyODcxNTBlMGQ0ZWI1NTE3NjUtM2Rh_PF84_9b4b0d2c-c77b-40fa-9a49-338196f70056'
bot_email = 'vp-ralph@webex.bot'
bot_url = "http://vpython.azurewebsites.net/events"
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
