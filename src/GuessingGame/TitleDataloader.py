import pandas as pd
import os


class TitleDataloader():

    def __init__(self, csvDelimeter: str = ",", path: str = "data/generated/tom_scott_videos_latest.csv"):
        # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fileName)
        self.data = pd.read_csv(path, delimiter=csvDelimeter)

    def load(self, shuffle=True):
        if shuffle:
            return self.data.sample(frac=1)

        return self.data
