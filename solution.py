from collections import OrderedDict
import csv


class Student(object):
    """docstring for Student"""
    def __init__(self, name, sid):
        self._name = name
        self._id = sid
        self._courses = OrderedDict()
        self._courses_with_dupl = OrderedDict()

    def __str__(self):
        res = ''
        res += 'Name: ' + self._name + '\n'
        res += 'ID: ' + str(self._id) + '\n'
        res += 'Courses:\n\t'
        if len(self._courses) == 0:
            res += "Didn't take any courses yet"
        else:
            courses = {}
            semesters = []

            # for tup in self._courses.values():
            #     if tup[0] not in semesters:
            #         semesters.append(tup[0])
            #     if tup[0] not in courses:
            #         courses[tup[0]] = [(tup[1], tup[2],)]
            #     else:
            #         courses[tup[0]].append((tup[1], tup[2],))

            for item in self._courses_with_dupl.values():
                if type(item) is tuple:
                    if item[0] not in semesters:
                        semesters.append(item[0])
                    if item[0] not in courses:
                        courses[item[0]] = [(item[1], item[2],)]
                    else:
                        courses[item[0]].append((item[1], item[2],))
                else:
                    for tup in item:
                        if tup[0] not in semesters:
                            semesters.append(tup[0])
                        if tup[0] not in courses:
                            courses[tup[0]] = [(tup[1], tup[2],)]
                        else:
                            courses[tup[0]].append((tup[1], tup[2],))
            for semester in semesters:
                res += '\n\t' + semester + '\n\t\t'
                for course, grade in courses[semester]:
                    res += course.get_id() + ': ' + course.get_name() + ': ' + str(grade) + '\n\t\t'

        return res

    def add_course(self, semester, course, grade):
        cid = course.get_id()
        if cid in self._courses:
            del self._courses[cid]
        self._courses[cid] = (semester, course, grade)

        if cid not in self._courses_with_dupl:
            self._courses_with_dupl[cid] = [(semester, course, grade)]
        else:
            self._courses_with_dupl[cid].append((semester, course, grade))


class Curriculum(object):
    """docstring for Curriculum"""
    def __init__(self):
        self._courses = []
        self._courses_by_id = {}

    def add_course(self, course):
        self._courses.append(course)
        self._courses_by_id[course.get_id()] = self._courses[-1]

    def get_course(self, cid):
        return self._courses_by_id[cid]

    def __str__(self):
        res = ''
        for course in self._courses:
            res += str(course) + '\n'
        return res


class Course(object):
    """docstring for Course"""
    def __init__(self, cid, name, pre, weight):
        self._name = name
        self._id = cid
        self._weight = weight
        if pre != '':
            self._pre = pre.split(sep=',')
        else:
            self._pre = []

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_weight(self):
        return self._weight

    def get_pre(self):
        return self._pre[:]

    def __str__(self):
        res = ''
        res += self._id + '\t\t' + self._name + '\t\t' + str(self._pre) + '\t\t' + str(self._weight)
        return res


# opening the curriculum file and retrieving its content into a list of tuples
with open('curriculum.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    curriculum_lst = []
    for row in reader:
        # making a list of tuples representing entries imported
        curriculum_lst.append((row[0].strip(), row[1].strip(), row[2].strip(), float(row[3])))


# Making the curriculum
curriculum = Curriculum()
for tup in curriculum_lst:
    course = Course(*tup)
    curriculum.add_course(course)


# opening the sample student file and retrieving its content into a list of tuples
with open('example_student_01.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    student_data_lst = []
    for row in reader:
        student_data_lst.append((row[0].strip(), row[1].strip(), row[2].strip()))


# Making a student
student = Student('random name', '000000')
for tup in student_data_lst:
    course = Course(tup[1], curriculum.get_course(tup[1]).get_name(), ','.join(curriculum.get_course(tup[1]).get_pre()), curriculum.get_course(tup[1]).get_weight())
    student.add_course(tup[0],
                       course,
                       tup[2])

print(student)
