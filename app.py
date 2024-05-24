from flask import Flask, render_template, request,jsonify
import pandas as pd
import mysql.connector
import math
import db_class

app = Flask(__name__)

# MySQL database configuration
my_db_connect = db_class.mysql_connector("localhost", "root", "password", "nptel_management")

@app.route('/upload-marks-from-excel')
def upload_marks_from_excel():
    return render_template('upload_excel.html')


# check and correct this function
@app.route('/populate-database-from-excel', methods=['POST'])
def populate_database_from_excel():
    if request.method == 'POST':
        print('inside upload folder')
        print(request.form)
        file = request.files['file']
        sem = request.form['semester']
        year = request.form['year']
        print(type(sem),type(year))

        # Check if the file is of the allowed type
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # Read the Excel file
            df = pd.read_excel(file)
            df_values = df.values
            df_values = df_values[:, :-1].tolist()

            counter = 1
            for values in df_values:
                if math.isnan(values[0]):
                    print('broke',values)
                    break
                else:
                    print(values[0],counter)
                    counter+=1

            df_values = df_values[:counter-1]
            # Insert data into MySQL database
            if True:
                my_db_connect.facade_insert(df_values,sem,year)
                print('succesfullll')
                # If insertion successful, return the inserted data
                inserted_values = df.to_html()
                return render_template('succesful.html')
            else:
                return "Error inserting data into database."
        else:
            return "Unsupported file format. Please upload a .xlsx or .xls file."


@app.route('/succesful-excel')
def succesfulexcel():
    return render_template('succesful.html')


@app.route('/',methods=['GET','POST'])
def yearwise_statistics():
    print(request.method)
    if request.method == "GET":

        # real data
        acc_year = my_db_connect.getDistinctAcademicYears()
        sem_type = my_db_connect.getDistinctSemesterTypes()
        # Sample data for GET request
        yearwise_enrollment_data = my_db_connect.enorllemntcountyearwise()
        subject_enrollment_data = my_db_connect.course_enrollment_count()

        context = {
            'acc_year': acc_year,
            'sem_type': sem_type,
            'yearwise_enrollment_data': yearwise_enrollment_data,
            'subject_enrollment_data': subject_enrollment_data,
            'post_request': False
        }
        print('********')
        print(context)
        print('rendering template')
        return render_template('yearwise_statistics.html', **context)

    elif request.method == "POST":
        print('2222222')
        course_selected = request.form['course_selected']
        sem_selected = request.form['sem_selected']
        print('!!!!!!')
        print(course_selected)
        print(sem_selected)

        # real data
        acc_year = my_db_connect.getDistinctAcademicYears()
        sem_type = my_db_connect.getDistinctSemesterTypes()
        enrollment_count = my_db_connect.getUniqueRegnoCountBySemTypeAndYear(course_selected,sem_selected)
        course_count = my_db_connect.getUniqueCourseCodeCountBySemTypeAndYear(course_selected,sem_selected)
        markshare_50_80 = my_db_connect.getEnrolledCountGroupedByYearAndSemType()
        sem_enrollment = my_db_connect.getSemesterWiseCountByYearAndSemType(course_selected,sem_selected)
        toppers_data = my_db_connect.getToppersgivenSemandYear(sem_selected,course_selected)
        print('ofvotr',toppers_data)
        context = {
            'selected_year':course_selected,
            'selected_sem':sem_selected,
            'acc_year': acc_year,
            'sem_type': sem_type,
            'enrollment_count': enrollment_count,
            'course_count': course_count,
            'markshare_50_80': markshare_50_80,
            'sem_enrollment': sem_enrollment,
            'toppers_data': toppers_data
        }
        return render_template('yearwise_statistics.html', **context,post_request=True)


# ask maam if this code is required else remove this
@app.route('/course_details', methods=['GET', 'POST'])
def course_stats_final():
    if request.method == "GET":
        course = 'UITOL91'
        set_courses = my_db_connect.all_set_course()
        score_count = my_db_connect.tot_avg_max(course)[0]  # Example: (Total Students, Average Marks, Maximum Marks)
        enrollment_graph = my_db_connect.enrollment_graph(course)  # Example: (Year, Enrollment Count)
        sem_enrollment = my_db_connect.pie_chart(course)  # Example: (Semester, Enrollment Count)
        markshare_50_80 = my_db_connect.silver_score_graph(course) # Example: (Course, 0-50%, 50-80%, 80-100%)
        markshare_80_100 = my_db_connect.gold_score_graph(course)  # Example: (Year, Semester, Average Marks)
        toppers_data = my_db_connect.toppers(course)
        print('available_courses,score_count,enrollment_graph,sem_enrollment,markshare,markshare_80_100,toppers_data')
        print(set_courses,score_count,enrollment_graph,sem_enrollment,markshare_50_80,markshare_80_100,toppers_data)
        return render_template('course_stats_final.html', set_courses=set_courses, available_courses=set_courses,
                            score_count=score_count, enrollment_graph=enrollment_graph, sem_enrollment=sem_enrollment,
                            markshare_50_80=markshare_50_80, markshare_80_100=markshare_80_100,
                                toppers_data=toppers_data,post_request=False)
    elif request.method == "POST":
        course = request.form['course']
        print('!!!!!!')
        print(course)
        set_courses = my_db_connect.all_set_course()
        score_count = my_db_connect.tot_avg_max(course)[0]  # Example: (Total Students, Average Marks, Maximum Marks)
        enrollment_graph = my_db_connect.enrollment_graph(course)  # Example: (Year, Enrollment Count)
        sem_enrollment = my_db_connect.pie_chart(course)  # Example: (Semester, Enrollment Count)
        markshare_50_80 = my_db_connect.silver_score_graph(course) # Example: (Course, 0-50%, 50-80%, 80-100%)
        markshare_80_100 = my_db_connect.gold_score_graph(course)  # Example: (Year, Semester, Average Marks)
        toppers_data = my_db_connect.toppers(course)
        course_data = my_db_connect.course_details(course)[0]
        print('available_courses,score_count,enrollment_graph,sem_enrollment,markshare,markshare_80_100,toppers_data')
        print(set_courses,score_count,enrollment_graph,sem_enrollment,markshare_50_80,markshare_80_100,toppers_data,course_data)

        context = {
            'course_data': course_data,
            'set_courses': set_courses,
            'available_courses': set_courses,
            'score_count': score_count,
            'enrollment_graph': enrollment_graph,
            'sem_enrollment': sem_enrollment,
            'markshare_50_80': markshare_50_80,
            'markshare_80_100': markshare_80_100,
            'toppers_data': toppers_data,
            'course': course,
            'post_request': True
        }
        return render_template('course_stats_final.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
