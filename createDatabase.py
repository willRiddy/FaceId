import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='will',
    password='toor',
    database='faceRegistration'
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE faceRegistration") # Creates database
# mycursor.execute("SHOW DATABASES") # Prints database
# [print(x) for x in mycursor]

# create pupils table
# mycursor.execute("CREATE TABLE pupils (pupilID INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), photo VARCHAR(255), cameraID INT, time TIME)")
# create camera table
# mycursor.execute("CREATE TABLE cameras (cameraID INT AUTO_INCREMENT PRIMARY KEY, location VARCHAR(255))")
# create timtable table
# mycursor.execute("CREATE TABLE timetable (periodID INT AUTO_INCREMENT PRIMARY KEY, timeStart Time, timeEnd Time)")


#mycursor.execute("ALTER TABLE pupils RENAME COLUMN overide TO override")
mydb.commit()