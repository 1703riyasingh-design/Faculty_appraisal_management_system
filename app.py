from flask import Flask, flash, render_template, request, redirect, session,url_for
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from db import get_connection
from flask import send_file
import os



app = Flask(__name__)
app.secret_key = "appraisal_secret"


from flask import flash

from flask import flash

def generate_acr_pdf(data):

    if not os.path.exists("static/pdfs"):
        os.makedirs("static/pdfs")

    file_path = f"static/pdfs/ACR_{data['faculty_id']}.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("<b>Bhilai Institute of Technology, Durg</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Faculty Name: {data['name']}", styles["Normal"]))
    
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [
        ["Section", "Marks"],
        ["Part A", data.get("teaching_total", 0)],
        ["Part B", data.get("student_total", 0)],
        ["Part C", data.get("research_total", 0)],
        ["Part D", data.get("academic_total", 0)],
        ["Part E", data.get("institution_total", 0)],
        ["Part F (HOD)", data.get("hod_total", 0)],
        ["Total", data.get("total_marks", 0)],
        ["Percentage", str(data.get("percentage", 0)) + " %"],
        ["Overall Appraisal", data.get("appraisal", "")]
    ]

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (1,1), (-1,-1), 'CENTER')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>HOD Remark:</b>", styles["Normal"]))
    elements.append(Paragraph(data.get("hod_remark",""), styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Principal Remark:</b>", styles["Normal"]))
    elements.append(Paragraph(data.get("principal_remark",""), styles["Normal"]))

    doc.build(elements)

    return file_path


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["role"] = user["role"]

            role = user["role"]   

            if role == "faculty":
                return redirect("/faculty")

            elif role == "admin":
                return redirect("/admin")

            elif role == "hod":
                return redirect("/acr-list")

            elif role == "principal":
                return redirect("/acr-list")

            else:
                flash("You are not authorized", "danger")
                return redirect("/")

        flash("Invalid Email or Password", "danger")
        return redirect("/")

    return render_template("login.html")



@app.route("/faculty")
def faculty_dashboard():

    if session.get("role") != "faculty":
        return redirect("/")

    faculty_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # -------------------------
    # SECTION TOTAL CALCULATION
    # -------------------------

    # Section A
    cursor.execute("SELECT IFNULL(SUM(points),0) total FROM section_a_workload WHERE faculty_id=%s", (faculty_id,))
    a1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(total_projects),0) total FROM section_a_projects WHERE faculty_id=%s", (faculty_id,))
    a2 = float(cursor.fetchone()["total"])

    section_a = a1 + a2

    # Section B
    cursor.execute("SELECT IFNULL(SUM(feedback_index),0) total FROM section_b_feedback WHERE faculty_id=%s", (faculty_id,))
    b1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(result_percentage),0) total FROM section_b_result WHERE faculty_id=%s", (faculty_id,))
    b2 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_b_mentoring WHERE faculty_id=%s", (faculty_id,))
    b3 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(total_marks),0) total FROM section_b_records WHERE faculty_id=%s", (faculty_id,))
    b4 = float(cursor.fetchone()["total"])

    section_b = b1 + b2 + b3 + b4

    # Section C
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_publications WHERE faculty_id=%s", (faculty_id,))
    c1 = float(cursor.fetchone()["total"])

    section_c = c1

    # Section D
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_invigilation WHERE faculty_id=%s", (faculty_id,))
    d1 = float(cursor.fetchone()["total"])

    section_d = d1

    # Section E
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_e_books WHERE faculty_id=%s", (faculty_id,))
    e1 = float(cursor.fetchone()["total"])

    section_e = e1

    grand_total = section_a + section_b + section_c + section_d + section_e

    # -------------------------
    # FETCH FINAL ACR STATUS
    # -------------------------

    cursor.execute("""
        SELECT principal_status, final_pdf, percentage
        FROM acr_approval
        WHERE faculty_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (faculty_id,))

    acr_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "faculty_dashboard.html",
        section_a=section_a,
        section_b=section_b,
        section_c=section_c,
        section_d=section_d,
        section_e=section_e,
        grand_total=grand_total,
        acr_data=acr_data
    )



@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/")

    if session.get("role") != "admin":
        flash("Unauthorized Access!", "danger")
        return redirect("/faculty")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all faculty users
    cursor.execute("SELECT id, email FROM users WHERE role='faculty'")
    faculty_list = cursor.fetchall()

    faculty_data = []

    for faculty in faculty_list:
        faculty_id = faculty["id"]

        # Section A
        cursor.execute(
            "SELECT IFNULL(SUM(points),0) total FROM section_a_workload WHERE faculty_id=%s",
            (faculty_id,)
        )
        a = float(cursor.fetchone()["total"])

        cursor.execute(
            "SELECT IFNULL(SUM(total_projects),0) total FROM section_a_projects WHERE faculty_id=%s",
            (faculty_id,)
        )
        a += float(cursor.fetchone()["total"])

        # Section B
        cursor.execute(
            "SELECT IFNULL(SUM(feedback_index),0) total FROM section_b_feedback WHERE faculty_id=%s",
            (faculty_id,)
        )
        b = float(cursor.fetchone()["total"])

        cursor.execute(
            "SELECT IFNULL(SUM(result_percentage),0) total FROM section_b_result WHERE faculty_id=%s",
            (faculty_id,)
        )
        b += float(cursor.fetchone()["total"])

        cursor.execute(
            "SELECT IFNULL(SUM(marks),0) total FROM section_b_mentoring WHERE faculty_id=%s",
            (faculty_id,)
        )
        b += float(cursor.fetchone()["total"])

        cursor.execute(
            "SELECT IFNULL(SUM(total_marks),0) total FROM section_b_records WHERE faculty_id=%s",
            (faculty_id,)
        )
        b += float(cursor.fetchone()["total"])

        # Section C
        cursor.execute(
            "SELECT IFNULL(SUM(marks),0) total FROM section_c_lab_development WHERE faculty_id=%s",
            (faculty_id,)
        )
        c = float(cursor.fetchone()["total"])

        # Section D
        cursor.execute(
            "SELECT IFNULL(SUM(marks),0) total FROM section_d_invigilation WHERE faculty_id=%s",
            (faculty_id,)
        )
        d = float(cursor.fetchone()["total"])

        # Section E
        cursor.execute(
            "SELECT IFNULL(SUM(marks),0) total FROM section_e_swayam WHERE faculty_id=%s",
            (faculty_id,)
        )
        e = float(cursor.fetchone()["total"])

        grand_total = a + b + c + d + e

        # Grade Logic
        if grand_total >= 80:
            grade = "Excellent"
        elif grand_total >= 60:
            grade = "Good"
        elif grand_total >= 40:
            grade = "Average"
        else:
            grade = "Poor"

        faculty_data.append({
            "email": faculty["email"],
            "total": grand_total,
            "grade": grade
        })

    cursor.close()
    conn.close()

    return render_template("admin_dashboard.html", faculty_data=faculty_data)




@app.route("/faculty_profile", methods=["GET", "POST"])
def faculty_profile():

    if "user_id" not in session:
        return redirect("/")

    faculty_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        email = request.form["email"]
        designation = request.form["designation"]
        department = request.form["department"]
        qualification = request.form["qualification"]
        specialization = request.form["specialization"]
        dob = request.form["dob"]
        joining_date = request.form["joining_date"]
        phone = request.form["phone"]

        cursor.execute("""
            INSERT INTO faculty_profile
            (faculty_id, email, designation, department, qualification,
             specialization, dob, joining_date, phone)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            email=%s, designation=%s, department=%s,
            qualification=%s, specialization=%s,
            dob=%s, joining_date=%s, phone=%s
        """, (
            faculty_id, email, designation, department,
            qualification, specialization, dob, joining_date, phone,
            email, designation, department,
            qualification, specialization, dob, joining_date, phone
        ))

        conn.commit()

    cursor.execute("SELECT * FROM faculty_profile WHERE faculty_id=%s", (faculty_id,))
    profile = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("faculty_profile.html", profile=profile)



@app.route("/section-a")
def section_a():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Workload total
    cursor.execute("""
        SELECT IFNULL(SUM(points),0) AS workload_total
        FROM section_a_workload
        WHERE faculty_id = %s
    """, (session["user_id"],))
    workload = cursor.fetchone()["workload_total"]

    if workload > 80:
        workload = 80

    # Projects total
    cursor.execute("""
        SELECT IFNULL(SUM(total_projects),0) AS project_total
        FROM section_a_projects
        WHERE faculty_id = %s
    """, (session["user_id"],))
    projects = cursor.fetchone()["project_total"]

    if projects > 20:
        projects = 20

    section_total = workload + projects

    if section_total > 100:
        section_total = 100

    cursor.close()
    conn.close()

    return render_template(
        "section_a_main.html",
        workload_total=workload,
        project_total=projects,
        section_total=section_total
    )


@app.route("/section-a/workload", methods=["GET", "POST"])
def section_a_workload():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    faculty_id = session["user_id"]

    if request.method == "POST":

        course = request.form.get("course")
        semester = request.form.get("semester_section")
        subject = request.form.get("subject_name")
        subject_type = request.form.get("subject_type")
        scheduled = int(request.form.get("scheduled_classes", 0))
        held = int(request.form.get("held_classes", 0))

        # Attendance Calculation
        if scheduled > 0:
            percentage = (held / scheduled) * 100
        else:
            percentage = 0

        # Base Marks
        if subject_type == "Theory":
            base = 15
        else:
            base = 10

        points = round((percentage / 100) * base)

        if points > base:
            points = base

        # Check current total
        cursor.execute("""
            SELECT IFNULL(SUM(points),0) as total
            FROM section_a_workload
            WHERE faculty_id = %s
        """, (faculty_id,))
        current_total = cursor.fetchone()["total"]

        if current_total + points > 80:
            cursor.close()
            conn.close()
            return render_template(
                "section_a_workload.html",
                error="❌ Maximum 80 marks allowed",
                subjects=[],
                total=current_total
            )

        # Insert
        cursor.execute("""
            INSERT INTO section_a_workload
            (faculty_id, course, semester_section, subject_name,
             subject_type, scheduled_classes, held_classes, points)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            faculty_id, course, semester, subject,
            subject_type, scheduled, held, points
        ))

        conn.commit()

    # Fetch subjects
    cursor.execute("""
        SELECT * FROM section_a_workload
        WHERE faculty_id = %s
    """, (faculty_id,))
    subjects = cursor.fetchall()

    # Calculate total
    cursor.execute("""
        SELECT IFNULL(SUM(points),0) as total
        FROM section_a_workload
        WHERE faculty_id = %s
    """, (faculty_id,))
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template(
        "section_a_workload.html",
        subjects=subjects,
        total=total
    )


