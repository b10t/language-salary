from dotenv import load_dotenv

from salary_functions import get_average_salary_table
from fetch_from_headhunter import get_vacancies_from_hh
from fetch_from_super_job import get_vacancies_from_sj


if __name__ == "__main__":
    load_dotenv()

    programming_languages = ['Python', 'Java', 'C#']

    print(get_average_salary_table('HeadHunter Moscow',
                                   get_vacancies_from_hh(
                                       programming_languages)))
    print(get_average_salary_table('SuperJob Moscow',
                                   get_vacancies_from_sj(
                                       programming_languages)))
