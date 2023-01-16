from src.population import load_population_csv, clean_population_data
from src.vaccination import load_vaccination_csv, clean_vaccination_data
from src.statistics import StatisticsGenerator, store_statistics_sqlite


def main():
    population_data = load_population_csv(
        './data/country_populations.csv',
        name_col='Country Name',
        code_col='Country Code',
        population_col='2020'
    )
    vaccination_data = load_vaccination_csv('./data/vaccinations.csv', code_col='iso_code', total_col='people_fully_vaccinated')

    statistics_generator = StatisticsGenerator(
        population_data,
        vaccination_data,
        population_clean_method=clean_population_data,
        vaccination_clean_method=clean_vaccination_data
    )

    statistics = statistics_generator.generate_statistics()

    store_statistics_sqlite('./zadacha.db', 'countries', statistics)


if __name__ == '__main__':
    main()



