from textual.widgets import Placeholder
from textual.reactive import reactive


DIGITS = {
    "0": [
        "0000",
        "00 00",
        "00 00",
        "00 00",
        "0000",
    ],
    "1": [
        "  11",
        "  11",
        "  11",
        "  11",
        "  11",
    ],
    "2": [
        "2222",
        "   22",
        "2222",
        "22",
        "2222",
    ],
    "3": [
        "3333",
        "   33",
        " 333",
        "   33",
        "3333",
    ],
    "4": [
        "44 44",
        "44 44",
        "444444",
        "   44",
        "   44",
    ],
    "5": [
        "555555",
        "55",
        "55555",
        "    55",
        "55555",
    ],
    "6": [
        "6666",
        "66",
        "6666",
        "66 66",
        "6666",
    ],
    "7": [
        "777777",
        "   77",
        "   77",
        "   77",
        "   77",
    ],
    "8": [
        "8888",
        "88 88",
        "8888",
        "88 88",
        "8888",
    ],
    "9": [
        "9999",
        "99 99",
        "9999",
        "   99",
        "9999",
    ],
    ":": [
        "  ",
        "88",
        "  ",
        "88",
        "  ",
    ],
}


class AsciiTime:
    """Render a time in ASCII art using Textual"""

    def __init__(self, mm_ss: str = "00:00"):
        self.mm_ss = mm_ss
        self.time = ""
        self.update_time()

    def on_mount(self) -> None:
        """Called when the widget is added to the app"""
        self.update_time()

    def update_time(self) -> None:
        """Update the time in ASCII art"""
        digit_lines = []
        for ch in self.mm_ss:
            digit_lines.append(DIGITS[ch])

        # Combine the digit lines horizontally
        combined_lines = []
        for line_parts in zip(*digit_lines):
            combined_lines.append("  ".join(line_parts))

        self.time = "\n".join(combined_lines)

    def __rich_console__(self, console) -> None:
        """Render the ASCII art time in the console"""
        console.print(self.time, end="\n")


def time_to_ascii(time_str: str) -> str:
    """Convert a time string (MM:SS) to ASCII art.

    Args:
        time_str: Time string in MM:SS format

    Returns:
        str: ASCII art representation of the time
    """
    timer = AsciiTime(time_str)
    return timer.time


if __name__ == "__main__":
    print("Testing AsciiTime:")
    timer = AsciiTime("12:34")
    print(timer.time)

    print("\nTesting time_to_ascii function:")
    print(time_to_ascii("12:34"))
    print(time_to_ascii("01:23"))
    print(time_to_ascii("45:00"))
