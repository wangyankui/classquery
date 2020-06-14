import sqlite3
import datetime

db_path = 'classroom.sqlite'
conn = sqlite3.connect(db_path,check_same_thread = False)
sql_create = '''
    CREATE TABLE IF NOT EXISTS classroom (
      num TEXT NOT NULL UNIQUE,
      state INTEGER NOT NULL,
      loc TEXT,
      size INTEGER,
      electronic INTEGER,
      manyMedia INTEGER,
      wifi INTEGER,
      airConditioner INTEGER
    )
    '''
# 用 execute 执行一条 sql 语句
conn.execute(sql_create)
sql_create = '''
        CREATE TABLE IF NOT EXISTS course (
          num TEXT NOT NULL UNIQUE,
          name TEXT,
          time INTEGER,
          classroom TEXT
        )
        '''
# 用 execute 执行一条 sql 语句
conn.execute(sql_create)
sql_create = '''
          CREATE TABLE IF NOT EXISTS user (
            name TEXT NOT NULL UNIQUE,
            password TEXT,
            type TEXT,
            id INTEGER
          )
          '''
# 用 execute 执行一条 sql 语句
conn.execute(sql_create)
sql_create = '''
             CREATE TABLE IF NOT EXISTS yuyue (
               username TEXT,
               classroom TEXT,
               time INTEGER,
               num INTEGER
             )
             '''
# 用 execute 执行一条 sql 语句
conn.execute(sql_create)
# yuyue(conn, 'YF101', 'wangjin')
# login(conn, 17301017, 'wangjin123')
# query(conn, 'YF101')
# yuyue(conn, 'YF101', 17301017, '4', '5')
# change_state(conn, 17301017, 'YF102', 'size', 80)
# qxyy(conn, 17301017,'YF101', 4, 1)
#tuijian(conn, 'YF', 85, 4, 1, 1, 1)
def columns(table_name):
    if table_name == 'classroom':
        return ['num', 'state', 'loc', 'size', 'electronic', 'manyMedia', 'wifi', 'airConditioner']
    elif table_name == 'course':
        return['num', 'name', 'time', 'classroom']
    elif table_name == 'user':
        return['name', 'password', 'type', 'id']
    elif table_name == 'yuyue':
        return['userid', 'classroom', 'time', 'num']
    else:
        print("表名不对")
        return 0


def insert(conn, table_name, value):
    cols = columns(table_name)
    if cols != 0:
        sql_insert = "INSERT INTO " + table_name + "("
        for c in cols:
            sql_insert = sql_insert + c + ","
        sql_insert = sql_insert[:-1]
        sql_insert = sql_insert + ") VALUES ("
        for v in value:
            sql_insert = sql_insert + v + ","
        sql_insert = sql_insert[:-1]
        sql_insert = sql_insert + ");"
        print(sql_insert)
        conn.execute(sql_insert)
        conn.commit()


def delete(conn, table_name, where):
    sql_delete = "DELETE FROM " + table_name + " WHERE " + where + ";"
    conn.execute(sql_delete)
    conn.commit()
    print(sql_delete)


def update(conn, table_name, set, where):
    sql_update = "UPDATE " + table_name + " SET " + set
    if where != "":
        sql_update = sql_update + " WHERE " + where
    sql_update = sql_update + ";"
    conn.execute(sql_update)
    conn.commit()
    #print(sql_update)


def select(conn, table_name, where):
    cols = columns(table_name)
    if cols != 0:
        sql_select = "SELECT * FROM " + table_name
        if where != "":
            sql_select = sql_select + " WHERE " + where
        sql_select = sql_select + ";"
        print(sql_select)
        curs = conn.execute(sql_select)
        return list(curs)


def timeToInt(week, hour):
    if hour >= 8 and hour < 10:
        t = 1
    elif hour >= 10 and hour < 12:
        t = 2
    elif hour >= 14 and hour < 16:
        t = 3
    elif hour >= 16 and hour < 18:
        t = 4
    elif hour >= 19 and hour < 21:
        t = 5
    else:
        t = 0
    if t == 0:
        return 0
    else:
        t += week * 5
        return t


def issyouke(conn, classroom, week, hour):
    t = timeToInt(week, hour)
    if t != 0:
        where = 'classroom = \'' + classroom + '\' and time = ' + str(t)
        table_name = 'course'
        l2 = select(conn, table_name, where)
        if len(l2) != 0:
            return l2
        else:
            return 0
    else:
        return 0


def login(conn, uid, password):
    where = 'id = \'' + str(uid) + '\' and password = \'' + password + '\''
    table_name = 'user'
    l1 = select(conn, table_name, where)
    if len(l1) == 0:
        #print('账号或密码错误')
        return 0
    else:
        #print('登录成功')
        return 1


def zhuce(conn, type, id, name, password):
    table_name = 'user'
    where = 'id = ' + str(id)
    l = select(conn, table_name, where)
    if len(l) == 0:
        username = '\''+ name + '\''
        uid = '\'' + str(id) + '\''
        word = '\'' + password + '\''
        type = '\'' + type + '\''
        value = [username, word, type, uid]
        insert(conn, table_name, value)
        return 1
    else:
        return 0


