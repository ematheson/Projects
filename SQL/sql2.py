import sqlite3 as sql
import csv
import pandas as pd


def createTables():

    db = sql.connect("db")
    cur = db.cursor()

    cur.execute('DROP TABLE IF EXISTS "students"')
    cur.execute('DROP TABLE IF EXISTS "fields"')
    cur.execute('DROP TABLE IF EXISTS "grades"')
    cur.execute('DROP TABLE IF EXISTS "classes"')

    cur.execute('CREATE TABLE students (StudentID INT NOT NULL, Name TEXT, MajorCode INT NOT NULL, MinorCode INT NOT NULL);')
    cur.execute('CREATE TABLE fields (ID INT NOT NULL, Name TEXT);')
    cur.execute('CREATE TABLE grades (StudentID INT NOT NULL, ClassID INT NOT NULL, Grade TEXT);')
    cur.execute('CREATE TABLE classes (ClassID INT NOT NULL, Name TEXT);')

    with open('students.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO students VALUES(?, ?, ?, ?);", rows)

    with open('fields.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO fields VALUES(?, ?);", rows)

    with open('grades.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO grades VALUES(?, ?, ?);", rows)

    with open('classes.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO classes VALUES(?, ?);", rows)

    db.commit()
    db.close()

def prob1():
    """
    Specify relationships between columns in given sql tables.
    """
    print "One-to-one relationships:"
    print "StudentID -> Name"
    print "ID -> Name"
    print "ClassID -> Name"

    print "**************************"
    print "One-to-many relationships:"
    print "StudentID -> ClassID"   #students can be in multiple classes
    print "ClassID -> Grade"
    #majors can have multiple students

    print "***************************"
    print "Many-to-Many relationships:"
    print "StudentID -> Grade"


def prob2():
    """
    Write a SQL query that will output how many students belong to each major,
    including students who don't have a major.

    Return: A table indicating how many students belong to each major.
    """
    #Build your tables and/or query here

    createTables()

    query = "SELECT fields.Name, COUNT(students.Name) FROM students LEFT OUTER JOIN fields ON students.MajorCode=fields.ID GROUP BY fields.Name ORDER BY fields.Name;"

    db = sql.connect("db")
    cur = db.cursor()
    # This line will make a pretty table with the results of your query.
        ### query is a string containing your sql query
        ### db is a sql database connection
    result =  pd.read_sql_query(query, db)
    db.commit()
    db.close()
    return result


def prob3():
    """
    Select students who received two or more non-Null grades in their classes.

    Return: A table of the students' names and the grades each received.
    """
    #Build your tables and/or query here
    createTables()

    db = sql.connect("db")
    cur = db.cursor()

          #if there wasn't a Count there, would it return all of a students grades in a comma list of somethin?

    query = "SELECT students.Name, COUNT(grades.Grade) FROM students LEFT OUTER JOIN grades ON students.StudentID = grades.StudentID WHERE grades.Grade IS NOT 'NULL' GROUP BY students.Name HAVING COUNT(grades.Grade)>2;"

    result =  pd.read_sql_query(query, db)

    db.commit()
    db.close()
    return result


def prob4():
    """
    Get the average GPA at the school using the given tables.

    Return: A float representing the average GPA, rounded to 2 decimal places.
    """
    createTables()
    db = sql.connect("db")
    cur = db.cursor()


    query = "SELECT  ROUND(AVG(                              \
                CASE                                          \
                WHEN Grade IN ('A', 'A+', 'A-') THEN 4.0       \
                WHEN Grade IN ('B+', 'B', 'B-') THEN 3.0        \
                WHEN Grade IN ('C+', 'C', 'C-') THEN 2.0         \
                WHEN Grade IN ('D+', 'D', 'D-') THEN 1.0          \
                ELSE 0.0                                           \
                END ), 2) AS gpa                                    \
                FROM grades WHERE Grade IS NOT 'NULL';"


    result =  pd.read_sql_query(query, db)
    return result.iloc[0][0]


def prob5():
    """
    Find all students whose last name begins with 'C' and their majors.

    Return: A table containing the names of the students and their majors.
    """
    #Build your tables and/or query here
    createTables()

    db = sql.connect("db")
    cur = db.cursor()                                        

    query = "SELECT students.Name, fields.Name FROM students LEFT OUTER JOIN fields ON students.MajorCode=fields.ID WHERE students.Name LIKE '% C%';"

    result =  pd.read_sql_query(query, db)

    db.commit()
    db.close()
    return result

if __name__ == '__main__':
    #print prob3()
    #print prob4()
    #print prob5()