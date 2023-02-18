import os
import json

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()


def isAlready(id):
    with open('/home/areeburrub/codealert-bot-discord/hackathon/already.json', 'r') as f:
    # with open('hackathon/already.json', 'r') as f:
        data = json.load(f)
    if id in data:
        return True
    else:
        #add id to data
        data.append(id)
        with open('/home/areeburrub/codealert-bot-discord/hackathon/already.json', 'w') as f:
        # with open('hackathon/already.json', 'w') as f:
            json.dump(data, f)
        return False


def sendNoContestsToday():
    webhookForNoContest = DiscordWebhook(url=os.environ.get('DISCORD_HACKATHON_WEBHOOK_URL'),
                                         content=f'No hackthons found! Enjoy your free time 🌚👋🏻')
    webhookForNoContest.execute()


def sendContestAlerts(hackathons):
    for hackathon in hackathons:
        if (isAlready(hackathon['id'])):
            # webhook = DiscordWebhook(url=os.environ.get('DISCORD_HACKATHON_REMINDER_WEBHOOK_URL'))
            # embed = DiscordEmbed(title="Reminder for "+hackathon["name"], description=hackathon["platform"], color='03b2f8')
            # embed.set_footer(text='Made with ❤️ && ☕️', icon_url="")
            # embed.set_image(url=hackathon["thumbnail"])
            # embed.set_timestamp()
            # embed.add_embed_field(name='Registration Ends in ', value=hackathon["regEnd"],inline=False)
            # embed.add_embed_field(name='Find @', value=hackathon["link"], inline=False)
            # webhook.add_embed(embed)
            # webhook.execute()
            # webhook.remove_embed(0)
            continue
        else:
            webhook = DiscordWebhook(url=os.environ.get('DISCORD_HACKATHON_WEBHOOK_URL'))
            print("Sending")
            embed = DiscordEmbed(title=hackathon["name"], description=hackathon["platform"], color='03b2f8')
            embed.set_footer(text='Made with ❤️ && ☕️', icon_url="")
            embed.set_image(url=hackathon["thumbnail"])
            embed.set_timestamp()
            embed.add_embed_field(name='Starts @', value=hackathon["start_iso"])
            embed.add_embed_field(name='Ends @', value=hackathon["end_iso"])
            embed.add_embed_field(name='Registration Ends in ', value=hackathon["regEnd"],inline=False)
            embed.add_embed_field(name='Prize :', value=hackathon["prize"])
            embed.add_embed_field(name='Find @', value=hackathon["link"], inline=False)
            embed.add_embed_field(name='Mark the event @',value=f"[Add this to Google Calender]({hackathon['calender_event']})", inline=False)
            embed.set_author(name='Hackathon Alert', url=hackathon["link"])
            # embed.add_embed_field(name='Reminder @', value=f"{contest['ticktick_task']}", inline=False)
            # todo add a check if successful
            webhook.add_embed(embed)
            webhook.execute()
            webhook.remove_embed(0)
            # webhookForTickTick = DiscordWebhook(url=os.environ.get('DISCORD_WEBHOOK_URL'), content=f'Add this contest
            # to TickTick for ⏰ @ <{contest["ticktick_task"]}>') webhookForTickTick.execute()
