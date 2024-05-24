import mysql.connector

# create a class for populating mysql values
class mysql_connector:

    # initializing the host, user, password and database
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = self.init_mysql_conn()

    # initialize database_connection
    def init_mysql_conn(self):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            print("successfully_connected")
            self.db = mydb
            return mydb.cursor()
        except:
            print("error occured in setting connection with database")

    # create the table in the given database
    def create_table(self, table_name, col_dtype_dict: dict):

        values = ""

        values += "("
        for key in col_dtype_dict:
            values += str(key)
            values += " "
            values += str(col_dtype_dict[key])
            values += ","
        values = values[0 : len(values) - 1]
        values += ")"

        sql = "create table if not exists " + table_name + values + ";"

        self.cursor.execute(sql)

    # insert table given table_name,values type is list
    def insert(self, table_name, values: tuple):

        sql = "INSERT INTO " + table_name + " VALUEs " + str(values)

        self.cursor.execute(sql)

        self.db.commit()

    # fetch all values given a databse,tuple of values
    def fetchall(self, table_name):

        self.cursor.execute("select * from " + table_name)

        results = self.cursor.fetchall()

        for values in results:
            print(values)

    def validate_password(self, email, pwd):
        # function to validate the password given by the user
        # input is email and password
        self.cursor.execute(
            "SELECT pass_word FROM student WHERE email_id = %s", (email,)
        )
        student = self.cursor.fetchone()

        # Check if the username exists in the teacher table
        self.cursor.execute(
            "SELECT pass_word FROM teacher WHERE email_id = %s", (email,)
        )
        teacher = self.cursor.fetchone()

        if student:
            if student[0] == pwd:
                return "student"
        elif teacher:
            if teacher[0] == pwd:
                return "teacher"
        else:
            return None

    def get_details_student(self, email):
        # function to get details of students for home page of student
        # input is email of the  student
        dic = dict()

        self.cursor.execute(
            f"select st_name, regno, dept, acc_year from student where email_id = '{email}'"
        )

        std_details = self.cursor.fetchone()

        format = ("name", "regno", "dept", "acc_year")

        for i in range(len(std_details)):
            dic[format[i]] = std_details[i]

        print(dic)

        # output is the details in formatt
        # {'st_name': 'Emily Davis', 'regno': 1004, 'dept': 'Civil Engineering', 'acc_year': '2025-2026'}
        return dic

    def completed_course_details(self, email):
        # function to get th student completed course details given email
        # input is the email of the student
        dic = dict()

        self.cursor.execute(
            f"select nm.c_code, c.c_name, c.weeks, nm.verified_marks from course c join nptel_marks nm on nm.c_code = c.c_code where nm.email_id = '{email}'"
        )

        comp_course_details = self.cursor.fetchall()

        format = ("c_code", "c_name", "weeks", "marks")

        for i in range(len(comp_course_details)):
            for j in range(len(format)):
                if i == 0:
                    dic[format[j]] = [comp_course_details[i][j]]
                else:
                    dic[format[j]].append(comp_course_details[i][j])

        print(dic)
        # output is in the formatt
        # {'c_code': ['EE201', 'ME301'], 'c_name': ['Electrical Circuits', 'Mechanical Dynamics'], 'weeks': [10, 14], 'marks': [88, 90]}
        return dic

    def add_course(self, c_code, c_name, weeks, nptel_link, if_yes):
        # function to add the course to the course_table
        # input is the (c_code,c_name,weeks,nptel_link,if_yes)
        # example input 'CHEM501', 'Chemical Kinetics', 8, 'https://nptel.com/chem501', 'Yes'
        # output data is added to db successfully
        self.insert("course", (c_code, c_name, weeks, nptel_link, if_yes))

    def display_c_code(self):
        self.cursor.execute("select c_code from courses")
        data = self.cursor.fetchall()
        return data

    def display_c_name(self):
        self.cursor.execute("select c_name from courses")
        data = self.cursor.fetchall()
        return data

    def display_dept(self):
        self.cursor.execute("select distinct(dept) from student")
        data = self.cursor.fetchall()
        return data

    def display_sem(self):
        self.cursor.execute("select distinct(sem) from student")
        data = self.cursor.fetchall()
        return data

    def register_course(self, email, c_code):
        # code to insert into the registered course for the user
        self.insert("register_course", (email, c_code))

    def upload_marksheet(self, email, c_code, marks, pdf, verified, qr_code):
        # function to upload marksheet of user to data base
        # input is email,c_code,marks,pdf,verified,qr_code
        # no output as it is insert stmt only
        self.insert("certificate", (email, c_code, marks, pdf, verified, qr_code))

    # needs to be changed
    def get_available_course(self, email):
        # function to get the available courses that the user has registered needs to be changes
        # input is email id
        # output in formatt
        self.cursor.execute(
            f"select c.c_code, c.c_name from course c join set_course s on c.c_code = s.c_code where sem = (select sem from student where email_id = '{email}')"
        )
        data = self.cursor.fetchall()
        return data

    # get course details
    def get_course_details(self, lis_c_name):
        # req dic
        dic = dict()
        for c_name in lis_c_name:
            dic.update(self._get_course_details(c_name))
        print(dic)
        return dic

    # get the course details
    def _get_course_details(self, c_name):
        # write sql query to get the course details
        query = f"""select c.c_code,c.c_name,weeks,nptel_link,dept,acc_year from course c join set_course s on c.c_code = s.c_code where c.c_name = '{c_name}'"""
        # executre the query
        self.cursor.execute(query)
        # get all the data
        details = self.cursor.fetchall()
        # set a dictionary
        dic = {}
        # set value as a dictionary of detail_name and detail
        order = ("c_code", "c_name", "weeks", "nptel_link", "dept", "acc_year")
        # loop through data
        for data in details:
            # set the course as key
            key = data[1]
            value = {}
            for index in range(len(data)):
                value[order[index]] = data[index]
            # set the primary key's value as value
            dic[key] = value
        # end
        print(dic)
        return dic

    # get the name sem sub marks from table
    def student_details(self):
        # write query
        query = """select s.st_name, s.sem, c.c_name, ce.marks,ce.verified,s.email_id,c.c_code from student s join certificate ce on ce.email_id = s.email_id join course c on c.c_code = ce.c_code order by s.sem;"""
        # execute query
        self.cursor.execute(query)
        # fetch the query
        details = self.cursor.fetchall()
        # convert to req formatt
        order = ("name", "sem", "c_name", "ce_marks", "verified","email_id","c_code")
        lis = []
        for data in details:
            dic = {}
            for index in range(len(order)):
                dic[order[index]] = data[index]
            print(dic)
            lis.append(dic)
        # return
        print(lis)
        return lis

    # get data from nptel_marks table
    def verified_details(self):
        # query to get student id, name subject_name, score
        query = """
        select n.email_id,s.st_name, c.c_name, n.verified_marks 
        from nptel_marks n
        join student s on s.email_id = n.email_id
        join course c on c.c_code = n.c_code;
        """
        # excetue and fetch the query
        self.cursor.execute(query)
        details = self.cursor.fetchall()
        # convert to req format json
        order = ("email", "name", "subject", "marks")
        lis = []
        for data in details:
            dic = {}
            for index in range(len(order)):
                dic[order[index]] = data[index]
            print(dic)
            lis.append(dic)
        # return
        print(lis)
        return lis

    # admin verification for teacher
    def admin_verifcation_std_list(self):
        # query to get student id, name subject_name, score
        query_std = """
        select s.dig_id,s.st_name,s.sem, s.acc_year,cour.c_name,cert.c_code,cert.verified from student s
        join certificate cert on cert.email_id = s.email_id
        join course cour on cert.c_code = cour.c_code;
        """
        # excetue and fetch the query
        self.cursor.execute(query_std)
        mix_std = self.cursor.fetchall()

        query_dis_year = """
        select distinct(acc_year) from student;
        """
        self.cursor.execute(query_dis_year)
        dist_year = self.cursor.fetchall()

        dict = {}
        for years_tup in dist_year:
            dict[years_tup[0]] = []

        for years_tup in dist_year:
            for records in mix_std:
                if records[3] == years_tup[0]:
                    dict[years_tup[0]].append(records)

        print(dict)
    class Student:
        def get_verified_details(self, email):
            # complete details of verified certificates from user
            query_std = f"""
            select cour.c_name,verified_marks,ssn_marks 
            from nptel_marks n
            join certificate cer on n.email_id = cer.email_id 
            join course cour on cer.c_code = cour.c_code
            where verified = 'ver' and n.email_id = '{email}'
            """
            print(query_std)
            # excetue and fetch the query
            self.cursor.execute(query_std)
            verified_details = self.cursor.fetchall()

            print(verified_details)
            return verified_details

        def get_nverified_details(self, email):
            # complete details of verified certificates from user
            query_std = f"""
            select cour.c_code,cour.c_name,marks 
            from certificate cer 
            join course cour on cer.c_code = cour.c_code
            where verified = 'nver' and cer.email_id ='{email}' 
            """
            print(query_std)
            # excetue and fetch the query
            self.cursor.execute(query_std)
            nverified_details = self.cursor.fetchall()

            print(nverified_details)
            return nverified_details

        def get_rej_details(self, email):
            # complete details of verified certificates from user
            query_std = f"""
            select r.std_email_id,c.c_name,c.c_code,teacher_email_id,issue 
            from rejected r
            join course c on c.c_code = r.c_code
            join teacher t on t.email_id = teacher_email_id
            where std_email_id = '{email}'
            """
            print(query_std)
            # excetue and fetch the query
            self.cursor.execute(query_std)
            rej_details = self.cursor.fetchall()

            print(rej_details)
            return rej_details

    def ins_certificate(self,email_id,c_code,marks,qr_code_link,certificate_link):

        query_ins = f'''
        insert into certificate (email_id, c_code, marks, verified, upload_date, qr_code_url, certificate_link) values ('{email_id}', '{c_code}', {marks}, 'nver', CURRENT_TIMESTAMP,'{qr_code_link}', '{certificate_link}')
        '''
        self.cursor.execute(query_ins)

        self.db.commit()

    def get_file_name(self,email,c_code):
        query_file = f'''
        select certificate_link from certificate where email_id = '{email}' and c_code = '{c_code}'
        '''

        # excetue and fetch the query
        self.cursor.execute(query_file)
        certifcate_link = self.cursor.fetchone()[0]

        return certifcate_link

    def get_ver_details_admin(self,email,c_code):
        query_det = f'''
        select s.regno,cour.c_name,marks,s.email_id from certificate cer
        join student s on s.email_id = cer.email_id
        join course cour on cour.c_code = cer.c_code
        where cer.email_id = '{email}' and cer.c_code = '{c_code}';
        '''
        # excetue and fetch the query
        self.cursor.execute(query_det)
        details = self.cursor.fetchone()

        print(details)
        return details

    def ins_nptel_marks(self,email_id,c_code,marks):
        query_ins = f'''
        insert into nptel_marks (email_id, c_code, verified_marks, verified_date) values ('{email_id}', '{c_code}', {marks}, CURRENT_TIMESTAMP)
        '''
        self.cursor.execute(query_ins)

        self.db.commit()

    def update_cert_correct(self,email_id,c_code):
        query_cor = f'''
        update certificate set verified = 'ver' 
        where email_id = '{email_id}' and c_code = '{c_code}';
        '''
        self.cursor.execute(query_cor)
        self.db.commit()

    def update_cert_wrong(self,email_id,c_code):
        query_cor = f'''
        update certificate set verified = 'rej' 
        where email_id = '{email_id}' and c_code = '{c_code}';
        '''
        self.cursor.execute(query_cor)
        self.db.commit()

    # ADMIN HOME STAT PAGE
    def admin_stat_home(self):
        query_det = f'''
        select count(distinct(email_id)) from certificate;
        '''
        # excetue and fetch the query
        self.cursor.execute(query_det)
        students_enrolled = self.cursor.fetchone()

        query_det = f'''
        select count(distinct(email_id)) from certificate;
        '''
        # excetue and fetch the query
        self.cursor.execute(query_det)
        course_taken = self.cursor.fetchone()

        return students_enrolled,course_taken

    def toppers_table(self):

        semester = [2,4]
        map = {}
        for sem in semester:
            query_det = f'''
            SELECT s.st_name, c.c_code, c.marks
            FROM student s
            JOIN certificate c ON s.email_id = c.email_id
            JOIN set_course sc on sc.c_code = c.c_code
            WHERE sc.sem = {sem} and c.marks = (select max(marks) from certificate where c_code = c.c_code);
            '''
            self.cursor.execute(query_det)
            toppers_table = self.cursor.fetchall()
            map[sem] = toppers_table
        print(map)
        return map

    def course_name(self):

        query_det = f'''
        SELECT DISTINCT(c_name) 
        FROM course c 
        '''
        self.cursor.execute(query_det)
        course_available = self.cursor.fetchall()
        return course_available

    def course_details(self,c_code):

        query_det = f'''
        select c_name,c_code,weeks,nptel_link
        from course where c_code =  '{c_code}';
        '''

        self.cursor.execute(query_det)
        course_details = self.cursor.fetchall()
        print(course_details)
        return course_details

    # statistics db query
    def all_set_course(self):
        print('')
        print('this is the data for all the set courses id 1')
        print('')
        query_det = f'''
        SELECT DISTINCT(c.c_name),c.c_code
        FROM course c;
        '''

        self.cursor.execute(query_det)
        course_details = self.cursor.fetchall()
        print(course_details)
        return course_details

    def get_details_course(self,c_code):
        print('')
        print('This is the data for available courses id 2')
        print('')
        query_det = f'''
        select * from course
        where c_code = '{c_code}';
        '''

        self.cursor.execute(query_det)
        course_details = self.cursor.fetchall()
        print(course_details)
        return course_details

    def tot_avg_max(self,c_code):
        print('')
        print('This is the data for tot average mark id 3')
        print('')
        query_det = f'''
        SELECT COUNT(regno),AVG(verified_marks),MAX(verified_marks) AS total_students
        FROM NPTEL_MARKS
        WHERE c_code = '{c_code}';
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def toppers(self,c_code):
        print('')
        print('This is the data for toppers given sem and course code id 4')
        print('')
        query_det = f'''
        SELECT nm.regno,s.st_name, nm.verified_marks,nm.acc_year, nm.sem_type
        FROM NPTEL_MARKS nm
        join student s on nm.regno = s.regno
        WHERE nm.c_code = '{c_code}' -- Replace 'noc24-cs47' with your desired course code
        ORDER BY nm.verified_marks DESC
        LIMIT 10;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def convert_to_dicts(self,input_list):
        output = [{"year": str(year), "odd_semester": odd, "even_semester": even} for year, even, odd in input_list]
        return output

    def enrollment_graph(self,c_code):
        print('')
        print('This is the data for double line graph chart id 5')
        print('')
        query_det = f'''
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' THEN regno END) AS Even_Sem_Enrollment_Count,
            COUNT(CASE WHEN sem_type = 'odd' THEN regno END) AS Odd_Sem_Enrollment_Count
        FROM 
            NPTEL_MARKS
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        records = self.convert_to_dicts(records)
        print('@@@@@@@')
        print(records)
        return records

    def pie_chart(self,c_code):
        print('')
        print('This is the data for pie chart id 6')
        print('')
        query_det = f'''
        SELECT 
            sem, 
            COUNT(DISTINCT regno) AS num_students_enrolled 
        FROM NPTEL_MARKS 
        WHERE c_code = '{c_code}' 
        GROUP BY sem;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def silver_score_graph(self,c_code):
        print('')
        print('This is the data for slacked bar graph id 7')
        print('')
        query_det = f'''
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' AND verified_marks BETWEEN 50 AND 80 THEN regno END) AS Even_Sem_Marks_Count,
            COUNT(CASE WHEN sem_type = 'odd' AND verified_marks BETWEEN 50 AND 80 THEN regno END) AS Odd_Sem_Marks_Count
        FROM 
            NPTEL_MARKS
            
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def silver_score_graph(self, c_code):
        print("")
        print("This is the data for slacked bar graph id 7")
        print("")
        query_det = f"""
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' AND verified_marks BETWEEN 50 AND 80 THEN regno END) AS Even_Sem_Marks_Count,
            COUNT(CASE WHEN sem_type = 'odd' AND verified_marks BETWEEN 50 AND 80 THEN regno END) AS Odd_Sem_Marks_Count
        FROM 
            NPTEL_MARKS
            
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def gold_score_graph(self,c_code):
        print('')
        print('This is the data for multiple line chart id 8')
        print('')

        query_det = f'''
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' AND verified_marks BETWEEN 80 AND 100 THEN regno END) AS Even_Sem_Marks_Count,
            COUNT(CASE WHEN sem_type = 'odd' AND verified_marks BETWEEN 80 AND 100 THEN regno END) AS Odd_Sem_Marks_Count
        FROM 
            NPTEL_MARKS
            
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def ins_std_table(self,records:list):

        try: 
            query_ins =' '
            for record in records:
                # get the reg no and name and popullate the database
                query_ins += f'''
                        insert into student (regno, st_name) values ('{record[1]}', '{record[2]}');
                        '''
                print(query_ins)
            self.cursor.execute(query_ins)

            self.db.commit()

        except Exception as e:
            # Handle the error, print a message, and optionally rollback the transaction
            print("Error:", e)
            # self.db.rollback()

    def many_std_insert(self,data:list):
        print("student DATTAAAA")
        print(data)
        regno = []
        values = []
        query_det = f'''
        select regno from student;
        '''
        self.cursor.execute(query_det)
        old_course=[course[0] for course in self.cursor.fetchall()]
        print(old_course)
        for record in data:
            if record[1] not in regno:
                regno.append(record[1])
                tup = (record[1],record[2])
                if record[1] not in old_course:
                    values.append(tup)
        insert_st = 'INSERT INTO STUDENT(regno,st_name) values (%s,%s)'
        # print(values)
        for value in values:
            print(value)
            self.cursor.execute(insert_st,value)
        self.db.commit()
        # self.db.close()
        return True

    def many_course_insert(self,data):
        print("DATTAAAA")
        print(data)
        regno = []
        values = []
        query_det = f'''
        select c_code from course;
        '''
        self.cursor.execute(query_det)
        old_course=[course[0] for course in self.cursor.fetchall()]
        print(old_course)
        for record in data:
            # record[4] => code record[5] => c_name
            if record[4] not in regno:
                regno.append(record[4])
                tup = (record[4],record[5])
                if record[4] not in old_course:
                    values.append(tup)
        insert_st = 'INSERT INTO COURSE(c_code,c_name) values (%s,%s)'
        self.cursor.executemany(insert_st,values)
        self.db.commit()
        # self.db.close()
        return True

    def many_nptelmark_ins(self,data,sem,year):
        print("DATTAAAA")
        print(data)
        regno_c_code = []
        values = []
        for record in data:
            print(type(record[1]),type(record[4]),type(record[7]),type(sem),type(year))
            print(record[1],record[4],record[7],sem,year)
            # record[1] => regno record[4] => c_code
            if record[1] not in regno_c_code:
                regno_c_code.append((record[1],record[4]))
                tup = (record[1],record[4],record[7],record[3],year,sem)
                values.append(tup)
        # print(values)
        insert_st = 'INSERT INTO nptel_marks(regno,c_code,verified_marks,sem,acc_year,sem_type) values (%s,%s,%s,%s,%s,%s)'
        for value in values:
            print(value)

            self.cursor.execute(insert_st,value)
        self.db.commit()
        # self.db.close()
        return True

    def facade_insert(self,data,sem,year):
        '''
        inserts the values into student table,course and nptel_marks table
        '''
        a = self.many_std_insert(data.copy())
        if a:
            b = self.many_nptelmark_ins(data.copy(),sem,year)
        if b:
            c = self.many_course_insert(data.copy())
        print(a,b,c)
        return True

    def getUniqueRegnoCountBySemTypeAndYear(self,acc_year,sem_type):
        print('')
        print('This is the data for the unique regno count')
        print('')

        query_det = f'''
        SELECT COUNT(DISTINCT regno) AS unique_regno_count
        FROM NPTEL_MARKS
        WHERE sem_type = '{sem_type}' AND acc_year = '{acc_year}';
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getUniqueCourseCodeCountBySemTypeAndYear(self,acc_year,sem_type):
        print('')
        print('This is the data for the unique course code given year and sem type')
        print('')

        query_det = f'''
        SELECT COUNT(DISTINCT c_code) AS unique_course_code_count
        FROM NPTEL_MARKS
        WHERE sem_type = '{sem_type}' AND acc_year = '{acc_year}';
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getEnrolledCountGroupedByYearAndSemType(self):
        print('')
        print('This is the data for the unique enrolled count given year and sem_type')
        print('')

        query_det = f'''
        SELECT 
            acc_year,
            SUM(CASE WHEN sem_type = 'odd' THEN count ELSE 0 END) AS odd_sem_count,
            SUM(CASE WHEN sem_type  = 'even' THEN count ELSE 0 END) AS even_sem_count
        FROM 
            (SELECT 
                acc_year,
                sem_type,
                COUNT(DISTINCT regno) AS count
            FROM 
                NPTEL_MARKS
            GROUP BY 
                acc_year, 
                sem_type) AS subquery
        GROUP BY 
            acc_year
        ORDER BY 
            acc_year;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getSemesterWiseCountByYearAndSemType(self,acc_year,sem_type):
        print('')
        print('This is the data for unique year given year and sem_type')
        print('')

        query_det = f'''
        SELECT 
            sem,
            COUNT(distinct(regno)) AS count
        FROM 
            NPTEL_MARKS
        WHERE 
            acc_year = '{acc_year}' 
            AND sem_type = '{sem_type}'
        GROUP BY 
            sem
        ORDER BY 
            sem;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getDistinctAcademicYears(self):
        print('')
        print('This is the data for distinct accademic years available')
        print('')

        query_det = f'''
        select distinct(acc_year) from nptel_marks;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getDistinctSemesterTypes(self):
        print('')
        print('This is the data for different sem types available')
        print('')

        query_det = f'''
        select distinct(sem_type) from nptel_marks;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getToppersgivenSemandYear(self,sem,year):
        print('')
        print('This is the data for different toppers')
        print('')
        print(sem,year)
        query_det = f'''
        SELECT 
    nm.regno,
    s.st_name,
    c.c_name,
    nm.verified_marks,
    nm.acc_year,
    nm.sem_type
FROM 
    NPTEL_MARKS nm 
    JOIN student s ON nm.regno = s.regno
    JOIN course c ON c.c_code = nm.c_code
WHERE 
    nm.acc_year = '{year}' -- Specify the desired academic year
    AND nm.sem_type = '{sem}' -- Specify the desired semester type
ORDER BY
    nm.verified_marks desc
LIMIT 5;
        '''

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def enorllemntcountyearwise(self):
        print("")
        print("This is the data for accademic year enrollment")
        print("")
        query_det = f"""
        select acc_year,count(distinct(regno)) from nptel_marks group by acc_year;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        records = [
            {"year": year, "enrollment_count": count}
            for year, count in records
        ]
        print(records)
        return records

    def course_enrollment_count(self):
        print("")
        print("This is the data for accademic year enrollment")
        print("")
        query_det = f"""
        select c_name,count(regno) 
        from nptel_marks nm
        join course c on nm.c_code = c.c_code
        group by nm.c_code 
        order by count(regno) desc;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        records = subject_enrollment_data = [
            {"name": name, "count": count}
            for name, count in records
        ]
        print(records)
        return records


