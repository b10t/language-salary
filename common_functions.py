from terminaltables import SingleTable

LIST_PROGRAMMING_LANGUAGES = ['Python', 'Java', 'C#']


def predict_salary(salary_from, salary_to):
    """Получение прогнозируемой зарплаты."""
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    else:
        return salary_to * 0.8


def show_table_average_salary(title, vacancies_data):
    """Отобразить таблицу по языкам программирования, со средней зарплатой."""

    table_data = []
    table_data.append(('Язык программирования', 'Найдено вакансий',
                       'Обработано вакансий', 'Средняя зарплата'))

    for language, language_data in vacancies_data.items():
        table_data.append(tuple([language, *language_data.values()]))

    table_instance = SingleTable(table_data, title)
    print(table_instance.table)
