from dotenv import load_dotenv

from salary_functions import get_average_salaries_table
from fetch_from_headhunter import get_from_hh_salaries
from fetch_from_super_job import get_from_sj_salaries


if __name__ == "__main__":
    load_dotenv()

    programming_languages = ['Python', 'Java', 'C#']

    print(get_average_salaries_table('HeadHunter Moscow',
                                     get_from_hh_salaries(
                                         programming_languages)))
    print(get_average_salaries_table('SuperJob Moscow',
                                     get_from_sj_salaries(
                                         programming_languages)))
