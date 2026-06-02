import discord
from discord.ext import commands
from datetime import datetime, timezone


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


WELCOME_CHANNEL_ID = 12345678909874563210  


def get_account_age(created_at):
    now = datetime.now(timezone.utc)  
    delta = now - created_at

    days = delta.days
    years = days // 365
    months = (days % 365) // 30

    return f"{years}y {months}m {days % 30}d ago"

@bot.event
async def on_ready():
    print(f"🔥 Royan is ONLINE as {bot.user}")


@bot.event
async def on_member_join(member):
    print(f"JOIN DETECTED: {member}")  

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if not channel:
        print("❌ Channel not found!")
        return

    embed = discord.Embed(
        title="✨ Welcome to the Server!",
        description=f"Hey {member.mention}, welcome to **{member.guild.name}** 🎉",
        color=discord.Color.green(),
        timestamp=datetime.now(timezone.utc)  
    )

    avatar = member.avatar.url if member.avatar else member.default_avatar.url

    embed.set_author(
        name=f"{member.name}#{member.discriminator}",
        icon_url=avatar
    )

    embed.set_thumbnail(url=avatar)

    embed.add_field(
        name="👤 Member Info",
        value=(
            f"**Join Position:** {member.guild.member_count}\n"
            f"**Created On:** {member.created_at.strftime('%d %b %Y')}\n"
            f"**Account Age:** {get_account_age(member.created_at)}"
        ),
        inline=False
    )

    embed.add_field(
        name="🆔 User ID",
        value=f"`{member.id}`",
        inline=True
    )

    embed.set_footer(
        text=member.guild.name,
        icon_url=member.guild.icon.url if member.guild.icon else None
    )

    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    print(f"LEAVE DETECTED: {member}") 

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if not channel:
        print("❌ Channel not found!")
        return

    embed = discord.Embed(
        title="💔 Member Left",
        description=f"**{member.name}** has left the server...",
        color=discord.Color.red(),
        timestamp=datetime.now(timezone.utc)  
    )

    avatar = member.avatar.url if member.avatar else member.default_avatar.url

    embed.set_author(
        name=f"{member.name}#{member.discriminator}",
        icon_url=avatar
    )

    embed.set_thumbnail(url=avatar)

    roles = [role.mention for role in member.roles if role.name != "@everyone"]
    roles_text = ", ".join(roles) if roles else "No roles"

    embed.add_field(
        name="🎭 Roles",
        value=roles_text,
        inline=False
    )

    embed.add_field(
        name="📉 Members Left",
        value=f"{member.guild.member_count} remaining",
        inline=True
    )

    embed.add_field(
        name="🆔 User ID",
        value=f"`{member.id}`",
        inline=True
    )

    embed.set_footer(
        text=member.guild.name,
        icon_url=member.guild.icon.url if member.guild.icon else None
    )

    await channel.send(embed=embed)


bot.run("YOUR_BOT_TOKEN")
