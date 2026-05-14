import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    cursor.execute('CREATE TABLE semester (semester_id INTEGER, semester TEXT, year INTEGER)')
    cursor.execute('CREATE TABLE course (course_id INTEGER, name TEXT, department TEXT, number TEXT, credits TEXT, advisory_requirement TEXT, enforced_requirement TEXT, description TEXT, num_semesters INTEGER, num_enrolled INTEGER, has_discussion TEXT, has_lab TEXT, has_projects TEXT, has_exams TEXT, has_final_project TEXT, has_final_exam TEXT, has_midterm TEXT)')
    cursor.execute('CREATE TABLE instructor (instructor_id INTEGER, name TEXT, uniqname TEXT)')
    cursor.execute('CREATE TABLE course_offering (offering_id INTEGER, course_id INTEGER, semester INTEGER, section_number INTEGER, start_time TIME, end_time TIME, monday TEXT, tuesday TEXT, wednesday TEXT, thursday TEXT, friday TEXT, saturday TEXT, sunday TEXT, has_final_project TEXT, has_final_exam TEXT, textbook TEXT, class_address TEXT, allow_audit TEXT)')
    cursor.execute('CREATE TABLE offering_instructor (offering_instructor_id INTEGER, offering_id INTEGER, instructor_id INTEGER)')
    cursor.execute('CREATE TABLE student (student_id INTEGER, lastname TEXT, firstname TEXT, program_id INTEGER, declare_major TEXT, total_credit INTEGER, total_gpa REAL, entered_as TEXT, admit_term INTEGER, predicted_graduation_semester INTEGER, degree TEXT, minor TEXT, internship TEXT)')
    cursor.execute('CREATE TABLE program (program_id INTEGER, name TEXT, college TEXT, introduction TEXT)')
    cursor.execute('CREATE TABLE gsi (course_offering_id INTEGER, student_id INTEGER)')
    cursor.execute('CREATE TABLE area (course_id INTEGER, area TEXT)')
    cursor.execute('CREATE TABLE requirement (requirement_id INTEGER, requirement TEXT, college TEXT)')
    cursor.execute('CREATE TABLE comment_instructor (instructor_id INTEGER, student_id INTEGER, score INTEGER, comment_text TEXT)')
    cursor.execute('CREATE TABLE program_requirement (program_id INTEGER, category TEXT, min_credit INTEGER, additional_req TEXT)')
    cursor.execute('CREATE TABLE course_prerequisite (pre_course_id INTEGER, course_id INTEGER)')
    cursor.execute('CREATE TABLE course_tags_count (course_id INTEGER, clear_grading INTEGER, pop_quiz INTEGER, group_projects INTEGER, inspirational INTEGER, long_lectures INTEGER, extra_credit INTEGER, few_tests INTEGER, good_feedback INTEGER, tough_tests INTEGER, heavy_papers INTEGER, cares_for_students INTEGER, heavy_assignments INTEGER, respected INTEGER, participation INTEGER, heavy_reading INTEGER, tough_grader INTEGER, hilarious INTEGER, would_take_again INTEGER, good_lecture INTEGER, no_skip INTEGER)')
    cursor.execute('CREATE TABLE jobs (job_id INTEGER, job_title TEXT, description TEXT, requirement TEXT, city TEXT, state TEXT, country TEXT, zip INTEGER)')
    cursor.execute('CREATE TABLE program_course (program_id INTEGER, course_id INTEGER, workload INTEGER, category TEXT)')
    cursor.execute('CREATE TABLE student_record (student_id INTEGER, course_id INTEGER, semester INTEGER, grade TEXT, how TEXT, transfer_source TEXT, earn_credit TEXT, repeat_term TEXT, test_id TEXT)')
    cursor.execute('CREATE TABLE ta (campus_job_id INTEGER, student_id INTEGER, location TEXT)')
    

    cursor.executemany('INSERT INTO semester VALUES (?, ?, ?)', [(1, 'Fall', 2005)])
    cursor.executemany('INSERT INTO course VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      [(995, 'CMBIOL 995', 'CMBIOL', '995', '3', '', '', 'Advanced Biology', 1, 10, 'N', 'N', 'Y', 'Y', 'Y', 'Y', 'Y')])
    cursor.executemany('INSERT INTO instructor VALUES (?, ?, ?)', [(1, 'Prof Smith', 'psmith'), (2, 'Prof Jones', 'pjones')])
    cursor.executemany('INSERT INTO course_offering VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      [(1, 995, 1, 1, '10:00', '11:30', 'Y', 'N', 'Y', 'N', 'Y', 'N', 'N', 'Y', 'Y', 'Book1', 'Room 101', 'N')])
    cursor.executemany('INSERT INTO offering_instructor VALUES (?, ?, ?)', [(1, 1, 1), (2, 1, 2)])
    cursor.executemany('INSERT INTO program VALUES (?, ?, ?, ?)', [(1, 'Biology', 'LSA', 'Biology program')])
    cursor.executemany('INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      [(1, 'Doe', 'John', 1, 'Biology', 120, 3.5, 'Freshman', 1, 8, 'BS', 'Chemistry', 'Y')])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Courses: {cursor.execute('SELECT COUNT(*) FROM course').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
