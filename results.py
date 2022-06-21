import pandas as pd


def append_result(result_obj: pd.DataFrame):
    new_row = pd.DataFrame(zip(list()))

    pd.concat([result_obj, new_row])
