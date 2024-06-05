import sqlite3
from grading import assign_grade  # Importing assign_grade function

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            # Create students table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )
            """)
            
            # Create classes table with the subject column
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER,
                    subject TEXT,
                    score INTEGER,
                    student_id INTEGER,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            """)
            
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating tables:", e)

    def add_student(self, name, class_ids_subjects):
        try:
            # Add a new student to the database
            self.cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
            student_id = self.cursor.lastrowid

            self.conn.commit()
            print("Student Added Successfully")
            
            # Ensure each student is registered in at least 8 subjects
            if len(class_ids_subjects) < 8:
                raise ValueError("Each student must be registered in a minimum of 8 subjects.")
            
            for class_id, subject in class_ids_subjects:
                self.cursor.execute("INSERT INTO classes (class_id, subject, student_id) VALUES (?, ?, ?)",
                                    (class_id, subject, student_id))

            self.conn.commit()
            print("Student Added to Classes Successfully")
        except sqlite3.Error as e:
            print("Error adding student:", e)
        except ValueError as ve:
            print(ve)

    def update_student_class(self, student_id, class_id):
        try:
            # Update the class ID of the specified student in the classes table
            self.cursor.execute("UPDATE classes SET class_id=? WHERE student_id=?", (class_id, student_id))
            self.conn.commit()
            print("Student Updated Successfully")
        except sqlite3.Error as e:
            print("Error updating student class:", e)

    def update_student_score(self, student_id, subject, score):
        try:
            # Update the score of the specified student for a specific subject
            self.cursor.execute("""
                UPDATE classes
                SET score=?
                WHERE student_id=? AND subject=?
            """, (score, student_id, subject))
            self.conn.commit()
            print("Score Updated Successfully")
        except sqlite3.Error as e:
            print("Error updating student score:", e)

    def get_scores_in_class(self, class_id, subject):
        try:
            # Retrieve scores of all students in the specified class for the specified subject
            self.cursor.execute("SELECT score FROM classes WHERE class_id=? AND subject=?", (class_id, subject))
            scores = [row[0] for row in self.cursor.fetchall()]
            return scores
        except sqlite3.Error as e:
            print("Error retrieving scores:", e)
            return []

    def get_average_score_in_class(self, class_id, subject):
        try:
            scores = self.get_scores_in_class(class_id, subject)
            if scores:
                average_score = sum(scores) / len(scores)
                return average_score
            else:
                return None
        except sqlite3.Error as e:
            print("Error calculating average score:", e)
            return None

    def delete_student(self, student_id):
        try:
            # Delete a student from the database by ID
            self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            self.cursor.execute("DELETE FROM classes WHERE student_id=?", (student_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error deleting student:", e)

    def get_num_students_in_class(self, class_id):
        try:
            # Retrieve the number of students in the specified class from the classes table
            self.cursor.execute("SELECT COUNT(*) FROM classes WHERE class_id=?", (class_id,))
            num_students = self.cursor.fetchone()[0]
            return num_students
        except sqlite3.Error as e:
            print("Error retrieving number of students in class:", e)
            return None

    def close_connection(self):
        try:
            # Close database connection
            self.conn.close()
        except sqlite3.Error as e:
            print("Error closing connection:", e)
