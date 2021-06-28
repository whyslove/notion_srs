import requests
import asyncio

from datetime import datetime
from core.notion_api import Notion


# filter_property = {
#     "filter": {
#         "property": "Next",
#         "formula": {"date": {"start": {"on_or_before": "2021-09-10T02:43:42Z"}}},
#     }
# }

# res = requests.post(
#     f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
#     headers=HEADERS,
#     data=filter_property,
# ).json()

# if res.get("results") is None:
#     raise Exception(res)
# else:
#     all_cards = res.get("results")

# today_cards = select_today_cards(all_cards)


# page_id = today_cards[0]["id"]


# page = requests.get(
#     f"https://api.notion.com/v1/blocks/{page_id}/children",
#     headers=HEADERS,
# ).json()

# print(page)
# # print(a.json())
# # print(cards_list)

# f = open("json.txt", mode="w")
# f.write(str(res))
# f.close()


async def start_app():
    stop = False
    db = Notion()
    print("Hello! Welcome to terminal version of Spaced Repetion System")
    while stop is not True:
        # ans = input("[s] - start quize, [n] - add new words, [q] - quit\n").lower()
        ans = "s"
        if ans == "s":
            # start_quize()
            await db.get_cards()
        elif ans == "n":
            add_new_words()
        elif ans == "q":
            stop = True
            print("Thanks for using!")
            continue
        else:
            print("Unrecognizible character, please answer question again")


if __name__ == "__main__":
    asyncio.run(start_app())
