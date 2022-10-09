import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()


def sendNoContestsToday():
    webhookForNoContest = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'),
                                         content=f'No contests today! Enjoy your free time 🌚👋🏻')
    webhookForNoContest.execute()


def sendContestAlerts(hackathons):
    webhook = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'))
    for hackathon in hackathons:
        embed = DiscordEmbed(title=hackathon["name"], description=hackathon["platform"], color='03b2f8')
        embed.set_footer(text='Made with ❤️ && ☕️', icon_url="")
        embed.set_image(url=hackathon["thumbnail"])

        embed.set_timestamp()
        embed.add_embed_field(name='Starts @', value=hackathon["start_iso"])
        embed.add_embed_field(name='Ends @', value=hackathon["end_iso"])
        embed.add_embed_field(name='Registration Ends in ', value=hackathon["regEnd"],inline=False)
        embed.add_embed_field(name='Prize :', value=hackathon["prize"])
        embed.add_embed_field(
            name='Find @', value=hackathon["link"], inline=False)
        embed.add_embed_field(name='Mark the event @',value=f"[Add this to Google Calender]({hackathon['calender_event']})", inline=False)
        embed.set_author(name='Hackathon Alert', url=hackathon["link"])
        # embed.add_embed_field(name='Reminder @', value=f"{contest['ticktick_task']}", inline=False)
        webhook.add_embed(embed)
        # todo add a check if successful
        webhook.execute()
        webhook.remove_embed(0)
        # webhookForTickTick = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'), content=f'Add this contest
        # to TickTick for ⏰ @ <{contest["ticktick_task"]}>') webhookForTickTick.execute()
