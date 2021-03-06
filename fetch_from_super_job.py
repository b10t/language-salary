import os
from itertools import count
from statistics import mean

import requests

from salary_functions import predict_salary


def get_from_sj_salaries(programming_languages) -> dict:
    """Получить список зарплат с superjob.ru.

    Args:
        programming_languages (list): Список языков программирования для поиска

    Returns:
        dict: Словарь с данными по зарплатам
    """
    sj_token = os.getenv('SUPERJOB_KEY', '')

    salaries = {}
    for language in programming_languages:
        salaries[language] = get_salary_details(sj_token,
                                                language)

    return salaries


def get_salary_details(sj_token, language) -> dict:
    """Получить информацию по зарплате с superjob.ru.

    Args:
        sj_token (str): Токен от API SuperJob
        language (str): Язык программирования

    Returns:
        dict: Словарь с данными по вакансии
    """
    average_salaries = []

    for page_number in count():
        response_content = fetch_vacancies(sj_token,
                                           language,
                                           page_number)

        for vacancy in response_content['objects']:
            if vacancy['currency'] == 'rub':
                average_salaries.append(
                    predict_salary(vacancy['payment_from'],
                                   vacancy['payment_to']
                                   )
                )

        if not response_content['more']:
            break

    average_salaries = list(filter(None, average_salaries))

    salary_details = dict(
        vacancies_found=response_content['total'],
        vacancies_processed=len(average_salaries),
        average_salary=int(mean(average_salaries) if average_salaries else 0))

    return salary_details


def fetch_vacancies(sj_token, language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с superjob.ru.

    Args:
        sj_token (str): Токен от API SuperJob
        language (str): Язык программирования
        page (int, optional): Номер страницы. Defaults to 0.

    Returns:
        dict: Словарь с данными по вакансиям
    """
    moscow_region_id = 4
    publication_period = 0
    industries_catalog = 48

    headers = {'X-Api-App-Id': sj_token}
    payload = {'keyword': 'Программист %s' % language,
               't': moscow_region_id,
               'period': publication_period,
               'catalogues': industries_catalog,
               'page': page}
    response = requests.get(
        'https://api.superjob.ru/2.0/vacancies/',
        headers=headers,
        params=payload)
    response.raise_for_status()

    return response.json()
