import gensim
import pandas as pd
from src.pipeline.PipelineElement import PipelineElement


class PipelineVectorization(PipelineElement):
    def __init__(self):
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()
        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])

        temp = []
        for index, element in enumerate(subtitles.values):
            splitted_subtitle = subtitles.iloc[index, 0].split(" ")
            temp.append(splitted_subtitle)

        # create Pandas Series with define indexes
        x = pd.Series(temp)

        w2v_model = gensim.models.Word2Vec(x, vector_size=100, window=5, min_count=2)

        processed_data['ProcessedSubtitles'] = subtitles
        return processed_data