@app.route("/delete-workload/<int:id>")
def delete_workload(id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_a_workload
        WHERE id = %s AND faculty_id = %s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-a/workload")


@app.route("/section-a/projects", methods=["GET", "POST"])
def section_a_projects():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)


    faculty_id = session["user_id"]

    if request.method == "POST":

        btech = int(request.form.get("btech", 0))
        mtech = int(request.form.get("mtech", 0))
        mca_mba = int(request.form.get("mca_mba", 0))
        papers = int(request.form.get("papers", 0))

        # Calculation Logic
        total = (
            (btech * 2) +
            (mtech * 4) +
            (mca_mba * 3) +
            (papers * 5)
        )

        # Limit to 20
        if total > 20:
            total = 20

        # Save (Update if already exists)
        cursor.execute("""
            SELECT id FROM section_a_projects
            WHERE faculty_id = %s
        """, (faculty_id,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE section_a_projects
                SET btech=%s, mtech=%s, mca_mba=%s,
                    papers=%s, total_projects=%s
                WHERE faculty_id=%s
            """, (btech, mtech, mca_mba, papers, total, faculty_id))
        else:
            cursor.execute("""
                INSERT INTO section_a_projects
                (faculty_id, btech, mtech, mca_mba, papers, total_projects)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (faculty_id, btech, mtech, mca_mba, papers, total))

        conn.commit()

    # Fetch data
    cursor.execute("""
        SELECT * FROM section_a_projects
        WHERE faculty_id = %s
    """, (faculty_id,))
    data = cursor.fetchone()
    cursor.fetchall()   # force clear remaining result


    total = data["total_projects"] if data else 0

    cursor.close()
    conn.close()

    return render_template(
        "section_a_projects.html",
        data=data,
        total=total
    )
@app.route("/delete-projects")
def delete_projects():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_a_projects
        WHERE faculty_id = %s
    """, (session["user_id"],))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-a/projects")




# ==============================
# SECTION B MAIN
# ==============================

@app.route("/section-b")
def section_b():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    faculty_id = session["user_id"]

    cursor.execute("""
        SELECT IFNULL(SUM(feedback_index),0) as total 
        FROM section_b_feedback 
        WHERE faculty_id=%s
    """, (faculty_id,))
    feedback = float(cursor.fetchone()["total"])

    cursor.execute("""
        SELECT IFNULL(SUM(result_percentage),0) as total 
        FROM section_b_result 
        WHERE faculty_id=%s
    """, (faculty_id,))
    result = float(cursor.fetchone()["total"])

    cursor.execute("""
        SELECT IFNULL(SUM(marks),0) as total 
        FROM section_b_mentoring 
        WHERE faculty_id=%s
    """, (faculty_id,))
    mentoring = float(cursor.fetchone()["total"])

    cursor.execute("""
        SELECT IFNULL(SUM(total_marks),0) as total 
        FROM section_b_records 
        WHERE faculty_id=%s
    """, (faculty_id,))
    records = float(cursor.fetchone()["total"])

    cursor.close()
    conn.close()

    # Apply Caps
    feedback = min(feedback, 20)
    result = min(result, 10)
    mentoring = min(mentoring, 10)
    records = min(records, 50)

    grand_total = feedback + result + mentoring + records


    return render_template(
        "section_b_main.html",
        feedback=feedback,
        result=result,
        mentoring=mentoring,
        records=records,
        grand_total=grand_total
    )


# ==============================
# FEEDBACK MODULE
# ==============================

@app.route("/section-b/feedback", methods=["GET", "POST"])
def section_b_feedback():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        course = request.form["course"]
        semester_section = request.form["semester_section"]
        subject_name = request.form["subject_name"]
        feedback_index = float(request.form["feedback_index"])
        session_type = request.form["session_type"]

        # ✅ Validation (0-20 marks)
        if feedback_index < 0 or feedback_index > 20:
            return "Feedback marks must be between 0 and 20"

        avg_feedback = feedback_index

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_b_feedback
            (faculty_id, course, semester_section, subject_name,
             feedback_index, avg_feedback, session_type)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            course,
            semester_section,
            subject_name,
            feedback_index,
            avg_feedback,
            session_type
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-b")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM section_b_feedback
    WHERE faculty_id=%s
    """, (session["user_id"],))

    feedback_data = cursor.fetchall()

    cursor.close()
    conn.close()

    total_feedback = len(feedback_data)

    return render_template(
    "section_b_feedback.html",
    feedback_data=feedback_data,
    total_feedback=total_feedback
)


