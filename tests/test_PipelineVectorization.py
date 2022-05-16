import pandas as pd

from src.pipeline.PipelineVectorization import PipelineVectorization
from src.pipeline.PipelineElement import PipelineElement


class TestPipelineVectorization:
    def test_class_inheritance(self):
        assert issubclass(PipelineVectorization, PipelineElement)

    def test_vectorization(self):
        object = PipelineVectorization()
        data = pd.DataFrame(['She doesn’t study German on Monday.', 'Cats hate water.'])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        first_list = [['she', 'doesn', 't', 'study', 'german', 'on', 'monday']]
        second_list = [['cats', 'hate', 'water']]
        data_compare = pd.DataFrame([first_list, second_list])
        data_compare.columns = ['ProcessedSubtitles']
        assert data_compare.equals(data)
