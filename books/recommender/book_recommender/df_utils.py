import pandas


def load_dataframe_with_lowercase(name: str):
    """Load data from csv file as a lowecase strings."""
    return pandas.read_csv(
        name,
        encoding="cp1251",
        sep=";",
        on_bad_lines="skip",
        index_col=False,
        dtype='unicode'
    ).apply(lambda x: x.astype(str).str.lower())


def merge_two_dfs(
    df1: pandas.core.frame.DataFrame,
    df2: pandas.core.frame.DataFrame,
    key: str ="ISBN"):
    return pandas.merge(df1, df2, on=[key])

