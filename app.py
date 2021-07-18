import asyncio
from asyncio.coroutines import coroutine

from aioconsole import ainput
from datetime import datetime

from core.notion_api import Notion
from core.models import Card


async def start_app():
    db = Notion()
    print("Hello! Welcome to terminal version of Spaced Repetion System")
    while True:
        ans = await ainput("[s] - start quize, [n] - add new words, [q] - quit\n")
        if ans == "s":
            await start_quize(db)
        elif ans == "n":
            await add_new_words(db)
        elif ans == "q":
            print("Thanks for using!")
            break
        else:
            print("Unrecognizible character, please answer the question again \n")
    await db.session.close()


async def start_quize(db) -> None:
    print(
        """=================================================================================================
Rules of quize: you get a card in foreign language, press [ENTER] to flip it.
After you see the word in native, press [ENTER] - if you correct, type [q] for quit or type any key if you incorrect
================================================================================================="""
    )

    abort_quize = False
    task = None  # to handle situations while we want to quit no answering any word
    card = await db.get_next_card()
    while card is not None and abort_quize is False:
        print(card.native)
        ans = await ainput("-" * len(card.native))
        print(str(card.foreign), "\n")
        ans = await ainput("Are you correct? ")
        print("\n==================")
        if ans == "":
            card.level = int(card.level) + 1
            card.correct = True
        elif ans == "i":
            card.level = 1
            card.correct = False
        elif ans == "q":
            abort_quize = True
            if task != None:
                print("Please, waint untill all words will be updated")
                await task
        task = asyncio.create_task(db.update_card(card))
        card = await db.get_next_card()
    print("All words for today are gone, congratulations!\n")


async def add_new_words(db):
    print("==========================")
    print("Here you can add new words")
    while True:
        native = await ainput("Enter word in native language: ")
        foreign = await ainput("Enter word in foreign language: ")
        new_card = Card(
            page_id="", native=native, foreign=foreign, level=1, date_wrong=""
        )
        task = asyncio.create_task(db.add_card(new_card))
        ans = await ainput("Continue? Type [ENTER] to agree, any other key to stop ")
        if ans != "":
            print("Wait untill all words will be saved")
            await task
            break
        print("===========================")


if __name__ == "__main__":
    asyncio.run(start_app())
