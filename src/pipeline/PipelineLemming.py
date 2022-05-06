import nltk.downloader
import pandas as pd
from nltk.stem import WordNetLemmatizer

from src.pipeline.PipelineElement import PipelineElement


class PipelineLemming(PipelineElement):
    def __init__(self):
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()

        lemmatizer = WordNetLemmatizer()

        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])

        for x, subtitleTokens in enumerate(subtitles.values):
            for y, sentenceTokens in enumerate(subtitleTokens):
                for z, token in enumerate(sentenceTokens):
                    subtitles.values[x][y][z] = lemmatizer.lemmatize(token)

        processed_data['ProcessedSubtitles'] = subtitles

        return processed_data
