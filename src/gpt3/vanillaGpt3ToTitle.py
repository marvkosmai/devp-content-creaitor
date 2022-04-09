import openai
import pandas as pd
from tqdm import tqdm

from src import apikeys
from src.subtitle.SubtitleToStorage import SubtitlesToStorage

openai.api_key = apikeys.OPENAI_API_KEY

videos = pd.read_csv('../../data/videos/tom_scott_videos.csv')

generated_titles = list()
for _, row in tqdm(videos.iterrows(), total=videos.shape[0]):
    subtitle_downloader = SubtitlesToStorage(
        source='youtube',
        video_id=row['video_id'],
        storage_config={'type': 'return_value'}
    )

    subtitles = subtitle_downloader.save()

    prompt = 'Write a title for these subtitles: \n' + subtitles
    prompt = prompt[:3999]

    response = openai.Completion.create(
      engine='text-davinci-002',
      prompt=prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    title = response['choices'][0]['text'].strip()
    generated_titles.append(title)

videos['gpt3_vanilla_title'] = generated_titles
videos.to_csv('../../data/generated/tom_scott_videos_gpt3_vanilla.csv')
