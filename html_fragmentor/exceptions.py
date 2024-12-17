class MaxLengthExceededError(Exception):
    pass


class TagCanNotBeSplittenError(Exception):
    def __init__(self, tag) -> None:
        super().__init__(f"#{tag} can't be splitten!")
