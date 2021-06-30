class Card:
    def __init__(self, page_id, native, foreign, level, date_wrong) -> None:
        self.page_id = page_id
        self.native = (native,)
        self.foreign = foreign
        self.level = level
        self.date_wrong = date_wrong
        self.correct = None
