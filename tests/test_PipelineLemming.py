import pandas as pd

from src.pipeline.PipelineLemming import PipelineLemming
from src.pipeline.PipelineElement import PipelineElement



class TestPipelineLemming():
    def test_class_inheritance(self):
        assert issubclass(PipelineLemming, PipelineElement)

    def test_pipeline_lemming(self):
        object = PipelineLemming()
        
        first_subtitle = [['crying', 'cries', 'cry']]
        second_subtitle = [['laugh', 'laughs', 'laught']]
        data = pd.DataFrame([first_subtitle, second_subtitle])
        data.columns = ['ProcessedSubtitles']

        data = object.process(data)

        first_subtitle_compare = [['cry', 'cry', 'cry']]
        second_subtitle_compare = [['laugh', 'laugh', 'laught']]
        data_compare = pd.DataFrame([first_subtitle_compare, second_subtitle_compare])
        data_compare.columns = ['ProcessedSubtitles']

        assert data_compare.equals(data)