import pandas as pd

from src.pipeline.StripPunctuation import StripPunctuation
from src.pipeline.PipelineElement import PipelineElement

class TestStripPunctuation():
    def test_class_inheritance(self):
         object = StripPunctuation()
         assert issubclass(PipelineElement,PipelineElement)
    def test_punctuation_stripping(self):
        object = StripPunctuation()
        data = pd.DataFrame(['test1!#$%&()*+,-./:;<=>?@[\\]^_`{|}~','test2'])
        data.columns = ['ProcessedSubtitles']
        data = object.process(data)
        data_compare = pd.DataFrame(['test1','test2'])
        data_compare.columns = ['ProcessedSubtitles']
        assert data_compare.equals(data)
