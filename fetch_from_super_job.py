import os
from itertools import count
from statistics import mean

import requests

from salary_functions import predict_salary


def get_vacancies_from_sj(programming_languages) -> dict:
    """Получить список вакансий с superjob.ru

    Args:
        programming_languages (list): Список языков программирования для поиска

    Returns:
        dict: Словарь с данными по вакансиям
    """
    sj_token = os.getenv('SUPERJOB_KEY', '')

    vacancies = {}
    for language in programming_languages:
        vacancies[language] = get_vacancies_by_language(sj_token, language)

    return vacancies


def get_vacancies_by_language(sj_token, language) -> dict:
    """Получить вакансии по выбраному языку программирования с hh.ru

    Args:
        sj_token (str): Токен от API SuperJob
        language (str): Язык программирования

    Returns:
        dict: Словарь с данными по вакансии
    """
    found_records = 0
    average_salary = []

    for page_number in count():
        response_content = fetch_vacancies(sj_token,
                                           language,
                                           page_number)

        for vacancy in response_content['objects']:
            if vacancy['currency'] == 'rub':
                average_salary.append(
                    predict_salary(vacancy['payment_from'],
                                   vacancy['payment_to']
                                   )
                )

        if not response_content['more']:
            found_records = response_content['total']
            break

    average_salary = [salary for salary in average_salary if salary]

    vacancy_description = dict(
        vacancies_found=found_records,
        vacancies_processed=len(average_salary),
        average_salary=int(mean(average_salary) if average_salary else 0))

    return vacancy_description


def fetch_vacancies(sj_token, language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с superjob.ru

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
