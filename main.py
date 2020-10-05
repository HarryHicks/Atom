import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio

from random import randint


def get_prefix(client, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
    except:
        return 'atom '

description = '''Bot coded in discord.py by Hicksy#2047'''
bot = commands.Bot(command_prefix=get_prefix, description=description)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="atom help"))


@bot.command(aliases=['stats'])
async def info(ctx):
    embed = discord.Embed(title="Bot Statistics", colour=0x36393E)
    embed.set_author(name="Atom ",
                    icon_url="https://cdn.discordapp.com/avatars/732172271753494599/aec2276c70c45e6c3a2bdf1c337dba47.png?size=128")
    embed.set_footer(text="Creator: Hicksy#2047 | Atom  v1.0",
                    icon_url="https://cdn.discordapp.com/avatars/626065155767271445/a_26605c1c02b30201b782866c8f68590d.gif?size=128")
    embed.add_field(name="**Some Info**", value="**Developer:** <@626065155767271445>\n**Coded in:** discord.py\n**Support:** https://discord.gg/tsMjzbE")
    embed.add_field(name="**Bot Stats**", value=f"**Bot Users:** {len(bot.users)}\n**Servers using me:** {len(bot.guilds)}")
        
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def servers(ctx):
    await ctx.send('Servers connected to:')
    for guild in bot.guilds:
        await ctx.send(guild.name)

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed=discord.Embed(title="Kick", description="Member Successfully Kicked.")
    embed.set_footer(text="Atom ")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed=discord.Embed(title="Ban", description="Member Successfully Banned.")
    embed.set_footer(text="Atom ")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send("Member Successfully Muted!")

@bot.command()
@has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.remove_roles(role)
    await ctx.send("Member Successfully Unmuted!")

@bot.command()
@has_permissions(administrator=True)
async def suggest(ctx, *,suggestion):
    channel = bot.get_channel(750611141188648961)
    embed=discord.Embed(title="New Suggestion!", description=(suggestion))
    await channel.send(embed=embed)

@bot.command(pass_context = True)
@has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason:
    await ctx.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break

  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)
    await ctx.send("User Successfully warned!")

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
      await ctx.channel.purge(limit=limit)
      await ctx.send('Cleared by {}'.format(ctx.author.mention))


@bot.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  if not user:
    await ctx.send("Please provide a user.")
    return
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported")


bot.run("TOKEN")
