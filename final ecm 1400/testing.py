from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from time_conversion import hhmm_to_seconds
from covid_news_handling import news_API_request

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last_7_days , hospital_cases , cumulative_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last_7_days == 240_299
    assert hospital_cases == 7_019
    assert cumulative_deaths == 141_544


def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_hmm_to_seconds():
    assert hhmm_to_seconds("2:30") == 2.5*60**2


def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()


test_parse_csv_data()
test_process_covid_csv_data()
test_covid_API_request()
test_hmm_to_seconds()
test_news_API_request()