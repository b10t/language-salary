from terminaltables import SingleTable


def predict_salary(salary_from, salary_to):
    """Получение прогнозируемой зарплаты."""
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def get_average_salary_table(title, vacancies):
    """Отобразить таблицу по языкам программирования, со средней зарплатой."""

    vacancy_table = []
    vacancy_table.append(['Язык программирования', 'Найдено вакансий',
                          'Обработано вакансий', 'Средняя зарплата'])

    for language_name, vacancy_description in vacancies.items():
        vacancy_table.append([language_name, *vacancy_description.values()])

    table_instance = SingleTable(vacancy_table, title)
    return table_instance.table
