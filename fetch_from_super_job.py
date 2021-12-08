import os

import requests
from dotenv import load_dotenv

from common_functions import (calculation_of_average_salary,
                              get_dict_by_language,
                              get_list_programming_languages, predict_salary)


def get_superjob_token():
    load_dotenv()
    return os.getenv('SUPERJOB_KEY')


def predict_rub_salary_hh(salary):
    """Получение прогнозируемой зарплаты."""
    return predict_salary(salary['payment_from'], salary['payment_to'])


def get_vacancies_from_sj() -> list:
    """Получить список вакансий с superjob.ru"""
    vacancies_data = []
    for language in get_list_programming_languages():
        vacancies_data.append(get_vacancies_by_language(language))

    return vacancies_data


def get_vacancies_by_language(language) -> dict:
    """Получить вакансии по выбраному языку программирования с hh.ru

    Args:
        language (str): Язык программирования
    """
    response_content = fetch_vacancies_data(language)

    found_records = response_content['total']
    count_pages = round(found_records / 20)

    average_salary = []

    for page_number in range(count_pages):
        response_content = fetch_vacancies_data(language, page_number)

        for vacancy in response_content['objects']:
            if vacancy['currency'] == 'rub':
                average_salary.append(predict_rub_salary_hh(vacancy))

    language_dict = get_dict_by_language(
        language,
        found_records,
        len(average_salary),
        calculation_of_average_salary(average_salary))

    return language_dict


def fetch_vacancies_data(language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с superjob.ru

    Args:
        language (str): Язык программирования
        page (int, optional): Номер страницы. Defaults to 0.

    Returns:
        dict: Словарь с данными по вакансиям
    """
    headers = {'X-Api-App-Id': get_superjob_token()}
    payload = {'keyword': 'Программист %s' % language,
               't': 4,
               'period': 1,
               'catalogues': 48,
               'page': page}
    response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=payload)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    get_superjob_token()
