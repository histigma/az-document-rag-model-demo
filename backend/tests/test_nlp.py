import pytest
from modules.nlp.text_process import TextDataChunker, Document


def test_text_chunker():
    c = TextDataChunker()
    cs = c.from_text(
        "dsadwqlkej2io1e\n2nudfn akjsdcnsajkfwqnbhidbwiqdnqiqwd\n\n\n\ndkqndjwqbdijkqwdnjqw"
    )
    assert isinstance(cs, list)
    assert all(isinstance(c, Document) for c in cs)

