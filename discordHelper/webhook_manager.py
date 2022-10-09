import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()


def sendNoContestsToday():
    webhookForNoContest = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'),
                                         content=f'No contests today! Enjoy your free time 🌚👋🏻')
    webhookForNoContest.execute()


def sendNoImpContestsToday():
    webhookForNoContest = DiscordWebhook(url=os.environ.get('DISCORD_IMPORTANT_CONTEST_WEBHOOK_URL'),
                                         content=f'No Important contests today! Enjoy your free time 🌊')
    webhookForNoContest.execute()


def sendContestAlerts(contestList):
    impCounter = 0
    webhook = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'))
    impWebhook = DiscordWebhook(url=os.environ.get('DISCORD_IMPORTANT_CONTEST_WEBHOOK_URL'))
    for contest in contestList:
        embed = DiscordEmbed(title=contest["name"], description=contest["platform"], color='03b2f8')
        embed.set_footer(text='Made with ❤️ && ☕️', icon_url="")
        embed.set_image(url=contest["thumbnail"])

        embed.set_timestamp()
        embed.add_embed_field(name='Starts @', value=contest["start_iso"])
        embed.add_embed_field(name='Ends @', value=contest["end_iso"])
        embed.add_embed_field(name='Find @', value=contest["link"], inline=False)
        embed.add_embed_field(name='Mark the event @',
                              value=f"[Add this to Google Calender]({contest['calender_event']})", inline=False)
        # embed.add_embed_field(name='Reminder @', value=f"{contest['ticktick_task']}", inline=False)
        if contest["isImp"] == 1:
            impCounter += 1
            impWebhook.add_embed(embed)
            impWebhook.execute()
            impWebhook.remove_embed(0)
        else:
            webhook.add_embed(embed)
            webhook.execute()
            webhook.remove_embed(0)
        # todo add a check if successful

    if impCounter == 0:
        sendNoImpContestsToday()

# webhookForTickTick = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'), content=f'Add this contest
# to TickTick for ⏰ @ <{contest["ticktick_task"]}>') webhookForTickTick.execute()
