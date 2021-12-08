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
