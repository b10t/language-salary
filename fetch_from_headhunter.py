import requests

from common_functions import (calculation_of_average_salary,
                              get_dict_by_language,
                              get_list_programming_languages,
                              predict_rub_salary)


def get_vacancies_from_hh() -> list:
    """Получить список вакансий с hh.ru"""
    vacancies_data = []
    for language in get_list_programming_languages():
        vacancies_data.append(get_vacancies_by_language(language))
        # TODO удалить
        # break

    return vacancies_data


def get_vacancies_by_language(language) -> dict:
    """Получить вакансии по выбраному языку программирования с hh.ru

    Args:
        language (str): Язык программирования
    """
    response_content = fetch_vacancies_data(language)

    found_records = response_content['found']
    count_pages = response_content['pages']

    average_salary = []

    # TODO вернуть count_pages
    for page_number in range(1):
        response_content = fetch_vacancies_data(language, page_number)

        for vacancy in response_content['items']:
            if vacancy['salary']:
                if vacancy['salary']['currency'] == 'RUR':
                    average_salary.append(
                        predict_rub_salary(
                            vacancy['salary']
                        )
                    )

    language_dict = get_dict_by_language(
        language,
        found_records,
        len(average_salary),
        calculation_of_average_salary(average_salary))

    return language_dict


def fetch_vacancies_data(language, page=0) -> dict:
    """Получить данные по выбраному языку программирования с hh.ru

    Args:
        language (str): Язык программирования
        page (int, optional): Номер страницы. Defaults to 0.

    Returns:
        dict: Словарь с данными по вакансиям
    """
    payload = {'text': 'Программист %s' % language,
               'area': 1,
               'period': 1,
               'page': page}
    response = requests.get(
        'https://api.hh.ru/vacancies',
        params=payload)
    response.raise_for_status()

    return response.json()


if __name__ == "main":
    print(get_vacancies_from_hh())
