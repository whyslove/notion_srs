import asyncio

from aioconsole import ainput
from datetime import datetime

from core.notion_api import Notion


async def start_app():
    stop = False
    db = Notion()
    print("Hello! Welcome to terminal version of Spaced Repetion System")
    while stop is False:
        ans = await ainput("[s] - start quize, [n] - add new words, [q] - quit\n")
        if ans == "s":
            await start_quize(db)
        elif ans == "n":
            add_new_words()
        elif ans == "q":
            stop = True
            print("Thanks for using!")
            continue
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

    stop_quize = False
    asyncio.create_task(db._download_cards())
    card = await db.get_next_card()
    while card is not None and stop_quize is False:
        card_native = "".join(card.native)
        print(card_native)
        ans = await ainput("-" * len(card_native))
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
            stop_quize = True
            return None
        asyncio.create_task(db.update_card(card))
        card = await db.get_next_card()
    print("All words for today are gone, congratulations!\n")


if __name__ == "__main__":
    asyncio.run(start_app())