my_db_connect = mysql_connector("localhost", "root", "password", "nptel_management")

# my_db_connect.create_table('sample2',{'name':'TEXT','age':'TEXT'})

# my_db_connect.create_table('sample2',{'dig_id':'NUM','age':'TEXT'})

# my_db_connect.insert('nptel_marks',('emily.d@email.com', 'ME301', 90, 85))

# my_db_connect.fetchall('course')

# print(my_db_connect.validate_password('rahul.sharma@ssn.edu.in','rahulpass123'))

# my_db_connect.get_details_student('rahul.sharma@ssn.edu.in')

# my_db_connect.completed_course_details('emily.d@email.com')

# my_db_connect.add_course('CHEMS501', 'Chemicals Kinetics', 8, 'https://nptel.com/chem501', 'Yes')

# my_db_connect.get_available_course('rahul.sharma@ssn.edu.in')

# my_db_connect.get_course_details(['Database Management Systems','Mechatronics'])

# my_db_connect.student_details()

# my_db_connect.admin_verifcation_std_list()

# my_db_connect.get_verified_details('rahul.sharma@ssn.edu.in')

# my_db_connect.get_nverified_details('rahul.sharma@ssn.edu.in')

# my_db_connect.get_rej_details('rahul.sharma@ssn.edu.in')

