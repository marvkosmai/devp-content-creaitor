import pandas as pd

from src.pipeline.RemoveStopwords import RemoveStopwords
from src.pipeline.PipelineElement import PipelineElement


class TestRemoveStopwords:
    def test_class_inheritance(self):
        assert issubclass(RemoveStopwords, PipelineElement)

    def test_remove_stopwords(self):
        object = RemoveStopwords()
        data = pd.DataFrame([
            'Nick likes to play football, however he is not too fond of tennis.',
            'The world is big.'
        ])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        data_compare = pd.DataFrame([
            'Nick likes play football, fond tennis.',
            'The world big.'
        ])
        data_compare.columns = ['ProcessedSubtitles']
        assert data_compare.equals(data)
