import pandas as pd
from src.vaccination import load_vaccination_csv, clean_vaccination_data
from tempfile import NamedTemporaryFile


def test_load_vaccination_csv():
    with NamedTemporaryFile() as f:
        path = f.name
        code_col = 'code_col'
        total_col = 'total_col'

    # Create a test CSV file to load
        test_data = {'code_col': ['BGR', 'USA', 'OWID_WRL'], 'total_col': [1000.0, 2000.0, 3000.0], 'rand_col': [1, 2, 3]}
        test_df = pd.DataFrame(test_data)
        test_df.to_csv(path, index=False)

        # Test that the loaded dataframe has the correct columns and data
        result = load_vaccination_csv(path, code_col, total_col)
        expected_columns = ['iso_code', 'total_vaccinated']
        expected_data = {'iso_code': ['BGR', 'USA', 'OWID_WRL'], 'total_vaccinated': [1000.0, 2000.0, 3000.0]}
        expected = pd.DataFrame(expected_data)

        assert list(result) == expected_columns
        assert result.equals(expected)


def test_clean_vaccination_data():
    # Create a test dataframe to clean
    test_data = {'iso_code': ['BGR', 'USA', 'OWID_WRL'], 'total_vaccinated': [1000.0, None, 3000.0]}
    test_df = pd.DataFrame(test_data)

    # Test that the cleaned dataframe has the correct columns and data
    result = clean_vaccination_data(test_df)
    expected_columns = ['total_vaccinated']
    expected_data = {'total_vaccinated': [1000.0, 0.0]}
    expected = pd.DataFrame(expected_data, index=['BGR', 'USA'])

    assert list(result) == expected_columns
    print(result)
    print(expected)
    assert result.equals(expected)
