import json
import aiohttp
import json
import requests

from settings import settings
from datetime import datetime

from core.models import Card

filter_condition = {
    "property": "Next",
    "formula": {"date": {"on_or_before": str(datetime.now().strftime("%Y-%m-%d"))}},
}


#  def
class Notion:
    def __init__(self) -> None:
        self.HEADERS = {
            "Authorization": f"Bearer {settings.api_token}",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json",
        }
        self.DATABASE_ID = settings.database_id
        self.start_cursor = None

    def get_cards(self):
        end_of_pages = False
        cards = []
        while not end_of_pages:
            resp = requests.post(
                url=f"https://api.notion.com/v1/databases/{self.DATABASE_ID}/query",
                headers=self.HEADERS,
                json={
                    "next_cursor": self.start_cursor,
                    "filter": filter_condition,
                },
            ).json()
            for card in resp["results"]:
                page_id = card["id"]
                native = card["Name"]["title"]["text"]["content"]
                translation = self.get_page_body(page_id)
                level = card["properties"]["Level"]["select"]["name"]
                cards.append(Card(native, translation, level))

            if resp.get("has_more") is None:
                end_of_pages = False
            else:
                self.start_cursor = resp["next_cursor"]
                cards["has_more"] = True

        return cards

    def get_page_body(self, page_id: str):
        """Returns translation writen in main body of page"""
        page_id = ("").join(page_id.split("-"))
        resp = requests.get(
            url=f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=self.HEADERS,
        ).json()
        return resp["results"][0]["paragraph"]["text"]["text"]["content"]
