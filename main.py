from common_functions import show_table_average_salary
from fetch_from_headhunter import get_vacancies_from_hh
from fetch_from_super_job import get_vacancies_from_sj

if __name__ == "__main__":
    show_table_average_salary('HeadHunter Moscow', get_vacancies_from_hh())
    show_table_average_salary('SuperJob Moscow', get_vacancies_from_sj())
