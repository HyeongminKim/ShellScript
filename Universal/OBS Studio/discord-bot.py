import os
import discord
import subprocess

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 로그인 성공: {bot.user}")

@bot.slash_command(name="status", description="현재 재생 중인 음악 정보를 출력합니다.")
async def status(ctx: discord.ApplicationContext):
    await ctx.defer()  # 봇이 응답 중이라는 표시

    try:
        # playerctl metadata 실행
        result = subprocess.check_output(
            ["playerctl", "metadata", "--format",
                "제목: {{title}}\n",
                "URL: {{xesam:url}}\n",
                "{{duration(position)}} | {{duration(mpris:length)}}\n"
            ],
            text=True
        )
        if not result:
            result = "🎵 현재 재생 중인 트랙이 없습니다."
        else:
            await ctx.respond(f"🎵 현재 재생 정보:\n```\n{result}\n```")
    except subprocess.CalledProcessError:
        await ctx.respond("⚠️ playerctl 실행에 실패했습니다.")
    except FileNotFoundError:
        await ctx.respond("❌ 시스템에 playerctl이 설치되어 있지 않습니다.")

# 봇 실행
token = os.environ.get("DISCORD_BOT_PLAYERCTL")

if token:
    bot.run(token)
else:
    print("❌ 환경변수 'OBS_MEDIAINFO_DISCORD_BOT'이 설정되지 않았습니다.")

