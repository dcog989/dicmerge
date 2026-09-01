from dicmerge.scanner.base import Scanner

_LO_HEADER = "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \n"


class LibreOfficeScanner(Scanner):
    extension = ".dic"
    skip_header = len(_LO_HEADER.splitlines())

    @staticmethod
    def format_output(words: list[str]) -> str:
        return _LO_HEADER + "\n".join(words) + "\n"
