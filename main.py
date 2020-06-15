
import psycopg2 as pg


def create_basis():

    """
    Creating the tables' skeleton
    
    """
    cur.execute("CREATE TABLE IF NOT EXISTS student (id serial PRIMARY KEY, \
    name varchar(100) not null, gpa numeric(10,2), birth timestamptz)")
    cur.execute("CREATE TABLE IF NOT EXISTS course (id serial PRIMARY KEY, name varchar(100) not null)")
    cur.execute("INSERT into course (name) values ('Advanced Python')")
    cur.execute("CREATE TABLE IF NOT EXISTS student_course (id SERIAL PRIMARY KEY, student_id INTEGER REFERENCES student(id), \
    course_id INTEGER REFERENCES course(id))")
    connection.commit()


def create_db(tables):

    """
    Creating the very tables

    """
    cur.execute("CREATE TABLE %s (id serial PRIMARY KEY, name varchar(100) not null)" % (tables))
    connection.commit()


def get_students(course_id):

    """
    Providing data of students of a concrete course by its id
    
    """
    cur.execute("SELECT student.name, course.name FROM student_course join course on course.id = course_id join\
    student on student.id = student_id where course_id = %s" % (course_id))
    names = cur.fetchall()
    connection.commit()
    return names


def add_students(course_id, students):

    """
    Creating students and writing their data into a course

    """
    for student in students:

        print(student)
        cur.execute("INSERT into student (name, gpa, birth) values ('%s', '%s', '%s') RETURNING id" % \
                    (student['name'], student['gpa'], student['birth']))
        student_id = cur.fetchone()
        print(student_id[0])
        cur.execute("INSERT into student_course (student_id, course_id) values (%s, %s)" % (student_id[0], course_id))
    connection.commit()


def add_student(student):

    """
    Adding a new student
    
    """
    cur.execute("INSERT into student (name, gpa, birth) values ('%s', '%s', '%s')"\
    % (student['name'], student['gpa'], student['birth']))
    connection.commit()


def get_student(student_id):

    """
    Searching for a student by his/ her id
    
    """
    cur.execute("SELECT name FROM student where id = %s" % student_id)
    name = cur.fetchone()
    connection.commit()
    return name[0]


def main():

    """
    Main function with necessary key data
    
    """
    create_basis()

    students = ("""{'name': 'Vovchik Nekabaev', 'gpa': 8.9, 'birth': '1902-03-04'},
    {'name': 'George Bush Jr.', 'gpa': 10.1, 'birth': '1900-02-03'}
    {'name': 'Donald Trump', 'gpa': 11.1, 'birth': '1901-01-01'}""")
    
    add_students(1,students)
    get_students(1)
    get_student(2)

if __name__ == '__main__':

  connection = pg.connect(database='netology', user='netology', \
  host='local host', password='netology', \
  port='5432')
  cur = connection.cursor()

  main()

