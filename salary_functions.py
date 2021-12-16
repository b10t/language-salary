from terminaltables import SingleTable


def predict_salary(salary_from, salary_to):
    """Получение прогнозируемой зарплаты."""
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def get_average_salaries_table(title, salaries):
    """Получение таблицы по средним зарплатам."""
    salaries_table = []
    salaries_table.append(['Язык программирования', 'Найдено вакансий',
                          'Обработано вакансий', 'Средняя зарплата'])

    for language_name, salary_details in salaries.items():
        salaries_table.append([language_name, *salary_details.values()])

    table_instance = SingleTable(salaries_table, title)
    return table_instance.table
