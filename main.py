import pygame
from ui import UI
from database import Database
from class_manager import ClassManager

pygame.init()

def main():
    try:
        screen = pygame.display.set_mode((800, 600))
    except pygame.error as e:
        print("Unable to set up Pygame display:", e)
        return 

    # Initialize database
    db = Database("school_database.db")
    db.create_tables()

    # Create an instance of the UI class and pass the screen object to its constructor
    ui = UI(screen)

    # Initialize class manager
    class_manager = ClassManager(db_file="school_database.db")

    pygame.display.set_caption("School Management System")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            # Handle key events for creating, adding, and deleting students
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # Create a new student
                    student_name = input("Enter student name: ")
                    class_ids_subjects = []
                    for _ in range(8):  # Minimum 8 subjects
                        class_id = int(input("Enter class ID: "))  # assuming class id is an integer
                        subject = input("Enter subject name: ")
                        class_ids_subjects.append((class_id, subject))
                    db.add_student(student_name, class_ids_subjects)
                  
                elif event.key == pygame.K_a:
                    # Add existing student to a class
                    student_id = int(input("Enter student ID to add: "))  # assuming student ID is an integer
                    class_id = int(input("Enter class ID: "))  # assuming class ID is an integer
                    class_manager.assign_student_to_class(student_id, class_id)
                
                elif event.key == pygame.K_d:
                    # Delete a student
                    student_id = int(input("Enter student ID to delete: "))  # assuming student ID is an integer
                    class_manager.remove_student_from_class(student_id)

                elif event.key == pygame.K_u:
                    # Update student score
                    student_id = int(input("Enter student ID to update score: "))
                    subject = input("Enter subject name: ")
                    score = int(input("Enter new score: "))
                    class_manager.update_student_score(student_id, subject, score)
                
                elif event.key == pygame.K_v:
                    # View average score in a class for a subject
                    class_id = int(input("Enter class ID: "))
                    subject = input("Enter subject name: ")
                    average_score = class_manager.calculate_average_score(class_id, subject)
                    if average_score is not None:
                        print(f"The average score in class {class_id} for {subject} is {average_score:.2f}")
                    else:
                        print(f"No scores available for class {class_id} in {subject}")

        screen.fill((255, 255, 255))  # White background
        ui.update()  # Update the UI
        pygame.display.flip()
        clock.tick(30)

    # Close database connection
    db.close_connection()

    pygame.quit()

if __name__ == "__main__":
    main()
