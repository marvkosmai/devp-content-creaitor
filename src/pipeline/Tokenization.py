import pandas as pd
from src.pipeline.PipelineElement import PipelineElement
from gensim.utils import tokenize


class Tokenization(PipelineElement):
    def __init__(self):
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()
        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])
        for index, element in enumerate(subtitles.values):
            subtitles.iloc[index, 0] = list(tokenize(subtitles.iloc[index, 0], lowercase=True))

        processed_data['ProcessedSubtitles'] = subtitles
        return processed_data
