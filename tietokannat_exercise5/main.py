import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
dictionary = {}
debug = True


def create_table( ):
    # Creates a new table
    # GLobal variables are stored in "dictionary"
    cursor.execute("""CREATE TABLE """+ dictionary["table"]+
                    " ( " + dictionary["values"]+" ); ")


def insert():
    # Inserts values to the table
    # values are determined in global variable " dictionary "
    cursor.execute("""INSERT INTO """ + dictionary["table"] +
     """ VALUES( """ + dictionary["values"] +
     """ ) ; """)


def search():
    # Query to print
    cursor.execute("SELECT * "
                   "FROM  "+dictionary["table"]+
                    dictionary["ehto"]+
                   " ;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
def search_to_return():
    # Query to return
    cursor.execute("SELECT * "
                   "FROM "+dictionary["table"]+
                    dictionary["ehto"]+
                   " ;")
    rows = cursor.fetchall()
    return rows



def add_trigger():
    # Adds a trigger
    # Global values are stored in dictionary
    cursor.execute(dictionary["trigger"])


def create_table_from_values():
    # One function to create whole table
    create_table()
    add_trigger()


def create_random_students():
    # This is to test if a student can have starting year below 2010
    # For Exercise 3 a
    dictionary["values"] = "'001'," \
                           "'Opiskelija Olli'," \
                           "'CS'," \
                           "'2009'"
    insert()
    # This guy messes around with the db, the query should show that the value of starting year has changed to 2010
    dictionary["values"] = "'002'," \
                           "'Lopsikelija  Kolli'," \
                           "'PT'," \
                           "'2011'"
    insert()
    if debug:
        search()


def try_increasing_credits_by_3():
    # This is to test if one can change the credits given by a course how much one wants
    # It should be limited to a change of 2
    # EXercise 3 c
    dictionary["values"] = "'CS-1337'," \
                           "'Paras ohjelmointikurssi ikinä'," \
                           "'5'"
    insert()
    search()
    cursor.execute("UPDATE Courses "
                   "SET credits = 10 "
                   "WHERE code = 'CS-1337'; ")
    search()

def try_replacing_grade_with_smaller():
    # This is to test if grades can be lowered
    # Exercise 3 b
    dictionary["table"] = "Grades"
    dictionary["values"] = "'001','CS-1337','2022-05-31','3'"
    insert()
    search()
    cursor.execute("UPDATE Grades "
                   "SET grade = 1 "
                   "WHERE studentID > 0;")
    search()
    cursor.execute("UPDATE Grades "
                   "SET grade = 5 "
                   "WHERE studentID = 001;")
    search()


def search_for_this_artist(artist: str):
    # In the later part of exercise 5 there is a demand to ask for a way to search for paintings of an artist
    # With no changes after submission, only artist found in textfile.txt will be found

    dictionary["table"] = "Paintings "
    dictionary["ehto"] = "WHERE Paintings.painter = '"+artist+"'\n"
    return search_to_return()


def main():


    #This is to write something to test if stuff works

    dictionary["table"] = "Customers"
    dictionary["values"] = "custNo TEXT PRIMARY KEY, name TEXT, born INTEGER, bonus REAL, address TEXT, email TEXT"
    dictionary["ehto"] = ""

    create_table()
    dictionary["values"] = " '001', 'Matti Meikäläinen' , 1995, 0, 'Jokamiehentie 5' ,'masa.mese@hotmail.com'"
    insert()

    # HERE IS AN EXAMPLE OF HOW
    # READING INSTRUCTIONS IS HARDER THAN WRITING SQLITE
    # EXERCISE 3 DONE ON WRONG LANGUAGE

    dictionary["table"] = "Students"
    dictionary["values"] = " ID INTEGER PRIMARY KEY," \
                           "name TEXT," \
                           "program TEXT," \
                           "year INTEGER " \
                           ""
    dictionary["trigger"] = "CREATE TRIGGER studentyearTrigger2 "\
                            "AFTER INSERT ON Students " \
                            "WHEN NEW.year < 2010 " \
                            "BEGIN" \
                            "   UPDATE Students " \
                            "   SET year = 2010 " \
                            "   WHERE ID = new.ID; " \
                            "END; " \
                            ""
    create_table_from_values()
    if(debug):
        create_random_students() # Exercise 3 a


    dictionary["table"] = "Courses"
    dictionary["values"] = "code TEXT PRIMARY KEY," \
                           "name TEXT," \
                           "credits INTEGER" \
                           ""
    dictionary["trigger"] = "CREATE TRIGGER courseCreditTrigger " \
                            "AFTER UPDATE OF credits ON Courses " \
                            "WHEN NEW.credits > OLD.credits + 2 " \
                            "BEGIN " \
                            "   UPDATE Courses " \
                            "   SET credits = OLD.credits + 2 " \
                            "   WHERE code = new.code; " \
                            "END; " \
                            ""
    create_table_from_values()
    if(debug):
        try_increasing_credits_by_3() # Exercise 3 c

    dictionary["table"] = "Grades"
    dictionary["values"] = "studentID INTEGER, " \
                           "courseCode TEXT, " \
                           "date TEXT," \
                           "grade INTEGER, " \
                           "PRIMARY KEY (studentID, courseCode)" \
                           ""
    dictionary["trigger"] = "CREATE TRIGGER gradeTrigger " \
                            "AFTER UPDATE OF grade ON Grades " \
                            "WHEN NEW.grade < OLD.grade " \
                            "BEGIN " \
                                    "UPDATE Grades " \
                                    "SET grade = old.grade " \
                                    "WHERE studentID = old.studentID AND courseCode = old.courseCode; "\
                            "END; " \
                            ""
    create_table_from_values()
    if(debug):
        try_replacing_grade_with_smaller() # Exercise 3 b


    # THIS CONTAINS EXERCISE nro 4

    dictionary["table"] = "Paintings"
    dictionary["values"] = "name TEXT NOT NULL," \
                           "painter TEXT NOT NULL, " \
                           "year INTEGER check(year < 2030 AND year > 1100), " \
                           "type TEXT check( type IN ('watercolor', 'oil', 'acrylic','pencil', 'graphic', 'other')), " \
                           "insuranceValue REAL check( insuranceValue >= 0 AND insuranceValue < 10000001)  "
    dictionary["trigger"] = ""
    create_table_from_values()
    dictionary["table"] = "Museums"
    dictionary["values"] = "name TEXT PRIMARY KEY," \
                           "streetAddress TEXT, " \
                           "city TEXT NOT NULL," \
                           "webpage TEXT" \
                           ""
    dictionary["trigger"] = "CREATE TRIGGER no_webpage_trigger " \
                            "AFTER INSERT ON Museums " \
                            "WHEN NEW.webpage = '' " \
                            "BEGIN " \
                            "   UPDATE Museums " \
                            "   SET webpage = 'no webpage' " \
                            "   WHERE name = NEW.name ; " \
                            "END; " \
                            ""
    create_table_from_values()

    dictionary["table"] = "Owns"
    dictionary["values"] = "museumName TEXT NOT NULL, " \
                           "paintingName TEXT NOT NULL, " \
                           "painterName TEXT NOT NULL, " \
                           "start TEXT, " \
                           "end TEXT " \
                           ""
    dictionary["trigger"] = "CREATE TRIGGER owns_is_viableTrigger " \
                            "BEFORE INSERT ON Owns " \
                            "WHEN new.paintingName NOT IN (" \
                            "   SELECT name" \
                            "   FROM Paintings" \
                            ") OR new.museumName NOT IN (" \
                            "   SELECT name" \
                            "   FROM Museums) " \
                            "BEGIN" \
                            "   SELECT raise(ignore);" \
                            "END; "

    create_table_from_values()
    dictionary["table"] = "Paintings"
    dictionary["values"] = "'Darrainen night', 'Pemprant', '1969', 'oil','2'"
    dictionary["ehto"] = ""
    insert()
    print("The insurancevalue of wanted Painting added just before is ",end ="")
    print(search_to_return()[-1][-1]) # BECAUSE THERE IS ONLY ONE PAINTING THAT FILLS THE QUERY
    """
    #in case there could be multiple ones
    for painting in search_to_return():
        print( painting[-1] )
    """

    # EXERCISE 5
    # make your program to use the input read from the user (or from a text file)
    # The input must not include the actual INSERT commands to be executed, but the data which should be inserted to the tables.


    file = open(r"textfile.txt",)
    rownumber = 0
    for row in file:
        if( row == "Paintings\n" ):
            dictionary["table"] = "Paintings"
        elif( row == "Museums\n"):
            dictionary["table"] = "Museums"
        elif( row == "Owns\n"):
            dictionary["table"] = "Owns"
        elif(row == "\n"):
            break
        else:
            dictionary["values"] = row
            dictionary["ehto"] = ""
            insert()





    print("Tell me a name of an artist you wish to find paintings from:  ")

    artist_asked_by_user = input()
    #artist_asked_by_user = "Pemprant"
    found_paintings = search_for_this_artist( artist_asked_by_user )
    if(found_paintings == None  ) :
        print("No paintings found")
    else:
        for painting in found_paintings:
            print(painting[0],",", painting[2])

    conn.commit()
    conn.close()


main()

