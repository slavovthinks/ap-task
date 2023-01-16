import sqlite3
from typing import Callable

import pandas as pd
from pandas.io.sql import SQLiteTable


# TODO: Figure out how to supply on_conflict_keys and set_keys dynamically
def sqlite_upsert_method(table: SQLiteTable, conn: sqlite3.Connection, keys, data_iter):
    """A method for DataFrame.to_sql that upserts records in sqlite table"""
    columns = ', '.join(keys)
    query = f"""INSERT INTO {table.name} ({columns}) VALUES ({", ".join("?"*len(keys))})
                ON CONFLICT({keys[0]}) DO UPDATE SET {', '.join([f"{key} = ?" for key in keys])};
    """

    conn.executemany(query, (item*2 for item in data_iter))


def store_statistics_sqlite(db_path: str, table: str, statistics: pd.DataFrame):
    """
    Stores statistics to a SQLite table, if the table doesn't exists it will be created if table exists
    records will be upserted
    :param db_path: path to a SQLite database
    :param table: name of the table in which records will be stored
    :param statistics: A pandas DataFrame with `iso_code, name, population, total_vaccinated, percentage_vaccinated` cols
    """
    with sqlite3.connect(db_path) as con:
        statistics.to_sql(table, con, if_exists='append', method=sqlite_upsert_method)


class StatisticsGenerator:
    """
    A class for generating statistics from population and vaccination data.

    :param population_data: Dataframe containing population data.
    :param vaccination_data: Dataframe containing vaccination data.
    :param population_clean_method: A method for cleaning the population data before generating statistics.
    :param vaccination_clean_method: A method for cleaning the vaccination data before generating statistics.
    """
    def __init__(
            self,
            population_data: pd.DataFrame,
            vaccination_data: pd.DataFrame,
            population_clean_method: Callable[[pd.DataFrame], pd.DataFrame] = None,
            vaccination_clean_method: Callable[[pd.DataFrame], pd.DataFrame] = None
    ):
        self.population_data = population_data
        self.vaccination_data = vaccination_data
        self.population_clean_method = population_clean_method
        self.vaccination_clean_method = vaccination_clean_method

    def generate_statistics(self) -> pd.DataFrame:
        """
        Generates a statistics DataFrame with percentage_vaccinated column
        :return: A pandas DataFrame with `iso_code, name, population, total_vaccinated, percentage_vaccinated` cols
        """
        clean_population = self.population_clean_method(self.population_data) if self.population_clean_method else self.population_data
        clean_vaccination = self.vaccination_clean_method(self.vaccination_data) if self.vaccination_clean_method else self.vaccination_data
        statistics = clean_population.merge(clean_vaccination, on='iso_code')
        statistics['percentage_vaccinated'] = statistics['total_vaccinated'] / statistics['population'] * 100
        return statistics