def occupied(conn, roomNum):
    now = datetime.datetime.now()
    week = now.weekday()
    hour = now.hour
    t = timeToInt(week, hour)
    where = 'classroom = \'' + roomNum + '\' and time = ' + str(t)
    table_name = 'yuyue'
    zy = select(conn, table_name, where)
    where = 'num = \'' + roomNum + '\''
    table_name = 'classroom'
    l1 = select(conn, table_name, where)
    if len(zy) >= 1:
        i = 0
        sum = 0
        while i < len(zy):
            sum += zy[i][3]
            i += 1
        if sum >= l1[0][3]:
            return 2
        else:
            return 1
    else:
        return 0


def query(conn, roomNum):
    querydict={}
    where = 'num = \'' + roomNum + '\''
    table_name = 'classroom'
    l1 = select(conn, table_name, where)
    #print('教室号码：' + l1[0][0] + '\n')
    querydict['教室号码']=l1[0][0]
    if (occupied(conn, roomNum) == 2) | (l1[0][1] == 1):
        #print('教室状态：已满')
        querydict['教室状态']="已满"
    elif occupied(conn, roomNum) == 1:
        #print('教室状态：部分占用')
        querydict['教室状态'] = "部分占用"
    else:
        now = datetime.datetime.now()
        week = now.weekday()
        hour = now.hour
        if issyouke(conn, roomNum, week, hour) != 0:
            #print('教室状态：正在上课，')
            querydict['教室状态'] = "正在上课"
            c = issyouke(conn, roomNum, week, hour)
            #print('课程号：' + str(c[0][0]))
            #querydict[''] = "已满"
            #print('课程名：' + c[0][1])
        else:
            #print('教室状态：空闲')
            querydict['教室状态'] = "空闲"
    #print('\n')
    #print('教室容量：' + str(l1[0][3]) + '\n')
    querydict['教室容量'] = str(l1[0][3])
    #print('电源插座数量：' + str(l1[0][4]) + '\n')
    querydict['电源插座数量'] = str(l1[0][4])
    if l1[0][5] == 1:
        #print('多媒体设备：有' + '\n')
        querydict['多媒体设备'] = "有"
    else:
        #print('多媒体设备：无' + '\n')
        querydict['多媒体设备'] = "无"
    if l1[0][6] == 1:
        #print('无线网络：有' + '\n')
        querydict['无线网络'] = "有"
    else:
        #print('无线网络：无' + '\n')
        querydict['无线网络'] = "无"
    if l1[0][7] == 1:
        #print('空调：有' + '\n')
        querydict['空调'] = "有"
    else:
       # print('空调：无' + '\n')
        querydict['空调'] = "无"
    return querydict

#1-正在上课，2-空位不足，3-成功，4-被占用，5-无此教室
def yuyue(conn, roomNum, user, time, num):
    where = 'num = \'' + roomNum + '\''
    table_name = 'classroom'
    l1 = select(conn, table_name, where)
    if len(l1) != 0:
        if (l1[0][1] == 0) & (occupied(conn, roomNum) <= 1):
            now = datetime.datetime.now()
            week = now.weekday()
            hour = now.hour
            t = timeToInt(week, hour)
            if issyouke(conn, roomNum, week, hour) != 0:
                #print('预约失败，此教室正在上课')
                return 1
            else:
                where = 'classroom = \'' + roomNum + '\' and time = ' + str(t)
                table_name = 'yuyue'
                zy = select(conn, table_name, where)
                if len(zy) >= 1:
                    i = 0
                    sum = 0
                    while i < len(zy):
                        sum += zy[i][3]
                        i += 1
                    sum += int(num)
                    if sum > l1[0][3]:
                        #print('预约失败，空位不足')
                        return 2
                    else:
                        #print('预约成功')

                        table_name = 'yuyue'
                        userid = '\'' + str(user) + '\''
                        room = '\'' + roomNum + '\''
                        t = '\'' + time + '\''
                        n = '\'' + num + '\''
                        value = [userid, room, t, n]
                        insert(conn, table_name, value)
                        return 3
                else:
                    #print('预约成功')
                    table_name = 'yuyue'
                    username = '\'' + str(user) + '\''
                    room = '\'' + roomNum + '\''
                    t = '\'' + str(time) + '\''
                    n = '\'' + str(num) + '\''
                    value = [username, room, t, n]
                    insert(conn, table_name, value)
                    return 3
        else:
            #print('预约失败，此教室已被占用')
            return 4
    else:
        #print('预约失败,无此教室')
        return 5


def qxyy(conn, user, classroom, time, num):
    where = 'classroom = \'' + str(classroom) + '\' and userid = \'' + str(user) + '\' and time = \'' + str(time) + '\' and num = \'' + str(num) + '\''
    table_name = 'yuyue'
    delete(conn, table_name, where)


def change_state(conn, userid, roomNum, attribute, value):
    table_name = 'user'
    where = 'id = \'' + str(userid) + '\''
    u = select(conn, table_name, where)
    type = u[0][2]
    if type != 'manager':
        #print('权限不够')
        return 0
    else:
        where = 'num = \'' + roomNum + '\''
        set = attribute + '= \'' + str(value) + '\''
        table_name = 'classroom'
        update(conn, table_name, set, where)
        return 1


def tuijian(conn, loc, size, electronic, manyMedia, wifi, airConditioner):
    table_name = 'classroom'
    where = 'loc = \'' + loc + '\' and size >= \'' + str(size) + '\' and electronic >= \'' + str(electronic) + '\' and manyMedia >= \'' + str(manyMedia) + '\' and wifi >= \'' + str(wifi) + '\' and airConditioner >= \'' + str(airConditioner) + '\''
    l1 = select(conn, table_name, where)

    return l1
