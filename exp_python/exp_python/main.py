from Student import Student

# r = requests.get('http://www.yahoo.com')
# print(r.content)
# print(r.status_code)

def addition(a=1, b=1):
    """Add two numbers, and return their sum"""
    sum_result = a + b
    return sum_result

def var_args(name, *args):
    print(name)
    print(args)


def named_args(name, **kwargs):
    print(kwargs['firstname'])
    print(kwargs['lastname'])


def execute():
    print('great')

    print('hello'.capitalize())
    str = list('hello')
    for ch in str:
        print(ch)

    try:
        num = 3
        name = 'john'
        print(num + name)
    except Exception as err:
        print(err)

    name = 'daniel'
    msg = f"nice to meet you {name}"
    print(msg)

    result = 'bigger' if 2 > 1 else 'smaller'
    print(result)

    print(addition())
    print(addition(3, 4))

    print('name', 1000, None, 'end')

    var_args('daniel', 'name', 'hell', 100)

    named_args('daniel', firstname='kate', lastname='smith')

    multiply = lambda x, y: x * y

    print(multiply(3, 4))
    student = Student('mark')
    print(student.get_student_name())
    student.change_name()
    print(student.get_student_name())
    print(Student.school)

    if "no empty":
        print("not empty")


def testForLook():
    myTuple = (1, "a string", False)
    for item in myTuple:
        print(item)

def testGenerator(count, iterable):
    counter = 0

    for item in iterable:
        if counter == count:
            return
        counter += 1
        yield item


if __name__ == "__main__":
    execute()
