import csv
from my_exception import (InvalidNameException, InvalidSubjectException,
                          InvalidGradeException, InvalidTestResException)
import logging
import argparse


FORMAT = \
'{levelname:<8} - {asctime}. В модуле "{name}" ' \
'в строке {lineno:03d} функция "{funcName}()" ' \
'в {created} секунд записала сообщение: {msg}'


logging.basicConfig(format=FORMAT,
style='{',
filename="log_student.log",
encoding='UTF-8',
level=logging.ERROR,
filemode='a')

logger = logging.getLogger(__name__)


class CheckName:

    def __set_name__(self, owner, name):
        self._param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._param_name)\

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self._param_name, value)

    def validate(self, value):
        if not value.isalpha() or not value.istitle():
            raise InvalidNameException()


class Student:
    name = CheckName()
    surname = CheckName()
    patronymic = CheckName()


    def __init__(self, name: str, surname: str, patronymic: str, file_name: str):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.subjects = self.sub_from_csv(file_name)
        self.grades = {subject: [] for subject in self.subjects}
        self.test_results = {subject: [] for subject in self.subjects}


    def sub_from_csv(self, file_name: str):
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            return next(reader)


    def __str__(self):
        return f'Student: name = {self.name}, surname = {self.surname}, patronymic = {self.patronymic}'


    def add_grades(self, subject: str, grade: int):
        if subject not in self.subjects:
            raise InvalidSubjectException()
        if 2 > grade or grade > 5:
            raise InvalidGradeException()
        self.grades[subject].append(grade)


    def add_test_results(self, subject: str, t_res: int):
        if subject not in self.subjects:
            raise InvalidSubjectException()
        if 0 > t_res or t_res > 100:
            raise InvalidTestResException()
        self.test_results[subject].append(t_res)


    def average_grade(self):
        sum_grade = sum([sum(grade) for grade in self.grades.values()])
        sum_sub = sum([len(grade) for grade in self.grades.values()])
        if sum_sub:
            return sum_grade / sum_sub


    def average_test_results(self):
        for subject in self.subjects:
            if self.test_results[subject]:
                average_t_res = {subject: sum(self.test_results[subject]) / len(self.test_results[subject])}
            return average_t_res


def pars():
    parser = argparse.ArgumentParser(description='Info about student')
    parser.add_argument('-n' '--name', type=str, help='Student name')
    parser.add_argument('-s' '--surname', type=str, help='Student surname')
    parser.add_argument('-p' '--patronymic', type=str, help='Student patronymic')
    parser.add_argument('-fn' '--filename', type=str, help='CSV filename')
    args = parser.parse_args()

    try:
        st1 = Student(args.n__name, args.s__surname, args.p__patronymic, args.fn__filename)

        # ошибки для создания лога
        # st1.add_grades('physics', 10)
        # st1.add_test_results('literature', 50)
        st1.add_test_results('physics', 100500)


    except InvalidNameException:
        logger.error('Invalid value: full name should be istitle and isalpha')
    except InvalidSubjectException:
        logger.error(f'Subject not found')
    except InvalidGradeException:
        logger.error(f'Grade is invalid, it should be between 2 and 5')
    except InvalidTestResException:
        logger.error(f'Grade is invalid, it should be between 0 and 100')
    return st1



if __name__ == '__main__':
    print(pars())

    # вызов в командной строке: python student.py -n Ivan -s Ivanov -p Ivanovich -fn sub.csv
