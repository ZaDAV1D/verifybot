import discord
from discord.ext import commands

import os

TOKEN = os.getenv("TOKEN")  # חשוב לRender

VERIFIED_ROLE_ID = 1514345499711504628
VERIFY_CHANNEL_ID = 1514345739273113721

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

panel_sent = False


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = interaction.guild.get_role(VERIFIED_ROLE_ID)

        if role in interaction.user.roles:
            return await interaction.response.send_message(
                "✔️ אתה כבר מאומת",
                ephemeral=True
            )

        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "🎉 אומתת בהצלחה!",
                ephemeral=True
            )
        except:
            await interaction.response.send_message(
                "❌ אין לי הרשאה לתת רול",
                ephemeral=True
            )


@bot.event
async def on_ready():
    global panel_sent

    print(f"Logged in as {bot.user}")

    if panel_sent:
        return

    channel = bot.get_channel(VERIFY_CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="🔐 Verification",
            description="לחץ על הכפתור כדי לקבל גישה לשרת",
            color=discord.Color.green()
        )

        await channel.send(embed=embed, view=VerifyView())

        panel_sent = True
    else:
        print("❌ Verify channel not found")


bot.run(TOKEN)
