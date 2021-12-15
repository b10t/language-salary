from itertools import count
from statistics import mean

import requests

from common_functions import predict_salary


def get_vacancies_from_hh(programming_languages) -> dict:
    """Получить список вакансий с hh.ru

    Args:
        programming_languages (list): Список языков программирования для поиска

    Returns:
        dict: Словарь с данными по вакансиям
    """
    vacancies = {}
    for language in programming_languages:
        vacancies[language] = get_vacancies_by_language(language)

    return vacancies


def get_vacancies_by_language(language) -> dict:
    """Получить вакансии по выбраному языку программирования с hh.ru

    Args:
        language (str): Язык программирования

    Returns:
        dict: Словарь с данными по вакансии
    """
    found_records = 0
    average_salary = []

    for page_number in count():
        response_content = fetch_vacancies(language, page_number)

        for vacancy in response_content['items']:
            if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
                average_salary.append(
                    predict_salary(
                        vacancy['salary']['from'],
                        vacancy['salary']['to'],
                    )
                )

        if response_content['pages'] - 1 == page_number:
            found_records = response_content['found']
            break

    average_salary = [salary for salary in average_salary if salary]

    vacancy_description = dict(
        vacancies_found=found_records,
        vacancies_processed=len(average_salary),
        average_salary=int(mean(average_salary) if average_salary else 0))

    return vacancy_description


def fetch_vacancies(language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с hh.ru

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
