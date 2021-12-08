from common_functions import show_table_average_salary
from fetch_from_headhunter import get_vacancies_from_hh


if __name__ == "__main__":
    show_table_average_salary('HeadHunter Moscow', get_vacancies_from_hh())
