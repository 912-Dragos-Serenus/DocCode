class LexicalError(RuntimeError):
    def __init__(self, text: str, *args):
        self.text = text
        super().__init__(*args)

    def __str__(self) -> str:
        return "Invalid token here -> " + self.text[:10]
