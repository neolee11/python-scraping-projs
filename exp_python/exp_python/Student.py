import datetime

class Student:
    school = 'some school'

    @staticmethod
    def my_static_method():
        return datetime.datetime.now()

    def __init__(self, name):
        self.name = name

    def get_student_name(self):
        return self.name

    def set_student_name(self, name):
        self.name = name

    def change_name(self):
        self.__private_method('call private method ')

    def __private_method(self, msg):
        self.name = msg + self.name


class HighSchoolStudent(Student):

    def __init__(self):
        super(HighSchoolStudent, self).__init__("kate")

    def get_age(self):
        return self._age

    def set_age(self, age):
        self._age = age
