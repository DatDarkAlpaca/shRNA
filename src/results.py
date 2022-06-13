import pandas as pd


class ResultBuilder:
    def __init__(self):
        self.results = {}

    def build_results(self, filename: str):
        return pd.DataFrame(list(zip(self.results.values())), columns=self.results.keys()).to_csv(filename)

    def add_result(self, column_name: str, value: str):
        self.results[column_name] = value
