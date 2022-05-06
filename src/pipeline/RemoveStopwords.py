import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
from src.pipeline.PipelineElement import PipelineElement


class RemoveStopwords(PipelineElement):
    def __int__(self):
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()
        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])
        for index, element in subtitles.iterrows():
            subtitles.iloc[index, 0] = remove_stopwords(element['ProcessedSubtitles'])

        processed_data['ProcessedSubtitles'] = subtitles
        return processed_data
