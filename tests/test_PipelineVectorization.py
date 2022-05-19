import pandas as pd

from src.pipeline.PipelineVectorization import PipelineVectorization
from src.pipeline.PipelineElement import PipelineElement


class TestPipelineVectorization:
    def test_class_inheritance(self):
        assert issubclass(PipelineVectorization, PipelineElement)

    def test_vectorization(self):
        object = PipelineVectorization()
        data = pd.DataFrame(['she doesn’t study german on monday', 'cats hate water'])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        first_list = ['monday', 'on', 'german', 'study', 'doesn’t', 'she']
        second_list = ['water', 'hate', 'cats']

        assert data.iloc[0, 0].wv.index_to_key == first_list
        assert data.iloc[1, 0].wv.index_to_key == second_list
