import pandas as pd
from emot.emo_unicode import UNICODE_EMOJI
from src.pipeline.PipelineElement import PipelineElement


class EmojiToText(PipelineElement):
    def __int__(self):
        demoji.download_codes()
        pass

    def process(self, data: pd.DataFrame):
        processed_data = data.__deepcopy__()
        subtitles = pd.DataFrame(processed_data['ProcessedSubtitles'])
        for index, element in subtitles.iterrows():
            subtitles.iloc[index, 0] = self.__convert_emojis(element['ProcessedSubtitles'])

        processed_data['ProcessedSubtitles'] = subtitles
        return processed_data

    def __convert_emojis(self, text: str) -> str:
        for emot in UNICODE_EMOJI:
            text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()))
        return text
