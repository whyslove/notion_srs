from pydantic import BaseModel


class Card(BaseModel):
    page_id: str
    native: str
    foreign: str
    level: int
    date_wrong: str
    correct: bool = None
    # def __init__(self, page_id, native, foreign, level, date_wrong) -> None:
    #     self.page_id = page_id
    #     self.native = native
    #     self.foreign = foreign
    #     self.level = level
    #     self.date_wrong = date_wrong
    #     self.correct = None
