import os

import requests

from common_functions import LIST_PROGRAMMING_LANGUAGES, predict_salary


def get_vacancies_from_sj() -> list:
    """Получить список вакансий с superjob.ru"""
    sj_token = os.getenv('SUPERJOB_KEY', '')

    vacancies_data = []
    for language in LIST_PROGRAMMING_LANGUAGES:
        vacancies_data.append(get_vacancies_by_language(sj_token, language))

    return vacancies_data


def get_vacancies_by_language(sj_token, language) -> dict:
    """Получить вакансии по выбраному языку программирования с hh.ru

    Args:
        language (str): Язык программирования
    """
    response_content = fetch_vacancies_data(sj_token, language)

    found_records = response_content['total']
    count_pages = round(found_records / 20)

    average_salary = []

    for page_number in range(count_pages):
        response_content = fetch_vacancies_data(sj_token,
                                                language,
                                                page_number)

        for vacancy in response_content['objects']:
            if vacancy['currency'] == 'rub':
                average_salary.append(
                    predict_salary(vacancy['payment_from'],
                                   vacancy['payment_to']
                                   )
                )

    language_dict = {language: dict(
        vacancies_found=found_records,
        vacancies_processed=len(average_salary),
        average_salary=int(sum(average_salary) / len(average_salary)))}

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
    print(get_vacancies_from_sj())
