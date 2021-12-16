from itertools import count
from statistics import mean

import requests

from salary_functions import predict_salary


def get_from_hh_salaries(programming_languages) -> dict:
    """Получить список зарплат с hh.ru.

    Args:
        programming_languages (list): Список языков программирования для поиска

    Returns:
        dict: Словарь с данными по зарплатам
    """
    salaries = {}
    for language in programming_languages:
        salaries[language] = get_salary_details(language)

    return salaries


def get_salary_details(language) -> dict:
    """Получить информацию по зарплате с hh.ru.

    Args:
        language (str): Язык программирования

    Returns:
        dict: Словарь с данными по зарплате
    """
    records_found = 0
    average_salaries = []

    for page_number in count():
        response_content = fetch_vacancies(language, page_number)

        for vacancy in response_content['items']:
            if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
                average_salaries.append(
                    predict_salary(
                        vacancy['salary']['from'],
                        vacancy['salary']['to'],
                    )
                )

        if response_content['pages'] - 1 == page_number:
            records_found = response_content['found']
            break

    average_salaries = list(filter(None, average_salaries))

    salary_details = dict(
        vacancies_found=records_found,
        vacancies_processed=len(average_salaries),
        average_salary=int(mean(average_salaries) if average_salaries else 0))

    return salary_details


def fetch_vacancies(language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с hh.ru.

    Args:
        language (str): Язык программирования
        page (int, optional): Номер страницы. Defaults to 0.

    Returns:
        dict: Словарь с данными по вакансии
    """
    moscow_region_id = 1

    payload = {'text': 'Программист %s' % language,
               'area': moscow_region_id,
               'page': page}
    response = requests.get(
        'https://api.hh.ru/vacancies',
        params=payload)
    response.raise_for_status()

    return response.json()
