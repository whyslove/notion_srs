import asyncio
import aiohttp

from loguru import logger
from datetime import datetime

from settings import settings
from core.models import Card

FILTER_CONDITION = {
    "property": "Next",
    "formula": {"date": {"on_or_before": str(datetime.now().strftime("%Y-%m-%d"))}},
}

HEADERS = {
    "Authorization": f"Bearer {settings.api_token}",
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json",
}


class Notion:
    def __init__(self) -> None:
        self.DATABASE_ID = settings.database_id  # Id in Notion
        self.session = aiohttp.ClientSession()
        self.start_cursor = None
        self.cards = None  # will be asyncio.Queue

    async def get_next_card(self) -> Card:
        if self.cards == None:
            self.cards = asyncio.Queue()
            asyncio.create_task(self._download_cards())
        card = await self.cards.get()
        if card.page_id == "END":
            return None
        return card

    async def _download_cards(self) -> None:
        """Function to perform downloading cards from Notion and stores them in self.cards"""
        end_of_cards = False
        while end_of_cards is False:
            async with self.session.post(
                url=f"https://api.notion.com/v1/databases/{self.DATABASE_ID}/query",
                headers=HEADERS,
                json=self.compute_json_download_cards(),
            ) as resp:
                if resp.status != 200:
                    logger.error(f"{await resp.json()}")
                resp = await resp.json()
                for card in resp["results"]:
                    page_id = card["id"]
                    native = card["properties"]["Name"]["title"][0]["text"]["content"]
                    foreign = await self.get_page_body(page_id)
                    level = card["properties"]["Level"]["select"]["name"]
                    date_wrong = card["properties"]["Date Wrong"]["date"]["start"]
                    await self.cards.put(
                        Card(page_id, native, foreign, level, date_wrong)
                    )

                if resp.get("next_cursor") is None:
                    await self.cards.put(Card("END", "", "", -1, ""))
                    end_of_cards = True
                else:
                    self.start_cursor = resp["next_cursor"]

    async def get_page_body(self, page_id: str):
        """Returns foreign word writen in main body of page"""
        page_id = ("").join(page_id.split("-"))
        async with self.session.get(
            url=f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=HEADERS,
        ) as resp:
            if resp.status != 200:
                logger.error(f"{await resp.json()}")
            resp = await resp.json()
            return resp["results"][0]["paragraph"]["text"][0]["text"]["content"]

    async def update_card(self, card: Card) -> None:
        if card.correct == True:
            json = {"properties": {"Level": {"select": {"name": str(card.level)}}}}
        else:
            json = {
                "properties": {
                    "Level": {"select": {"name": str(card.level)}},
                    "Date Wrong": {
                        "date": {"start": str(datetime.now().strftime("%Y-%m-%d"))}
                    },
                }
            }
        async with self.session.patch(
            url=f"https://api.notion.com/v1/pages/{card.page_id}",
            headers=HEADERS,
            json=json,
        ) as resp:
            if resp.status != 200:
                logger.error(f"{await resp.json()}")

    async def add_card(self, card: Card) -> None:
        json = {
            "parent": {"database_id": self.DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": card.native}}]},
                "Level": {"select": {"name": str(1)}},
                "Date Wrong": {
                    "date": {"start": str(datetime.now().strftime("%Y-%m-%d"))}
                },
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "text": [{"type": "text", "text": {"content": card.foreign}}],
                    },
                }
            ],
        }
        async with self.session.post(
            url="https://api.notion.com/v1/pages", headers=HEADERS, json=json
        ) as resp:
            if resp.status != 200:
                logger.error(f"{await resp.json()}")

    def compute_json_download_cards(self) -> dict:
        # Start_cursor should be undefined to get 1st page, so this function needs for readbility
        if self.start_cursor == None:
            return {
                "filter": FILTER_CONDITION,
            }
        else:
            return {
                "start_cursor": self.start_cursor,
                "filter": FILTER_CONDITION,
            }