@app.route("/delete-feedback", methods=["POST"])
def delete_feedback():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM section_b_feedback WHERE faculty_id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-b")




# ==============================
# RESULT MODULE
# ==============================

@app.route("/section-b/result", methods=["GET", "POST"])
def section_b_result():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        course = request.form["course"]
        semester_section = request.form["semester_section"]
        subject_name = request.form["subject_name"]
        result_percentage = float(request.form["result_percentage"])
        session_type = request.form["session_type"]

        # ✅ Validation (0-40 marks)
        if result_percentage < 0 or result_percentage > 40:
            return "Result marks must be between 0 and 40"

        avg_result = result_percentage

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_b_result
            (faculty_id, course, semester_section, subject_name,
             result_percentage, avg_result, session_type)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            course,
            semester_section,
            subject_name,
            result_percentage,
            avg_result,
            session_type
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-b")

    return render_template("section_b_result.html")

@app.route("/delete-result", methods=["POST"])
def delete_result():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM section_b_result WHERE faculty_id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-b")



# ==============================
# MENTORING MODULE
# ==============================

@app.route("/section-b/mentoring", methods=["GET", "POST"])
def section_b_mentoring():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        mentoring_details = request.form["mentoring_details"]
        marks = int(request.form["marks"])

        # ✅ Validation (0-10 marks)
        if marks < 0 or marks > 10:
            return "Mentoring marks must be between 0 and 10"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_b_mentoring
            (faculty_id, mentoring_details, marks)
            VALUES (%s,%s,%s)
        """, (
            session["user_id"],
            mentoring_details,
            marks
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-b")

    return render_template("section_b_mentoring.html")

@app.route("/delete-mentoring", methods=["POST"])
def delete_mentoring():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM section_b_mentoring WHERE faculty_id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-b")



# ==============================
# RECORDS MODULE
# ==============================

@app.route("/section-b/records", methods=["GET", "POST"])
def section_b_records():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        lesson_plan = 1 if 'lesson_plan' in request.form else 0
        question_bank = 1 if 'question_bank' in request.form else 0
        attendance_register = 1 if 'attendance_register' in request.form else 0
        assignments = 1 if 'assignments' in request.form else 0
        course_notes = 1 if 'course_notes' in request.form else 0
        lab_records = 1 if 'lab_records' in request.form else 0
        lab_manual = 1 if 'lab_manual' in request.form else 0
        pedagogy_initiative = 1 if 'pedagogy_initiative' in request.form else 0
        class_test_copies = 1 if 'class_test_copies' in request.form else 0
        action_taken = 1 if 'action_taken' in request.form else 0

    
        total_marks = (
            lesson_plan + question_bank + attendance_register +
            assignments + course_notes + lab_records + lab_manual +
            pedagogy_initiative + class_test_copies + action_taken
        )

        total_marks = total_marks * 5   # 10 checkboxes × 5 = 50 max
        conn = get_connection()
        cursor = conn.cursor()

        if total_marks > 50:
            total_marks = 50


        cursor.execute("""
            INSERT INTO section_b_records
            (faculty_id, lesson_plan, question_bank, attendance_register,
             assignments, course_notes, lab_records, lab_manual,
             pedagogy_initiative, class_test_copies, action_taken, total_marks)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            lesson_plan,
            question_bank,
            attendance_register,
            assignments,
            course_notes,
            lab_records,
            lab_manual,
            pedagogy_initiative,
            class_test_copies,
            action_taken,
            total_marks
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-b")

    return render_template("section_b_records.html")

