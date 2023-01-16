from unittest.mock import Mock

import pandas as pd

from src.statistics import StatisticsGenerator


def test_generate_statistics():
    population_data = pd.DataFrame({'iso_code': ['BGR', 'USA'], 'population': [1000.0, 2000.0]})
    vaccination_data = pd.DataFrame({'iso_code': ['BGR', 'USA'], 'total_vaccinated': [500.0, 1500.0]})
    population_clean_method = Mock(return_value=population_data)
    vaccination_clean_method = Mock(return_value=vaccination_data)

    generator = StatisticsGenerator(population_data, vaccination_data, population_clean_method, vaccination_clean_method)
    statistics = generator.generate_statistics()

    # Assert that the population_clean_method and vaccination_clean_method mocks were called with the correct arguments
    population_clean_method.assert_called_once_with(population_data)
    vaccination_clean_method.assert_called_once_with(vaccination_data)

    # Assert that the generated statistics DataFrame has the correct columns and data
    expected_columns = ['iso_code', 'population', 'total_vaccinated', 'percentage_vaccinated']
    expected_data = {'iso_code': ['BGR', 'USA'], 'population': [1000.0, 2000.0], 'total_vaccinated': [500.0, 1500.0], 'percentage_vaccinated': [50.0, 75.0]}
    expected = pd.DataFrame(expected_data, columns=expected_columns)


    assert list(statistics) == expected_columns
    assert statistics.equals(expected)