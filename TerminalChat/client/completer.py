from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from typing import Iterable

class Completer1(Completer):
    def __init__(self, words, ignore_case=False) -> None:
        self.words = words
        self.ignore_case = ignore_case
        self.display_dict = {}
        super().__init__()

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
            if self.ignore_case:
                word_before_cursor = word_before_cursor.lower()
            word_before_cursor = document.get_word_before_cursor()

            def word_matches(word: str) -> bool:
                """True when the word before the cursor matches."""
                # word_before_cursor = word_before_cursor
                if self.ignore_case:
                    word = word.lower()
                if not word_before_cursor.startswith('@'):
                    return False
                cursor_word = word_before_cursor.removeprefix('@')
                return word.startswith(cursor_word)

            for a in self.words:
                if word_matches(a):
                    yield Completion(
                        text=a,
                        start_position=-len(word_before_cursor) + 1,
                    )