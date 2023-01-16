import pandas as pd


def load_vaccination_csv(path: str, code_col: str, total_col: str) -> pd.DataFrame:
    """
    Loads vaccination data from a CSV file
    :param path: path to the CSV file
    :param code_col: Name of the column that contains country_code/iso_code ex.: BGR, USA
    :param total_col: Name of the column that contains total vaccinated people value
    :return: A Dataframe with iso_code and total_vaccinated columns
    """
    vaccination_data = pd.read_csv(path, usecols=[code_col, total_col])
    vaccination_data.rename(columns={total_col: 'total_vaccinated', code_col: 'iso_code'}, inplace=True)
    return vaccination_data


def clean_vaccination_data(vaccination_data: pd.DataFrame) -> pd.DataFrame:
    """
    Removes countries with OWID_ prefix, sets NaN total_vaccinated to 0
    :param vaccination_data: A Dataframe with iso_code and total_vaccinated columns
    :return: A Dataframe with iso_code and total_vaccinated columns
    """
    cleaned = vaccination_data.loc[~vaccination_data['iso_code'].str.startswith('OWID_')]
    cleaned.loc[cleaned['total_vaccinated'].isna(), 'total_vaccinated'] = 0
    return cleaned.groupby('iso_code').max()
