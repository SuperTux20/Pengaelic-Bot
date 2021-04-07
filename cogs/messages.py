import discord
from discord.ext import commands
from pengaelicutils import options
from json import dumps


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
    name = "messages"
    name_typable = name
    description = "Make me say all sorts of things."
    description_long = description + " And possibly make me die inside."

    @commands.command(name="say", help="I'll repeat whatever you tell me.", pass_context=True, aliases=["repeat", "parrot"], usage="<message>")
    async def say_back(self, ctx, *, arg):
        await ctx.send(
            arg
        )
        await ctx.message.delete()

    @commands.command(name="delet", help="delet this.")
    async def delet_this(self, ctx):
        await ctx.message.delete()
        await ctx.send(
            "https://supertux20.github.io/Pengaelic-Bot/images/gifs/no_one_is_safe.gif"
        )

    @commands.command(name="credits", help="See who helped me come to exist!")
    async def credits(self, ctx):
        bot_credits = {
            "Main Developer and Creator": "chickenmeister",
            "Current Host": "Hyperfresh",
            "Biggest Helper": "legenden",
            "Other Helpers": "leasip"
        }
        if options(ctx.guild.id)["JSONmenus"]:
            bot_credits = {
                cred.lower(): bot_credits[cred]
                for cred in bot_credits
            }
            await ctx.send(f"""
```json
"credits": {str(dumps(bot_credits, indent=4))}
```
""")
        else:
            embed = discord.Embed(
                color=32639,
                title="Credits",
                description="All the people on Discord who helped me become what I am today."
            )
            for cred in bot_credits:
                embed.add_field(
                    name=cred,
                    value=bot_credits[cred]
                )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(
        Messages(
            client
        )
    )
