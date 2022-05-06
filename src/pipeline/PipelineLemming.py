import pandas as pd
from src.pipeline.PipelineElement import PipelineElement
from nltk.stem import WordNetLemmatizer

class PipelineLemming(PipelineElement):
    def __init__(self):
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