@app.route("/delete-records", methods=["POST"])
def delete_records():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM section_b_records WHERE faculty_id=%s",
        (session["user_id"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-b")


@app.route("/section-c")
def section_c():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    faculty_id = session["user_id"]

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_lab_development WHERE faculty_id=%s", (faculty_id,))
    lab = float(cursor.fetchone()["total"] or 0)

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_department_activity WHERE faculty_id=%s", (faculty_id,))
    dept = float(cursor.fetchone()["total"] or 0)

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_fdp WHERE faculty_id=%s", (faculty_id,))
    fdp = float(cursor.fetchone()["total"] or 0)

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_research_guidance WHERE faculty_id=%s", (faculty_id,))
    research = float(cursor.fetchone()["total"] or 0)

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_publications WHERE faculty_id=%s", (faculty_id,))
    publication = float(cursor.fetchone()["total"] or 0)

    cursor.close()
    conn.close()

    # Apply Caps
    lab = min(lab, 15)
    dept = min(dept, 25)
    fdp = min(fdp, 20)
    research = min(research, 15)
    publication = min(publication, 20)

    grand_total = lab + dept + fdp + research + publication


    return render_template(
        "section_c_main.html",
        lab=lab,
        dept=dept,
        fdp=fdp,
        research=research,
        publication=publication,
        grand_total=grand_total
    )

@app.route("/section-c/lab", methods=["GET","POST"])
def section_c_lab():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        initiative = request.form["initiative"]
        marks = int(request.form["marks"])

        if marks < 0 or marks > 15:
            return "Marks must be between 0 and 15"

        cursor.execute("""
            INSERT INTO section_c_lab_development
            (faculty_id, initiative, marks)
            VALUES (%s,%s,%s)
        """, (session["user_id"], initiative, marks))

        conn.commit()

    cursor.execute("""
        SELECT * FROM section_c_lab_development
        WHERE faculty_id=%s
    """, (session["user_id"],))

    lab_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "section_c_lab.html",
        lab_data=lab_data
    )

@app.route("/delete-lab/<int:id>", methods=["POST"])
def delete_lab(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_c_lab_development
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-c/lab")


@app.route("/section-c/department", methods=["GET","POST"])
def section_c_department():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        activity_details = request.form["activity_details"]
        marks = int(request.form["marks"])

        if marks < 0 or marks > 25:
            return "Marks must be between 0 and 25"

        cursor.execute("""
            INSERT INTO section_c_department_activity
            (faculty_id, activity_details, marks)
            VALUES (%s,%s,%s)
        """, (session["user_id"], activity_details, marks))

        conn.commit()

    cursor.execute("""
        SELECT * FROM section_c_department_activity
        WHERE faculty_id=%s
    """, (session["user_id"],))

    dept_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "section_c_department.html",
        dept_data=dept_data
    )
@app.route("/delete-dept/<int:id>", methods=["POST"])
def delete_dept(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_c_department_activity
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-c/department")


@app.route("/section-c/fdp", methods=["GET","POST"])
def section_c_fdp():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        programme_name = request.form["programme_name"]
        duration = request.form["duration"]
        role = request.form["role"]
        institute_name = request.form["institute_name"]
        marks = int(request.form["marks"])

        if marks < 0 or marks > 20:
            return "Marks must be between 0 and 20"

        cursor.execute("""
            INSERT INTO section_c_fdp
            (faculty_id, programme_name, duration, role, institute_name, marks)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (session["user_id"], programme_name, duration, role, institute_name, marks))

        conn.commit()

    cursor.execute("""
        SELECT * FROM section_c_fdp
        WHERE faculty_id=%s
    """, (session["user_id"],))

    fdp_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "section_c_fdp.html",
        fdp_data=fdp_data
    )

@app.route("/delete-fdp/<int:id>", methods=["POST"])
def delete_fdp(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_c_fdp
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-c/fdp")


@app.route("/section-c/research", methods=["GET","POST"])
def section_c_research():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        scholar_name = request.form["scholar_name"]
        registration_date = request.form["registration_date"]
        role = request.form["role"]
        status = request.form["status"]
        award_date = request.form.get("award_date")
        marks = int(request.form["marks"])

        if marks < 0 or marks > 15:
            return "Marks must be between 0 and 15"

        cursor.execute("""
            INSERT INTO section_c_research_guidance
            (faculty_id, scholar_name, registration_date, role, status, award_date, marks)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            scholar_name,
            registration_date,
            role,
            status,
            award_date,
            marks
        ))

        conn.commit()

    # Fetch Data
    cursor.execute("""
        SELECT * FROM section_c_research_guidance
        WHERE faculty_id=%s
    """, (session["user_id"],))

    research_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "section_c_research.html",
        research_data=research_data
    )

