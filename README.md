# notion_srs
This repository allows you to work with Notion Spaced Repetion template from terminal. 

This is useful for those people who needs easy accesible and cloud storage tool for learning something according to 
[forgetitng curve](https://www.mindtools.com/pages/article/forgetting-curve.htm)

To use this programm you have to
1. copy the original version of Spaced Repetion into your Notion
[here is the link to it](https://www.notion.so/Template-Spaced-Repetition-119e1f5778ae4062a418d5d1eab1a1b5). Important that you have to store what you want to learn in the main body of page, not in some property
2. to perform requests to Notion you have to achieve ```DATABASE_ID``` and ```NOTION_API_KEY```
So, read [this](https://developers.notion.com/docs/getting-started) article written by Notion developers and
store this information in `.env` file in the root directory of the project (near the file app.py). Note, that you have to
create this file by yourself.

Please follow this structure in `.env`
```
DATABASE_ID = {your_database_id}
NOTION_API_KEY = secret_{your api key} #without Bearer
```
