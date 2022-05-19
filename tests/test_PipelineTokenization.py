import pandas as pd

from src.pipeline.PipelineElement import PipelineElement
from src.pipeline.PipelineTokenization import PipelineTokenization


class TestPipelineTokenization:
    def test_class_inheritance(self):
        assert issubclass(PipelineTokenization, PipelineElement)

    def test_tokenization(self):
        object = PipelineTokenization()
        data = pd.DataFrame(['She doesn’t study German on Monday.', 'Cats hate water.'])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        first_list = [['she', 'doesn', 't', 'study', 'german', 'on', 'monday']]
        second_list = [['cats', 'hate', 'water']]
        data_compare = pd.DataFrame([first_list, second_list])
        data_compare.columns = ['ProcessedSubtitles']
        assert data_compare.equals(data)
