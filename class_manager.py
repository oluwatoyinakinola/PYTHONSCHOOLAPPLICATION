from grading import assign_grade
from database import Database

class ClassManager:
    def __init__(self, max_students_per_class=80, db_file="school_database.db"):
        self.max_students_per_class = max_students_per_class
        self.db = Database(db_file)

    def is_class_full(self, num_students):
        return num_students >= self.max_students_per_class

    def create_new_class(self, class_name):
        self.db.add_class(class_name)

    def assign_student_to_class(self, student_id, class_id):
        # Check if the class is full
        num_students_in_class = self.db.get_num_students_in_class(class_id)
        if self.is_class_full(num_students_in_class):
            print("Class is full. Cannot add more students.")
            return

        # Add student to the class
        self.db.update_student_class(student_id, class_id)

    def remove_student_from_class(self, student_id):
        # Remove student from the class
        self.db.update_student_class(student_id, None)

    def reallocate_student_to_class(self, student_id, new_class_id):
        self.db.update_student_class(student_id, new_class_id)

    def update_student_score(self, student_id, subject, score):
        self.db.update_student_score(student_id, subject, score)

    def calculate_average_score(self, class_id, subject):
        return self.db.get_average_score_in_class(class_id, subject)
