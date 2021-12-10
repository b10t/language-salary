import os
from itertools import count

import requests

from common_functions import LIST_PROGRAMMING_LANGUAGES, predict_salary

MOSCOW_REGION_ID = 4
PUBLICATION_PERIOD = 1
INDUSTRIES_CATALOG = 48


def get_vacancies_from_sj() -> dict:
    """Получить список вакансий с superjob.ru"""
    sj_token = os.getenv('SUPERJOB_KEY', '')

    vacancies_data = {}
    for language in LIST_PROGRAMMING_LANGUAGES:
        vacancies_data[language] = get_vacancies_by_language(sj_token,
                                                             language)

    return vacancies_data


def get_vacancies_by_language(sj_token, language) -> dict:
    """Получить вакансии по выбраному языку программирования с hh.ru

    Args:
        language (str): Язык программирования
    """
    response_content = fetch_vacancies_data(sj_token, language)

    found_records = response_content['total']
    number_page = count()

    average_salary = []

    while True:
        response_content = fetch_vacancies_data(sj_token,
                                                language,
                                                next(number_page))

        for vacancy in response_content['objects']:
            if vacancy['currency'] == 'rub':
                average_salary.append(
                    predict_salary(vacancy['payment_from'],
                                   vacancy['payment_to']
                                   )
                )

        if not response_content['more']:
            break

    language_dict = dict(
        vacancies_found=found_records,
        vacancies_processed=len(average_salary),
        average_salary=int(sum(average_salary) / len(average_salary)))

    return language_dict


def fetch_vacancies_data(sj_token, language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с superjob.ru

    Args:
        language (str): Язык программирования
        page (int, optional): Номер страницы. Defaults to 0.

    Returns:
        dict: Словарь с данными по вакансиям
    """
    headers = {'X-Api-App-Id': sj_token}
    payload = {'keyword': 'Программист %s' % language,
               't': MOSCOW_REGION_ID,
               'period': PUBLICATION_PERIOD,
               'catalogues': INDUSTRIES_CATALOG,
               'page': page}
    response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=payload)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    print(get_vacancies_from_sj())