# my_db_connect.ins_certificate('rahul.sharma@ssn.edu.in1','CE401',25,'https://example.com/qr_code_4','link1')

# my_db_connect.get_file_name('rahul.sharma@ssn.edu.in','IT101')

# my_db_connect.get_ver_details_admin('rahul.sharma@ssn.edu.in','IT101')

# my_db_connect.update_cert_correct('rahul.sharma@ssn.edu.in','IT101')

# my_db_connect.toppers_table()

# my_db_connect.course_details('Software Testing')

# my_db_connect.all_set_course()
# my_db_connect.get_details_course('noc24-cs47')
# my_db_connect.toppers_table()
# my_db_connect.tot_avg_max('noc24-cs47')
# my_db_connect.toppers('noc24-cs47',4)
# my_db_connect.bar_graph('noc24-cs47')
# my_db_connect.pie_chart('noc24-cs47')
# my_db_connect.slacked_bar('noc24-cs47')
# my_db_connect.mul_line_chart('noc24-cs47')

# my_db_connect.many_std([[1.0, 185002001, 'Aadhithya B.Kailash', 'IV', 'UITOL91', 'Programming in Java', 3.0, 97, 'nan'], [2.0, 185002003, 'Adithya R', 'IV', 'UCSOL73', 'Social Networks', 3.0, 83, 'nan']])

# my_db_connect.getEnrolledCountGroupedByYearAndSemType()
# my_db_connect.getSemesterWiseCountByYearAndSemType('2021-22','odd')
# my_db_connect.getUniqueCourseCodeCountBySemTypeAndYear('2021-22','odd')
# my_db_connect.getUniqueRegnoCountBySemTypeAndYear('2021-22','odd')
# my_db_connect.getDistinctAcademicYears()
# my_db_connect.getDistinctSemesterTypes()

# my_db_connect.getToppersgivenSemandYear('odd','2021-22')

#my_db_connect.enorllemntcountgivenyear()

my_db_connect.course_enrollment_count()
