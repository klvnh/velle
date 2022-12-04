import aiohttp
from bs4 import BeautifulSoup

class IconScraper:
    def __init__(self, bot):
        self.bot = bot

    async def pinterest(self, url : str):
        URL = url
        page = await self.bot.session.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
        html = await page.text()
        soup = BeautifulSoup(html, 'html.parser')
        return [image['src'] for image in soup.findAll('img')]