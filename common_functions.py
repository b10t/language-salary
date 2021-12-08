from terminaltables import SingleTable


def get_list_programming_languages():
    """Получить список языков программирования."""
    return ['Python', 'Java', 'C#']


def predict_rub_salary(salary):
    """Получение прогнозируемой зарплаты."""
    salary_from = salary['from']
    salary_to = salary['to']

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    else:
        return salary_to * 0.8


def calculation_of_average_salary(average_salary):
    """Расчет средней заработной платы.

    Args:
        average_salary (list): Список зарплат
    """
    return int(sum(average_salary) / len(average_salary))


def get_dict_by_language(language,
                         vacancies_found,
                         vacancies_processed,
                         average_salary) -> dict:
    """Возвращает словарь по данным языка.

    Args:
        language (str): Название языка программирования
        vacancies_found (int): Количество найденных вакансий
        vacancies_processed (int): Количество обработанных вакансий
        average_salary (float): Средняя заработная плата
    """
    return {language: dict(
        vacancies_found=vacancies_found,
        vacancies_processed=vacancies_processed,
        average_salary=average_salary)}


def show_table_average_salary(title, vacancies_data):
    """Отобразить таблицу по языкам программирования, со средней зарплатой."""

    table_data = []
    table_data.append(('Язык программирования', 'Найдено вакансий',
                       'Обработано вакансий', 'Средняя зарплата'))

    for vacancy in vacancies_data:
        language = list(vacancy.keys())

        for value in list(vacancy.values())[0].values():
            language.append(value)

        table_data.append(tuple(language))

    table_instance = SingleTable(table_data, title)
    print(table_instance.table)
