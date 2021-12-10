import requests

from common_functions import LIST_PROGRAMMING_LANGUAGES, predict_salary

MOSCOW_REGION_ID = 1


def get_vacancies_from_hh() -> list:
    """Получить список вакансий с hh.ru"""
    vacancies_data = []
    for language in LIST_PROGRAMMING_LANGUAGES:
        vacancies_data.append(get_vacancies_by_language(language))

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

    for page_number in range(count_pages):
        response_content = fetch_vacancies_data(language, page_number)

        for vacancy in response_content['items']:
            if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
                average_salary.append(
                    predict_salary(
                        vacancy['salary']['from'],
                        vacancy['salary']['to'],
                    )
                )

    language_dict = {language: dict(
        vacancies_found=found_records,
        vacancies_processed=len(average_salary),
        average_salary=int(sum(average_salary) / len(average_salary)))}

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
               'area': MOSCOW_REGION_ID,
               'page': page}
    response = requests.get(
        'https://api.hh.ru/vacancies',
        params=payload)
    response.raise_for_status()

    return response.json()


if __name__ == "main":
    print(get_vacancies_from_hh())
