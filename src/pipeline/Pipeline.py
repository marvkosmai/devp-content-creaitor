import pandas as pd


class Pipeline:
    def __init__(self, data: pd.DataFrame):
        self.functions_queue = []
        self.data = pd.DataFrame(data)
        self.processed_data = self.data

    def add_step(self, function):
        if callable(function):
            self.functions_queue.append(function)
        else:
            t = type(function)
            message = 'Expected Callable function but got ' + str(t)
            raise TypeError(message)

    def run(self):
        self.processed_data = self.data
        for function in self.functions_queue:
            self.processed_data = function(self.processed_data)


if __name__ == '__main__':
    """
    P = Pipeline([1,2,3])
    P.add_step(lambda x : [y+1 for y in x])
    P.add_step(print)
    P.run()
    """
