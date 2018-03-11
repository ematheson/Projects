import sqlite3 as sql
import csv
import pandas as pd


def prob1():
    """
    Create the following SQL tables with the following columns:
        -- MajorInfo: MajorID (int), MajorName (string)
        -- CourseInfo CourseID (int), CourseName (string)
    --------------------------------------------------------------
    Do not return anything.  Just create the designated tables.
    """
    database = sql.connect("sql1")
    cur = database.cursor()

    cur.execute('DROP TABLE IF EXISTS "MajorInfo"')

    cur.execute('CREATE TABLE MajorInfo (MajorID INT NOT NULL, MajorName TEXT);')

    cur.execute('DROP TABLE if exists "CourseInfo"')

    cur.execute('CREATE TABLE CourseInfo (CourseID INT NOT NULL, CourseName TEXT);')

    database.commit()
    database.close()


def prob2():
    """
    Create the following SQL table with the following columns:
        -- ICD: ID_Number (int), Gender (string), Age (int) ICD_Code (string)
    --------------------------------------------------------------
    Do not return anything.  Just create the designated table. (and fill them)
    """
    db = sql.connect("sql2")
    cur = db.cursor()

    cur.execute('DROP TABLE if exists "ICD"')
    cur.execute('CREATE TABLE ICD (ID_Number INT NOT NULL, Gender TEXT, Age INT NOT NULL, ICD_Code TEXT);')

    with open('icd9.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO ICD VALUES(?, ?, ?, ?);", rows)

    #testing
    cur.execute("PRAGMA table_info('ICD')")
    for info in cur:
        print info

    db.commit()
    db.close()

def prob3():
    """
    Create the following SQL tables with the following columns:
        -- StudentInformation: StudentID (int), Name (string), MajorCode (int)
        -- StudentGrades: StudentID (int), ClassID (int), Grade (int)

    Populate these tables, as well as the tables from Problem 1, with
        the necesary information.  Also, use the column names for
        MajorInfo and CourseInfo given in Problem 1, NOT the column
        names given in Problem 3.
    ------------------------------------------------------------------------
    Do not return anything.  Just create the designated tables.
    """

    database = sql.connect("sql1")
    cur = database.cursor()

    cur.execute('DROP TABLE IF EXISTS "StudentInformation"')
    cur.execute('DROP TABLE IF EXISTS "MajorInfo"')
    cur.execute('DROP TABLE IF EXISTS "StudentGrades"')
    cur.execute('DROP TABLE IF EXISTS "CourseInfo"')

    cur.execute('CREATE TABLE StudentInformation (StudentID INT NOT NULL, Name TEXT, MajorCode INT NOT NULL);')
    cur.execute('CREATE TABLE MajorInfo (MajorID INT NOT NULL, MajorName TEXT);')
    cur.execute('CREATE TABLE StudentGrades (StudentID INT NOT NULL, ClassID INT NOT NULL, Grade TEXT);')
    cur.execute('CREATE TABLE CourseInfo (CourseID INT NOT NULL, CourseName TEXT);')

    with open('student_info.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO StudentInformation VALUES(?, ?, ?);", rows)

    with open('major_info.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO MajorInfo VALUES(?, ?);", rows)

    with open('student_grades.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO StudentGrades VALUES(?, ?, ?);", rows)

    with open('course_info.csv', 'rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    cur.executemany("INSERT INTO CourseInfo VALUES(?, ?);", rows)

    database.commit()
    database.close()


def prob4():
    """
    Find the number of men and women, respectively, between ages 25 and 35
    (inclusive).
    You may assume that your "sql1" and "sql2" databases have already been
    created.
    ------------------------------------------------------------------------
    Returns:
        (n_men, n_women): A tuple containing number of men and number of women
                            (in that order)
    """

    db = sql.connect("sql2")
    cur = db.cursor()

    cur.execute('SELECT Gender FROM ICD WHERE Age>24 AND Age<36;')

    f_counter = 0
    m_counter = 0

    for person in cur:
        #print person  (u'F') or (u'M')

        if str(person)[3] == 'M':
            m_counter +=1

        elif str(person)[3] == 'F':
            f_counter +=1


    return (m_counter, f_counter)


def useful_test_function(db, query):
    """
    Print out the results of a query in a nice format using pandas
    ------------------------------------------------------------------------
    Inputs:
        db: A sqlite3 database connection
        query: A string containing the SQL query you want to execute
    """

    print pd.read_sql_query(query, db)

if __name__ == '__main__':
    
    prob2()
    prob4()
    #your query is a string