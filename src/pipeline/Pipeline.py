import os

import pandas as pd

from src.pipeline.PipelineElement import PipelineElement


class Pipeline:
    def __init__(self, data: pd.DataFrame = None):
        self.functions_queue = []
        self.data = pd.DataFrame(data)
        self.processed_data = self.data

    def read_data_from_csv(self, csv_file: str, **kwargs) -> None:
        if not isinstance(csv_file, str):
            raise TypeError(str(type(csv_file)) + ' is not a str')
        if not os.path.isfile(csv_file):
            raise FileNotFoundError(str(csv_file) + " is not a valid file")
        if len(kwargs) == 0:
            self.data = pd.read_csv(csv_file)
        self.data = pd.read_csv(csv_file, **kwargs)

    def batch_read_data_from_csv(self, csv_list: list, *, ignore_errors=False, **kwargs) -> None:
        if not isinstance(csv_list, list):
            raise TypeError(str(type(csv_list)) + ' is not a list')
        if len(csv_list) == 0:
            raise IndexError('List is empty')
        for index, file in enumerate(csv_list):
            if not os.path.isfile(file):
                if not ignore_errors:
                    raise FileNotFoundError(str(file) + " is not a valid file")
                else:
                    print(str(file) + " is not a valid file")
                    continue
            self.data = pd.concat([self.data, pd.read_csv(file, **kwargs)])
        self.data.reset_index(drop=True, inplace=True)

    def add_step(self, PipelineElementSubclass) -> None:
        """
        Adds a PipelineElement to the process Pipline, Subclass must have process function,
        which must take a Pandas Dataframe as input and returns a pandas Dataframe
        """
        if not issubclass(type(PipelineElementSubclass), PipelineElement):
            raise TypeError(
                'Expected Subclass from PipelineElement function but got ' + str(type(PipelineElementSubclass)))
        self.functions_queue.append(PipelineElementSubclass.process)

    def remove_last_step(self) -> None:
        self.functions_queue = self.functions_queue[:-1]

    def run(self) -> None:
        """
        Runs the functions_queue in order on self.data, result written in self.processed_data
        """
        self.processed_data = self.data
        for function in self.functions_queue:
            self.processed_data = function(self.processed_data)
