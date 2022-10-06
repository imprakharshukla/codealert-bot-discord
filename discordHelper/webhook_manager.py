import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()

webhook = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'))


def sendContestAlerts(contestList):
    print(len(contestList))
    for contest in contestList:
        embed = DiscordEmbed(title=contest["name"], description=contest["platform"], color='03b2f8')
        embed.set_footer(text='Made with ❤️ && ☕️', icon_url="")
        embed.set_image(url=contest["thumbnail"])

        embed.set_timestamp()
        embed.add_embed_field(name='Starts @', value=contest["start_iso"])
        embed.add_embed_field(name='Ends @', value=contest["end_iso"])
        embed.add_embed_field(name='Find @', value=contest["link"], inline=False)
        embed.add_embed_field(name='Mark the event @', value=contest["calender_event"], inline=False)
        webhook.add_embed(embed)
        # todo add a check if successful
        webhook.execute()