@app.route("/delete-research/<int:id>", methods=["POST"])
def delete_research(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_c_research_guidance
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-c/research")


@app.route("/section-c/publication", methods=["GET","POST"])
def section_c_publication():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        title = request.form["title"]
        co_author = request.form["co_author"]
        journal_name = request.form["journal_name"]
        category = request.form["category"]
        volume_issue = request.form["volume_issue"]
        citation_details = request.form["citation_details"]
        marks = int(request.form["marks"])

        if marks < 0 or marks > 20:
            return "Marks must be between 0 and 20"

        cursor.execute("""
            INSERT INTO section_c_publications
            (faculty_id, title, co_author, journal_name, category,
             volume_issue, citation_details, marks)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            title,
            co_author,
            journal_name,
            category,
            volume_issue,
            citation_details,
            marks
        ))

        conn.commit()

    # Fetch Data
    cursor.execute("""
        SELECT * FROM section_c_publications
        WHERE faculty_id=%s
    """, (session["user_id"],))

    publication_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "section_c_publication.html",
        publication_data=publication_data
    )

@app.route("/delete-publication/<int:id>", methods=["POST"])
def delete_publication(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_c_publications
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-c/publication")


@app.route("/section-d")
def section_d():

    if "user_id" not in session:
        return redirect("/")

    faculty_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Invigilation Total
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_invigilation WHERE faculty_id=%s", (faculty_id,))
    invigilation = float(cursor.fetchone()["total"] or 0)
    invigilation = min(invigilation, 10)

    # Answer Sheet Total
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_answer_sheets WHERE faculty_id=%s", (faculty_id,))
    answer = float(cursor.fetchone()["total"] or 0)
    answer = min(answer, 10)

    # Institutional Activity Total
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_institutional_activity WHERE faculty_id=%s", (faculty_id,))
    activity = float(cursor.fetchone()["total"] or 0)
    activity = min(activity, 15)

    cursor.close()
    conn.close()

    grand_total = invigilation + answer + activity
    grand_total = min(grand_total, 35)

    return render_template(
        "section_d_main.html",
        invigilation=invigilation,
        answer=answer,
        activity=activity,
        grand_total=grand_total
    )

@app.route("/section-d/invigilation", methods=["GET","POST"])
def section_d_invigilation():

    if "user_id" not in session:
        return redirect("/")

    faculty_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        odd = int(request.form["odd"])
        even = int(request.form["even"])

        marks = odd + even
        marks = min(marks, 10)

        cursor.execute("""
            INSERT INTO section_d_invigilation
            (faculty_id, odd, even, marks)
            VALUES (%s,%s,%s,%s)
        """, (faculty_id, odd, even, marks))

        conn.commit()
        return redirect("/section-d/invigilation")

    cursor.execute("SELECT * FROM section_d_invigilation WHERE faculty_id=%s", (faculty_id,))
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("section_d_invigilation.html", records=records)

@app.route("/delete-invigilation/<int:id>")
def delete_invigilation(id):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM section_d_invigilation WHERE id=%s AND faculty_id=%s",
                   (id, session["user_id"]))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-d/invigilation")

@app.route("/section-d/answer-sheets", methods=["GET","POST"])
def section_d_answer_sheets():

    if "user_id" not in session:
        return redirect("/")

    faculty_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        odd = int(request.form["odd"])
        even = int(request.form["even"])

        total = odd + even
        marks = total // 20
        marks = min(marks, 10)

        cursor.execute("""
            INSERT INTO section_d_answer_sheets
            (faculty_id, odd, even, marks)
            VALUES (%s,%s,%s,%s)
        """, (faculty_id, odd, even, marks))

        conn.commit()
        return redirect("/section-d/answer-sheets")

    cursor.execute("SELECT * FROM section_d_answer_sheets WHERE faculty_id=%s", (faculty_id,))
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("section_d_answer_sheets.html", records=records)

@app.route("/delete-answer-sheet/<int:id>")
def delete_answer_sheet(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_d_answer_sheets
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-d/answer-sheets")


@app.route("/section-d/activity", methods=["GET","POST"])
def section_d_activity():

    if "user_id" not in session:
        return redirect("/")

    faculty_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        details = request.form["activity_details"]
        marks = int(request.form["marks"])
        marks = min(marks, 15)

        cursor.execute("""
            INSERT INTO section_d_institutional_activity
            (faculty_id, activity_details, marks)
            VALUES (%s,%s,%s)
        """, (faculty_id, details, marks))

        conn.commit()
        return redirect("/section-d/activity")

    cursor.execute("SELECT * FROM section_d_institutional_activity WHERE faculty_id=%s", (faculty_id,))
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("section_d_activity.html", records=records)

@app.route("/delete-activity/<int:id>")
def delete_activity(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM section_d_institutional_activity
        WHERE id=%s AND faculty_id=%s
    """, (id, session["user_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/section-d/activity")



@app.route("/section-e")
def section_e():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    faculty_id = session["user_id"]

    tables = [
        "section_e_swayam",
        "section_e_other",
        "section_e_rd",
        "section_e_books",
        "section_e_consultancy"
    ]

    totals = {}

    for table in tables:
        cursor.execute(f"SELECT IFNULL(SUM(marks),0) total FROM {table} WHERE faculty_id=%s", (faculty_id,))
        totals[table] = float(cursor.fetchone()["total"] or 0)

    cursor.close()
    conn.close()

    grand_total = sum(totals.values())

    return render_template(
        "section_e_main.html",
        swayam=totals["section_e_swayam"],
        other=totals["section_e_other"],
        rd=totals["section_e_rd"],
        books=totals["section_e_books"],
        consultancy=totals["section_e_consultancy"],
        grand_total=grand_total
    )
@app.route("/section-e/swayam", methods=["GET", "POST"])
def section_e_swayam():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        programme = request.form["programme_name"]
        duration = int(request.form["duration_weeks"])
        course = request.form["course_name"]
        fdp = request.form["fdp_flag"]
        category = request.form["certification_category"]

        # 🔥 AUTO MARKS LOGIC
        marks = 0

        if duration >= 8:
            marks += 10
        else:
            marks += 5

        if fdp.lower() == "yes":
            marks += 5

        if category.lower() in ["elite", "gold"]:
            marks += 5

        # Cap at 20
        marks = min(marks, 20)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_e_swayam 
            (faculty_id, programme_name, duration_weeks, course_name, fdp_flag, certification_category, marks)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (session["user_id"], programme, duration, course, fdp, category, marks))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-e")

    return render_template("section_e_swayam.html")

@app.route("/section-e/other", methods=["GET", "POST"])
def section_e_other():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        activity = request.form["activity_details"]

        marks = 5 if activity.strip() != "" else 0

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_e_other 
            (faculty_id, activity_details, marks)
            VALUES (%s,%s,%s)
        """, (session["user_id"], activity, marks))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-e")

    return render_template("section_e_other.html")

@app.route("/section-e/rd", methods=["GET", "POST"])
def section_e_rd():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        title = request.form["title"]
        amount = float(request.form["amount_released"])

        marks = 5 if amount > 0 else 0

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_e_rd 
            (faculty_id, title, amount_released, marks)
            VALUES (%s,%s,%s,%s)
        """, (session["user_id"], title, amount, marks))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-e")

    return render_template("section_e_rd.html")

@app.route("/section-e/books", methods=["GET", "POST"])
def section_e_books():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        title = request.form["title"]

        marks = 5 if title.strip() != "" else 0

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_e_books 
            (faculty_id, title, marks)
            VALUES (%s,%s,%s)
        """, (session["user_id"], title, marks))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-e")

    return render_template("section_e_books.html")

@app.route("/section-e/consultancy", methods=["GET", "POST"])
def section_e_consultancy():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        title = request.form["title"]
        grant = float(request.form["grant_amount"])

        marks = 5 if grant > 0 else 0

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO section_e_consultancy 
            (faculty_id, title, grant_amount, marks)
            VALUES (%s,%s,%s,%s)
        """, (session["user_id"], title, grant, marks))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/section-e")

    return render_template("section_e_consultancy.html")

