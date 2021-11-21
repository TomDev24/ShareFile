import aiohttp
import asyncio
from time import time
import secrets
#import requests

# def synch_get():
#     r = requests.get('https://api.github.com/events')
#     print(r)


async def get_content(url, session):
    async with session.get(url) as res:
        data = await res.read()
        fname = "./files/" + secrets.token_hex(10) + ".jpg"
        with open(fname, "wb") as f:
            f.write(data)

async def get_files():
    url = "http://localhost:5000/files/2ca33637e35f7873.jpg"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(100):
            task = asyncio.create_task(get_content(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    t0 = time()
    asyncio.run(get_files())
    print("Time passed", time() - t0)
