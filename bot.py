import pydle
import asyncio
import re
import tex
import os
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
        display_n = 0
        replace_n = 0
        new_message = ""

        for m in tex_pattern.findall(message):
            if r"\[" in m:
                m_2 = r"$$" + m[2:-2] + r"$$"
                new_message = message.replace(m, m_2)
                display_n += 1
            else:
                if display_n > 0:
                    await self.message(target, f"\x02[TeX]\x02 Cannot render inline math and display math in the same query".strip())
                    return
                m_2 = r"$" + m[2:-2] + r"$"
                new_message = message.replace(m, m_2)
            replace_n += 1

        if replace_n < 1:
            return

        ok, res = tex.render_tex(source, new_message, 0)
        if not ok:
            await self.message(target, f"\x02[TeX]\x02 Failed to render".strip())
            return
        
        with open(res, "rb") as f:
            r = requests.post(
                "https://0x0.st/",
                files={"file": f},
                headers={"User-Agent": "curl/7.85.0"},
            )
            image_urls.append(r.text)
            os.remove(res)
        
        if len(image_urls) < 1:
            return

        await self.message(target, f"\x02[TeX]\x02 {' | '.join(map(str.strip, image_urls))}".strip())
    
    async def on_invite(self, channel, by):
        await self.join(channel)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = Bot('TeXBot', realname="TeXBot 1.1")
client.run(addr, tls=bool(int(use_ssl)), tls_verify=False)