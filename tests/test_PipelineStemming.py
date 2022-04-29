import pandas as pd

from src.pipeline.PipelineStemming import PipelineStemming
from src.pipeline.PipelineElement import PipelineElement


class TestPipelineStemming():
    def test_class_inheritance(self):
        assert issubclass(PipelineStemming, PipelineElement)

    def test_pipeline_lemming(self):
        object = PipelineStemming()
        
        first_subtitle = [['crying', 'cries', 'cry']]
        second_subtitle = [['program', 'programming', 'programer']]
        data = pd.DataFrame([first_subtitle, second_subtitle])
        data.columns = ['ProcessedSubtitles']

        data = object.process(data)

        first_subtitle_compare = [['cri', 'cri', 'cri']]
        second_subtitle_compare = [['program', 'program', 'program']]
        data_compare = pd.DataFrame([first_subtitle_compare, second_subtitle_compare])
        data_compare.columns = ['ProcessedSubtitles']

        assert data_compare.equals(data)