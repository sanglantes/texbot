import pydle
import asyncio
import re
import tex
import requests
import sys

tex_pattern = re.compile(
    r'\\\[.*?\\\]|\\\(.*?\\\)', re.VERBOSE|re.DOTALL
)

addr = sys.argv[1]
channel = sys.argv[2]
use_ssl = sys.argv[3]

class Bot(pydle.Client):
    async def on_connect(self):
        await self.join(channel)
        await self.set_mode(self.nickname, "+B")
    
    async def on_message(self, target, source, message):
        if source == self.nickname:
            return
        image_urls = []
        for e, m in enumerate(tex_pattern.findall(message)):
            if r"\[" in m:
                m = r"$$" + m[2:-2] + r"$$"
            else:
                m = r"$" + m[2:-2] + r"$"

            ok, res = tex.render_tex(source, m, e)
            if not ok:
                image_urls.append("Failed to render")
                continue

            with open(res, "rb") as f:
                r = requests.post(
                    "https://0x0.st/",
                    files={"file": f},
                    headers={"User-Agent": "curl/7.85.0"},
                )
                image_urls.append(r.text)

        if len(image_urls) < 1:
            return

        await self.message(target, f"\x02[TeX]\x02 {' | '.join(map(str.strip, image_urls))}".strip())
    
    async def on_invite(self, channel, by):
        await self.join(channel)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = Bot('TeXBot', realname="TeXBot 1.0")
client.run(addr, tls=bool(int(use_ssl)), tls_verify=False)