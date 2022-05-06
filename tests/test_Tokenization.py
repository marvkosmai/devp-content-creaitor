import pandas as pd

from src.pipeline.PipelineElement import PipelineElement
from src.pipeline.Tokenization import Tokenization


class TestTokenization():
    def test_class_inheritance(self):
        assert issubclass(Tokenization, PipelineElement)

    def test_tokenization(self):
        object = Tokenization()
        data = pd.DataFrame(['She doesn’t study German on Monday.', 'Cats hate water.'])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        first_list = [['she', 'doesn', 't', 'study', 'german', 'on', 'monday']]
        second_list = [['cats', 'hate', 'water']]
        data_compare = pd.DataFrame([first_list, second_list])
        data_compare.columns = ['ProcessedSubtitles']
        assert data_compare.equals(data)
