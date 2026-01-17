import discord
from discord.ext import commands
import aiohttp
import os
# ======================
# CONFIGURAÇÃO
# ======================

TOKEN = os.getenv("DISCORD_TOKEN")
ROBLOSECURITY = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzI1MTIwMTY5MTg4MzkxNTQyMjgoAw.6jAhnzSeBp-mjjPmanXWjcRRXEGb1mGEiZ3c_ZqkbnvDPigsSUEtdeF0a8AJ__jQKOSuPtV54Fo6DFF3A5FpGNxGFSA4-HWxjIStEeqDNATXkg_Otz2M7KNYAzEFi2IIOPLGscR0KpiJsotTSSefQVHaf1RIts8fP-LM-S-t8zznEzLXbKFh-d7wJo1rbVtYiEoFdyv7eRRO_UvA-PktiKE1R5RrocEg9yr0TCC6StT17AIGbh_imVYVUjdHeSdrWnrvNDHckUD-MY3IKB5GyeOeOgOFll5DIJ0XRH55I-jmm5xZJNlat6vsu3T6VB0HgS3Y_M3h7VF3uYrFVQde9oUU3AlJXXeUDDR4j01FjL8PhWNwPzV2LcW9yj4lLGXedGbeS4fZPrbmmNej5gobVla5H42BkfzlzkDmcxXoMJE8JhyLNAZvAii51XHR-twn94Oz--15b1OwplZQCkLwvyUDggM_VOsPqIgtJMSktmFjiEPW05a2VKVN-y9remRreAkx-O0jz9wiBhItwlQxNoZn1-SF08rY4hofNJr8XUn2aLGrQpOV0sSV764ScNwV6BDAbmu6g3b17R-hbSgWrezdb4h1Y8aTG9I4xDjIf7etZjp3Qd0bv8INl_lBu_kmrqyY8RrQxrZfSRkvrrrNF4b6w6kfS3RinDQ-vSXA68UyMiPBOb2hAlXqnayaXu1EKJXLkHJFqLq2lRQjSZOirfs5WKB20fvwHtxydqA0dG5PUH7ra_ZOdtQ_yFZJpK_bqW6i3Xq_tYkqwx0eciiMLD77sEFqnQcEYmybNhJVyTKshVmz"
USER_ID = 10349729102
BLOXLINK_API_KEY = "fd161e0f-c92a-4856-8483-485ca035c5b5"
GUILD_ID = 1461414512912502836

# ======================
# BOT SETUP
# ======================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


# ======================
# BOTÃO COMMAND
# ======================
@bot.command()
async def button(ctx):

    class MeuBotao(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Get Key", style=discord.ButtonStyle.success)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            async with aiohttp.ClientSession() as session:

                # ======================
                # Pegar RobloxID via Blox.link
                # ======================
                bloxlink_url = f"https://api.blox.link/v4/public/guilds/{GUILD_ID}/discord-to-roblox/{interaction.user.id}"
                headers = {"Authorization": BLOXLINK_API_KEY}

                async with session.get(bloxlink_url, headers=headers) as resp:
                    blox_data = await resp.json()

                robloxID = blox_data.get("robloxID")
                if not robloxID:
                    await interaction.response.send_message(
                        f"⚠️ Usuário não vinculado no Blox.link.",
                        ephemeral=True
                    )
                    return

                # ======================
                # Pegar transações do Roblox
                # ======================
                roblox_url = f"https://economy.roblox.com/v2/users/{USER_ID}/transactions?limit=50&transactionType=Sale"
                roblox_headers = {"Cookie": f".ROBLOSECURITY={ROBLOSECURITY}"}

                async with session.get(roblox_url, headers=roblox_headers) as r:
                    roblox_data = await r.json()

                # ======================
                # Filtrar transações do usuário pelo RobloxID
                # ======================
                resultado = [sale for sale in roblox_data.get("data", []) if sale["agent"]["id"] == int(robloxID)]

                if resultado:
                    content = (
                        f"✅ Sucess!\n\n"
                        #f"📦 Transação encontrada:\n{resultado[0]}"
                        f""
                        f"# KEY: EPSTEIN_ISLAND100"
                    )
                else:
                    content = (
                        f"❌You didn't buy the gamepass, kill yourself nigga"
                    )

                await interaction.response.send_message(content, ephemeral=True)

    # ======================
    # Enviar botão
    # ======================
    await ctx.send("Get Your Key here:", view=MeuBotao())


# ======================
# RUN BOT
# ======================
bot.run(TOKEN)
