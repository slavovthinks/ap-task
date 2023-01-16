import pandas as pd


def load_population_csv(path: str, name_col: str, code_col: str, population_col: str) -> pd.DataFrame:
    """
    Loads population data from a CSV file
    :param path: Path to the CSV file
    :param name_col: Country name column
    :param code_col: Country code column ex: USA, BGR
    :param population_col: Column containing country's total population
    :return: A pd.DataFrame with iso_code, population and name columns
    """
    country_population = pd.read_csv(
        path,
        usecols=[name_col, code_col, population_col],
        index_col=code_col
    )
    country_population.rename(columns={population_col: 'population', name_col: 'name'}, inplace=True)
    country_population.index.rename('iso_code', inplace=True)
    return country_population


def clean_population_data(population_data: pd.DataFrame) -> pd.DataFrame:
    """
    Removes countries which code starts with OWID_, sets NaN population to 0
    :param population_data:  A pd.DataFrame with iso_code, population and name columns
    :return:
    """
    cleaned = population_data.iloc[~population_data.index.str.startswith('OWID_')]
    cleaned.loc[cleaned['population'].isna(), 'population'] = 0
    return cleaned
