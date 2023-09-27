class MyException(Exception):
    pass

class InvalidNameException(MyException):
    def __init__(self):
        self.message = 'Invalid value: full name should be istitle and isalpha'
        super().__init__(self.message)

class InvalidSubjectException(MyException):
    def __init__(self):
        self.message = f'Subject not found'
        super().__init__(self.message)


class InvalidGradeException(MyException):
    def __init__(self):
        self.message = f'Grade is invalid, it should be between 2 and 5'
        super().__init__(self.message)


class InvalidTestResException(MyException):
    def __init__(self):
        self.message = f'Grade is invalid, it should be between 0 and 100'
        super().__init__(self.message)