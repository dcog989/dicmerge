from dicmerge.scanner.base import Scanner


class PlainTextScanner(Scanner):
    extension = ".txt"

    @staticmethod
    def format_output(words: list[str]) -> str:
        return "\n".join(words) + "\n"
