import pandas as pd

from src.pipeline.EmojiToText import EmojiToText
from src.pipeline.PipelineElement import PipelineElement


class TestEmojiToText:
    def test_class_inheritance(self):
        assert issubclass(EmojiToText, PipelineElement)

    def test_emoji_to_text(self):
        object = EmojiToText()
        data = pd.DataFrame([
            'The party im hosting for you is going to be 🔥',
            'Hello 👋'
        ])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        data_compare = pd.DataFrame([
            'The party im hosting for you is going to be fire',
            'Hello waving_hand'
        ])
        data_compare.columns = ['ProcessedSubtitles']
        assert data_compare.equals(data)
