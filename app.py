import requests

from settings import settings

HEADERS = {
    "Authorization": f"Bearer {settings.api_token}",
    "Notion-Version": "2021-05-13",
}
DATABASE_ID = settings.database_id

# a = requests.post(
#     f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=HEADERS
# )
# print(a.json())

a = requests.get(
    f"https://api.notion.com/v1/blocks/1feebd9c-1a53-40b2-af88-44bee9cf6617/children?page_size=100",
    headers=HEADERS,
)
print(a.json())
