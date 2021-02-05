import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="$")
rules = ["No Spamming", "No Off-Topic Discussion", "No Abusing Commands"]


@bot.command()
async def report(ctx, member: discord.Member, *, arg):
    guild = ctx.guild
    trial_number = 0
    channel_exists = True
    author = ctx.author
    rule = rules[int(arg) - 1]
    while channel_exists == True:
        channel_name = 'trial-' + str(trial_number)
        channel = get(guild.text_channels, name=channel_name)
        if channel is None:
            channel_exists = False
        else:
            trial_number = trial_number + 1

    judge_role = get(guild.roles, name="Judge")
    officer_role = get(guild.roles, name="Officer")
    jury_role = get(guild.roles, name="Jury")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        judge_role: discord.PermissionOverwrite(read_messages=True),
        jury_role: discord.PermissionOverwrite(read_messages=True),
        officer_role: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(channel_name,overwrites=overwrites)
    await ctx.send(
        f'{member.mention} has been charged with breaking Rule {arg} ({rule})  by {author.mention}'
    )


bot.run(DISCORD_TOKEN)
