import gensim
import pandas as pd
from src.pipeline.PipelineElement import PipelineElement


class PipelineVectorization(PipelineElement):
    def __init__(self):
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()
        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])

        w2v_model_list = []
        for index, element in enumerate(subtitles.values):
            splitted_subtitle = [subtitles.iloc[index, 0].split(" ")]

            # create Pandas Series with define indexes
            splitted_subtitle_series = pd.Series(splitted_subtitle)

            w2v_model = gensim.models.Word2Vec(splitted_subtitle_series, vector_size=100, window=5, min_count=1)
            w2v_model_list.append(w2v_model)

        processed_data['ProcessedSubtitles'] = w2v_model_list
        return processed_data
