import pymysql
from config import host, user, password, db_name

def create_connection(host, user, password, db_name):
    try:
        connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )    
        print('Conected successfully...')
        print('#' * 20)
    
    except Exception as ex:
        print("Connection refused")
        print(ex)
    return connection




def join_maker(connection, group_id, day_id):

    #cursor = connection.cursor()

    with connection.cursor() as cursor:   
        query = '''
        SELECT 
        lesson.lesson_time, 
        lesson.lesson_name, 
        calendar.week_day_name, 
        student_group.group_name 
        FROM 
        timetable
        INNER JOIN student_group on timetable.group_id = student_group.id
        INNER JOIN calendar on timetable.week_day_id = calendar.week_day
        INNER JOIN lesson on timetable.lesson_id = lesson.id
        WHERE student_group.id = (%s) and calendar.week_day = (%s)'''
    
        cursor.execute(query, (group_id, day_id))
        rows = cursor.fetchall()
    return rows



def check_student(connection, tg_id, group_id, first_name):
    #print('check_student called')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT tg_id FROM `student`")
        results = cursor.fetchall()
        for result in results:
            #print(result)
            if result['tg_id'] == tg_id:
                cursor.execute("SELECT group_id FROM `student` WHERE tg_id = (%s)", (tg_id))
                rows = cursor.fetchall()
                #print(rows)
                #print('coincidence', tg_id)
                return group_id
        else:
            #print('else construction')
            cursor.execute("INSERT INTO `student` (tg_id, group_id, first_name) VALUES (%s, %s, %s)", (tg_id, group_id, first_name,))
            connection.commit()
            #print('inserted, tg_id=', tg_id)
            return group_id
    
    
    


def execute_read_query(connection, query):
     cursor = connection.cursor()

     
     with connection.cursor() as cursor:
         cursor.execute(query)
         result = cursor.fetchall()
     return result
         
             
                


        


                
                
                
    