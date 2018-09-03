from main import *
from Student import *

# print(addition(5, 3))

# testForLook()

myList = [3, 2, 5, 99, 324, 0]
for item in testGenerator(5, myList):
    # print(item)
    pass

print(Student.my_static_method())

hsStu = HighSchoolStudent()
# hsStu.set_student_name("john")
hsStu.set_age(15)

print(hsStu.get_student_name())
print(hsStu.get_age())
