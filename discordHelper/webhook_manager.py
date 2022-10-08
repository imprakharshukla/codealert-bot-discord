import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()


def sendNoContestsToday():
    webhookForNoContest = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'),
                                         content=f'No contests today! Enjoy your free time 🌚👋🏻')
    webhookForNoContest.execute()


def sendContestAlerts(contestList):
    webhook = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'))
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
        webhook.add_embed(embed)
        # todo add a check if successful
        webhook.execute()
        webhook.remove_embed(0)
        # webhookForTickTick = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'), content=f'Add this contest
        # to TickTick for ⏰ @ <{contest["ticktick_task"]}>') webhookForTickTick.execute()