@app.route("/submit-acr")
def submit_acr():

    if "user_id" not in session:
        return redirect("/")

    faculty_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)


    # ================= SECTION CALCULATION =================

    # Section A
    cursor.execute("SELECT IFNULL(SUM(points),0) total FROM section_a_workload WHERE faculty_id=%s", (faculty_id,))
    a1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(total_projects),0) total FROM section_a_projects WHERE faculty_id=%s", (faculty_id,))
    a2 = float(cursor.fetchone()["total"])
    section_a = a1 + a2

    # Section B
    cursor.execute("SELECT IFNULL(SUM(feedback_index),0) total FROM section_b_feedback WHERE faculty_id=%s", (faculty_id,))
    b1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(result_percentage),0) total FROM section_b_result WHERE faculty_id=%s", (faculty_id,))
    b2 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_b_mentoring WHERE faculty_id=%s", (faculty_id,))
    b3 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(total_marks),0) total FROM section_b_records WHERE faculty_id=%s", (faculty_id,))
    b4 = float(cursor.fetchone()["total"])

    section_b = b1 + b2 + b3 + b4

    # Section C
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_lab_development WHERE faculty_id=%s", (faculty_id,))
    c1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_department_activity WHERE faculty_id=%s", (faculty_id,))
    c2 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_fdp WHERE faculty_id=%s", (faculty_id,))
    c3 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_research_guidance WHERE faculty_id=%s", (faculty_id,))
    c4 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_c_publications WHERE faculty_id=%s", (faculty_id,))
    c5 = float(cursor.fetchone()["total"])

    section_c = c1 + c2 + c3 + c4 + c5

    # Section D
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_invigilation WHERE faculty_id=%s", (faculty_id,))
    d1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_answer_sheets WHERE faculty_id=%s", (faculty_id,))
    d2 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_d_institutional_activity WHERE faculty_id=%s", (faculty_id,))
    d3 = float(cursor.fetchone()["total"])

    section_d = d1 + d2 + d3

    # Section E
    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_e_swayam WHERE faculty_id=%s", (faculty_id,))
    e1 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_e_other WHERE faculty_id=%s", (faculty_id,))
    e2 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_e_rd WHERE faculty_id=%s", (faculty_id,))
    e3 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_e_books WHERE faculty_id=%s", (faculty_id,))
    e4 = float(cursor.fetchone()["total"])

    cursor.execute("SELECT IFNULL(SUM(marks),0) total FROM section_e_consultancy WHERE faculty_id=%s", (faculty_id,))
    e5 = float(cursor.fetchone()["total"])

    section_e = e1 + e2 + e3 + e4 + e5

    # ================= FINAL CALCULATION =================

    grand_total = section_a + section_b + section_c + section_d + section_e
    max_marks = 400
    percentage = round((grand_total / max_marks) * 100, 2)

    if percentage >= 80:
            grade = "Excellent"
    elif percentage >= 60:
            grade = "Good"
    elif percentage >= 40:
            grade = "Average"
    else:
            grade = "Poor"


    # ================= CHECK EXISTING =================

    cursor.execute("SELECT * FROM acr_approval WHERE faculty_id=%s", (faculty_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE acr_approval
            SET total_marks=%s,
                percentage=%s,
                grade=%s
            WHERE faculty_id=%s
        """, (grand_total, percentage, grade, faculty_id))
    else:
        cursor.execute("""
            INSERT INTO acr_approval (faculty_id, total_marks, percentage, grade)
            VALUES (%s,%s,%s,%s)
        """, (faculty_id, grand_total, percentage, grade))

    conn.commit()
    cursor.close()
    conn.close()

    flash("✅ Your ACR application has been submitted successfully!", "success")

    return redirect("/faculty")


@app.route("/acr-list")
def acr_list():

    if "user_id" not in session:
        return redirect("/")

    role = session["role"]   # ✅ IMPORTANT LINE

    if role not in ["admin", "hod", "principal"]:
        return "Unauthorized"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if role == "hod":
        cursor.execute("""
            SELECT a.*, u.name 
            FROM acr_approval a
            JOIN users u ON a.faculty_id = u.id
            WHERE a.hod_status='Pending'
        """)

    elif role == "principal":
        cursor.execute("""
            SELECT a.*, u.name 
            FROM acr_approval a
            JOIN users u ON a.faculty_id = u.id
            WHERE a.hod_status='Approved'
            AND a.principal_status='Pending'
        """)

    elif role == "admin":
        cursor.execute("""
            SELECT a.*, u.name 
            FROM acr_approval a
            JOIN users u ON a.faculty_id = u.id
        """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("acr_list.html", data=data)

@app.route('/acr_requests')
def acr_requests():

    conn = get_connection()
    rows = cursor.fetchall()

    for row in rows:
        total = row['self_marks'] + row['hod_marks'] + row['principal_marks']
        row['total'] = total
        row['percentage'] = round((total / 400) * 100, 2)

    return render_template('acr_requests.html', rows=rows)



@app.route("/acr-update/<int:id>", methods=["POST"])
def acr_update(id):

    if session["role"] != "admin":
        return "Unauthorized"

    status = request.form["status"]
    remark = request.form["remark"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE acr_approval
        SET hod_status=%s, hod_remark=%s
        WHERE id=%s
    """, (status, remark, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/acr-list")


@app.route("/hod_review/<int:id>", methods=["GET", "POST"])
def hod_review(id):

    if session.get("role") != "hod":
        return "Unauthorized"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.*, u.name 
        FROM acr_approval a
        JOIN users u ON a.faculty_id = u.id
        WHERE a.id=%s
    """, (id,))
    
    data = cursor.fetchone()

    if request.method == "POST":

        responsibility = int(request.form["responsibility"])
        punctuality = int(request.form["punctuality"])
        commitment = int(request.form["commitment"])
        teamwork = int(request.form["teamwork"])
        relationship = int(request.form["relationship"])
        hod_remark = request.form["hod_remark"]

        hod_total = responsibility + punctuality + commitment + teamwork + relationship

        cursor.execute("""
            UPDATE acr_approval
            SET responsibility=%s,
                punctuality=%s,
                commitment=%s,
                teamwork=%s,
                relationship=%s,
                hod_total=%s,
                hod_remark=%s,
                hod_status='Approved',
                principal_status='Pending'
            WHERE id=%s
        """, (responsibility, punctuality, commitment,
              teamwork, relationship, hod_total,
              hod_remark, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/acr-list")

    return render_template("acr_hod.html", data=data)



@app.route("/hod-reject/<int:id>", methods=["POST"])
def hod_reject(id):

    if session.get("role") != "hod":
        return "Unauthorized"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE acr_approval
        SET hod_status='Rejected'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/acr-list")



@app.route("/principal_review/<int:id>", methods=["GET", "POST"])
def principal_review(id):

    if session.get("role") != "principal":
        return "Unauthorized"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch data
    cursor.execute("""
        SELECT a.*, u.name
        FROM acr_approval a
        JOIN users u ON a.faculty_id = u.id
        WHERE a.id=%s
    """, (id,))
    data = cursor.fetchone()

    if not data:
        return "Record not found"

    if request.method == "POST":

        compliance = request.form["compliance"]
        appraisal = request.form["appraisal"]
        principal_remark = request.form["principal_remark"]

        faculty_total = data.get("total_marks", 0) or 0
        hod_total = data.get("hod_total", 0) or 0

        final_total = faculty_total + hod_total
        percentage = round((final_total / 400) * 100, 2)

        # Update DB
        cursor.execute("""
            UPDATE acr_approval
            SET compliance=%s,
                appraisal=%s,
                principal_remark=%s,
                total_marks=%s,
                percentage=%s,
                principal_status='Approved'
            WHERE id=%s
        """, (
            compliance,
            appraisal,
            principal_remark,
            final_total,
            percentage,
            id
        ))
        conn.commit()

        # Fetch updated data
        cursor.execute("""
            SELECT a.*, u.name
            FROM acr_approval a
            JOIN users u ON a.faculty_id = u.id
            WHERE a.id=%s
        """, (id,))
        updated_data = cursor.fetchone()

        # Generate PDF
        pdf_path = generate_acr_pdf(updated_data)

        # Save PDF path
        cursor.execute("""
            UPDATE acr_approval
            SET final_pdf=%s
            WHERE id=%s
        """, (pdf_path, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/acr-list")

    cursor.close()
    conn.close()
    return render_template("acr_principal.html", data=data)

@app.route("/principal-reject/<int:id>", methods=["POST"])
def principal_reject(id):

    if session.get("role") != "principal":
        return "Unauthorized"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE acr_approval
        SET principal_status='Rejected'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/acr-list")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)  