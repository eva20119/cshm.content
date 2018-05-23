# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.auto import safeWrite
from db.connect.browser.views import SqlObj
import json
import csv
import base64
import qrcode
import datetime
from plone.namedfile.field import NamedBlobImage,NamedBlobFile
from plone import namedfile
from StringIO import StringIO


class CreateNews(BrowserView):
    def __call__(self):
        portal = api.portal.get()
        obj = api.content.create(
            type='Document',
            title='My Content',
            container=portal)


class SatisfactionFirst(BrowserView):
    template = ViewPageTemplateFile('template/satisfaction_first.pt')
    def __call__(self):
        request = self.request
        self.date = request.get('date')
        self.course_name = request.get('course_name')
        self.period = request.get('period')
        self.teacher = request.get('teacher')
        self.subject_name = request.get('subject_name')
        return self.template()


class SatisfactionSec(BrowserView):
    template = ViewPageTemplateFile('template/satisfaction_sec.pt')
    def __call__(self):
        request = self.request
        self.date = request.get('date')
        self.course_name = request.get('course_name')
        self.period = request.get('period')
        self.teacher = request.get('teacher')
        self.subject_name = request.get('subject_name')
        portal = api.portal.get()
        abs_url = portal.absolute_url()
        return self.template()


class ResultSatisfaction(BrowserView):
    def __call__(self):
        request = self.request
        course = request.get('course')
        subject_name = request.get('subject_name')
        is_round = request.get('is_round')
        period = request.get('period')
        date = request.get('date')
        teacher = request.get('teacher')
        seat = request.get('seat')
        question1 = request.get('question1')
        question2 = request.get('question2')
        question3 = request.get('question3')
        question4 = request.get('question4')
        question5 = request.get('question5')
        question6 = request.get('question6')
        question7 = request.get('question7')
        question8 = request.get('question8', 0)
        question9 = request.get('question9', '')
        question10 = request.get('question10', '')
        question11 = request.get('question11', '')
        question12 = request.get('question12', '')

        user = api.user.get_current().getId()
        execSql = SqlObj()

        execStr = """INSERT INTO `satisfaction`(`user`, `course`, `subject`, `period`, `date`, 
            `teacher`, `question1`, `question2`, `question3`, `question4`, `question5`, 
            `question6`, `question7`, `question8`,question9,question10,question11,question12,seat) 
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}','{}','{}')""".format(user, course, subject_name, 
            period, date, teacher, question1, question2, question3, question4, question5, 
            question6, question7, question8, question9, question10, question11, question12, seat)
        execSql.execSql(execStr)

        api.portal.show_message(message='', type='info', request=request)
        return '填寫完成'


class Manager(BrowserView):
    template = ViewPageTemplateFile('template/manager.pt')
    def __call__(self):
        self.course_title = self.request.get('course_title')
        return self.template()


class ResultManager(BrowserView):
    def __call__(self):
        request = self.request
        anw1 = request.get('anw1')
        anw2 = request.get('anw2')
        anw3 = request.get('anw3')
        anw4 = request.get('anw4')
        anw5 = request.get('anw5')
        anw6 = request.get('anw6')
        anw7 = request.get('anw7')
        anw8 = request.get('anw8')
        anw9 = request.get('anw9')
        anw10 = request.get('anw10')
        anw11 = request.get('anw11')
        anw12 = request.get('anw12')
        anw13 = request.get('anw13')
        anw14 = request.get('anw14')
        course_name = request.get('course_name')
        course_period = request.get('course_period')
        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6

        execSql = SqlObj()
        execStr = """INSERT INTO `manager`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, 
            `anw6`, `anw7`, `anw8`, `anw9`, `anw10`, `anw11`, `anw12`, `anw13`, `anw14`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, anw9, anw10, anw11, 
            anw12, anw13, anw14)
        execSql.execSql(execStr)
        api.portal.show_message(message='填寫完成', type='info', request=request)
        request.response.redirect('%s/@@manager?course_title=%s_%s' %(api.portal.get().absolute_url(), course_name, course_period) )


class Stacker(BrowserView):
    template = ViewPageTemplateFile('template/stacker.pt')
    def __call__(self):
        self.course_title = self.request.get('course_title')
        return self.template()


class ResultStacker(BrowserView):
    def __call__(self):
        request = self.request
        anw1 = request.get('anw1')
        anw2 = request.get('anw2')
        anw3 = request.get('anw3')
        anw4 = request.get('anw4')
        anw5 = request.get('anw5')
        anw6 = request.get('anw6')
        anw7 = request.get('anw7')
        anw8 = request.get('anw8')
        anw9 = request.get('anw9')
        course_name = request.get('course_name')
        course_period = request.get('course_period')
        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6
        execSql = SqlObj()
        execStr = """INSERT INTO `stacker`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, `anw6`, 
            `anw7`, `anw8`, `anw9`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}')""".format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, 
            anw9)
        execSql.execSql(execStr)
        api.portal.show_message(message='填寫完成', type='info', request=request)
        request.response.redirect('%s/@@stacker?course_title=%s_%s' %(api.portal.get().absolute_url(), course_name, course_period) )


class Emergency(BrowserView):
    template = ViewPageTemplateFile('template/emergency.pt')
    def __call__(self):
        self.course_title = self.request.get('course_title')
        return self.template()


class ResultEmergency(BrowserView):
    def __call__(self):
        request = self.request
        anw1 = request.get('anw1')
        anw2 = request.get('anw2')
        anw3 = request.get('anw3')
        anw4 = request.get('anw4')
        anw5 = request.get('anw5')
        anw6 = request.get('anw6')
        anw7 = request.get('anw7')
        anw8 = request.get('anw8' ,'')
        anw9 = request.get('anw9')
        anw10 = request.get('anw10')
        course_name = request.get('course_name')
        course_period = request.get('course_period')
        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6
        execSql = SqlObj()
        execStr = """INSERT INTO `emergency`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, `anw6`, 
            `anw7`, `anw8`, `anw9`, `anw10`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}','{}')""".format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, 
            anw9, anw10)
        execSql.execSql(execStr)
        api.portal.show_message(message='填寫完成', type='info', request=request)
        request.response.redirect('%s/@@emergency?course_title=%s_%s' %(api.portal.get().absolute_url(), course_name, course_period) )


class Ctype(BrowserView):
    template = ViewPageTemplateFile('template/c_type.pt')
    def __call__(self):
        self.course_title = self.request.get('course_title')
        return self.template()


class ResultCtype(BrowserView):
    def __call__(self):
        request = self.request
        anw1 = request.get('anw1')
        anw2 = request.get('anw2')
        anw3 = request.get('anw3')
        anw4 = request.get('anw4')
        anw5 = request.get('anw5')
        anw6 = request.get('anw6')
        anw7 = request.get('anw7')
        anw8 = request.get('anw8' ,'')
        anw9 = request.get('anw9')
        course_name = request.get('course_name')
        course_period = request.get('course_period')
        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6
        execSql = SqlObj()
        execStr = """INSERT INTO `c_type`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, `anw6`, 
            `anw7`, `anw8`, `anw9`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}')""".format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, 
            anw9)
        execSql.execSql(execStr)
        api.portal.show_message(message='填寫完成', type='info', request=request)
        request.response.redirect('%s/@@c_type?course_title=%s_%s' %(api.portal.get().absolute_url(), course_name, course_period) )


class FirePrevention(BrowserView):
    template = ViewPageTemplateFile('template/fire_prevention.pt')
    def __call__(self):
        return self.template()


class ResultFirePrevention(BrowserView):
    def __call__(self):
        request = self.request
        course1 = request.get('course1')
        course2 = request.get('course2', '')
        course3 = request.get('course3', '')
        course4 = request.get('course4', '')
        course5 = request.get('course5', '')
        period = request.get('period')
        date1 = request.get('date1')
        date2 = request.get('date2', '')
        select1 = request.get('select1', '')
        anw6_1 = request.get('6_1')
        anw7_1 = request.get('7_1')

        teacher1 = request.get('teacher1')
        teacher2 = request.get('teacher2', '')
        teacher3 = request.get('teacher3', '')
        teacher4 = request.get('teacher4', '')
        teacher5 = request.get('teacher5', '')

        anw1_1 = request.get('1_1', '')
        anw1_2 = request.get('1_2', '')
        anw1_3 = request.get('1_3', '')
        anw1_4 = request.get('1_4', '')
        anw1_5 = request.get('1_5', '')
        anw2_1 = request.get('2_1', '')
        anw2_2 = request.get('2_2', '')
        anw2_3 = request.get('2_3', '')
        anw2_4 = request.get('2_4', '')
        anw2_5 = request.get('2_5', '')
        anw3_1 = request.get('3_1', '')
        anw3_2 = request.get('3_2', '')
        anw3_3 = request.get('3_3', '')
        anw3_4 = request.get('3_4', '')
        anw3_5 = request.get('3_5', '')
        anw4_1 = request.get('4_1', '')
        anw4_2 = request.get('4_2', '')
        anw4_3 = request.get('4_3', '')
        anw4_4 = request.get('4_4', '')
        anw4_5 = request.get('4_5', '')
        anw5_1 = request.get('5_1', '')
        anw5_2 = request.get('5_2', '')
        anw5_3 = request.get('5_3', '')
        anw5_4 = request.get('5_4', '')
        anw5_5 = request.get('5_5', '')

        anw8_1 = request.get('8_1', '')
        anw9_1 = request.get('9_1', '')
        user = api.user.get_current().getId()

        execSql = SqlObj()

        if teacher1 and course1:
            execStr = """INSERT INTO `fire_prevention_set`(`user`, `course`, `period`, `teacher`, 
            `date1`, `date2`, `select1`, `anwA`, `anwB`, `anwC`, `anwD`, `anwE`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user, course1, 
            period, teacher1, date1, date2, select1, anw1_1, anw1_2, anw1_3,anw1_4, anw1_5)
            execSql.execSql(execStr)
        if teacher2 and course2:
            execStr = """INSERT INTO `fire_prevention_set`(`user`, `course`, `period`, `teacher`, 
            `date1`, `date2`, `select1`, `anwA`, `anwB`, `anwC`, `anwD`, `anwE`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user, course2, 
            period, teacher1, date1, date2, select1, anw2_1, anw2_2, anw2_3,anw2_4, anw2_5)
            execSql.execSql(execStr)
        if teacher3 and course3:
            execStr = """INSERT INTO `fire_prevention_set`(`user`, `course`, `period`, `teacher`, 
            `date1`, `date2`, `select1`, `anwA`, `anwB`, `anwC`, `anwD`, `anwE`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user, course3, 
            period, teacher1, date1, date2, select1, anw3_1, anw3_2, anw3_3,anw3_4, anw3_5)
            execSql.execSql(execStr)
        if teacher4 and course4:
            execStr = """INSERT INTO `fire_prevention_set`(`user`, `course`, `period`, `teacher`, 
            `date1`, `date2`, `select1`, `anwA`, `anwB`, `anwC`, `anwD`, `anwE`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user, course4, 
            period, teacher1, date1, date2, select1, anw4_1, anw4_2, anw4_3,anw4_4, anw4_5)
        if teacher5 and course5:
            execStr = """INSERT INTO `fire_prevention_set`(`user`, `course`, `period`, `teacher`, 
            `date1`, `date2`, `select1`, `anwA`, `anwB`, `anwC`, `anwD`, `anwE`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user, course5, 
            period, teacher1, date1, date2, select1, anw5_1, anw5_2, anw5_3,anw5_4, anw5_5)


        execStr = """INSERT INTO `counselor`(`fire_prevention1`, `fire_prevention2`) VALUES ('{}','{}')
            """.format(anw6_1, anw7_1)
        execSql.execSql(execStr)
        api.portal.show_message(message='填寫完成', type='info', request=request)
        request.response.redirect('%s/questionnaire4' %api.portal.get().absolute_url())


class ShowFireStatistics(BrowserView):
    template = ViewPageTemplateFile('template/show_fire_statistics.pt')
    def __call__(self):
        execSql = SqlObj()
        execStr = """SELECT * FROM fire_prevention_set"""
        self.result = execSql.execSql(execStr)
        return self.template()


class CalculateFire(BrowserView):
    template = ViewPageTemplateFile('template/calculate_fire.pt')
    def __call__(self):
        request = self.request
        course = request.get('course')
        period = request.get('period')
        teacher = request.get('teacher')
        select = request.get('select')
        self.period = period
        self.select = select
        if course and period and teacher:
            execStr = """SELECT * FROM fire_prevention_set WHERE course='{}' AND period='{}' 
                AND teacher='{}'""".format(course, period, teacher)
        elif course and period and not teacher:
            execStr = """SELECT * FROM fire_prevention_set WHERE course='{}' AND period='{}' 
                """.format(course, period)
        elif course and teacher and not period:
            execStr = """SELECT * FROM fire_prevention_set WHERE course='{}' AND teacher='{}'
                """.format(course, teacher)
        elif period and teacher and not course:
            execStr = """SELECT * FROM fire_prevention_set WHERE period='{}' AND teacher='{}'
            """.format( period, teacher)
        elif course and not period and not teacher:
            execStr = """SELECT * FROM fire_prevention_set WHERE course='{}' 
                """.format(course)
        elif period and not course and not teacher:
            execStr = """SELECT * FROM fire_prevention_set WHERE period='{}' 
                """.format(period)
        elif teacher and not period and not course:
            execStr = """SELECT * FROM fire_prevention_set WHERE teacher='{}' 
                """.format(teacher)
        if select == '初':
            execStr = "%s AND select1='初'" %execStr
        elif select == '複':
            execStr = "%s AND select1='複'" %execStr
        execSql = SqlObj()
        result = execSql.execSql(execStr)
        if not result:
            return 'error'
        # 抓teacher名單
        execStr = """SELECT DISTINCT(teacher) FROM `fire_prevention_set` WHERE period='{}' 
            """.format(period)
        # 抓course名單
        teachers = execSql.execSql(execStr)
        execStr = """SELECT DISTINCT(course) FROM fire_prevention_set WHERE period='{}'
            """.format(period)
        course = execSql.execSql(execStr)
        course_list = []
        data = {}
        tmp_data = {}
        for item in course:
            tmp = dict(item)
            course_list.append(tmp['course'])
        course_list.sort()
        teacher_list = []
        # 初始化資料,先將data都歸零方便後面判斷teacher是否有這堂課
        for item in teachers:
            tmp = dict(item)
            teacher = tmp['teacher']
            teacher_list.append(teacher)
            data[teacher] = {}
            for course in course_list:
                data[teacher][course] = 0
                tmp_data[teacher] = {}
        for item in result:
            tmp = dict(item)
            date1 = tmp['date1']
            date2 = tmp['date2']
            course = tmp['course']
            period = tmp['period']
            teacher = tmp['teacher']
            select1 = tmp['select1']
            anwA = tmp['anwA']
            anwB = tmp['anwB']
            anwC = tmp['anwC']
            anwD = tmp['anwD']
            anwE = tmp['anwE']
            # 蒐集所有資料到對應的位置
            if tmp_data[teacher].has_key(course):
                tmp_data[teacher][course][0].append(anwA)
                tmp_data[teacher][course][0].append(anwB)
                tmp_data[teacher][course][0].append(anwC)
                tmp_data[teacher][course][0].append(anwD)
                tmp_data[teacher][course][0].append(anwE)
            else:
                tmp_data[teacher][course] = [ [anwA, anwB, anwC, anwD, anwE] ]
        for teacher in teacher_list:
            for k,v in tmp_data[teacher].items():
                count_5 = v[0].count(5)
                count_4 = v[0].count(4)
                count_3 = v[0].count(3)
                count_2 = v[0].count(2)
                count_1 = v[0].count(1)
                weight_5 = count_5 * 5
                weight_4 = count_4 * 4
                weight_3 = count_3 * 3
                weight_2 = count_2 * 2
                weight_1 = count_1 * 1
                # 算完分數後將原本的資料覆蓋過去
                point = round(float(weight_5 + weight_4 + weight_3 + weight_2 + weight_1) / 
                        float(count_5 + count_4 + count_3 + count_2 + count_1), 2)
                tmp_data[teacher][k] = point
        # 將tmp_data和data資料做比對
        for k,v in tmp_data.items():
            for v_key,v_value in v.items():
                data[k][v_key] = v_value
        # data排序
        for k,v in data.items():
            data[k] = sorted(data[k].items())
        self.course_list = course_list
        self.data = data
        return self.template()
            

class SurverView(BrowserView):
    template = ViewPageTemplateFile('template/surver_view.pt')
    def __call__(self):
        request = self.request
        context = self.context
        
        title = context.Title()
        file = context.file
        data = {}
        abs_url = api.portal.get().absolute_url()
        ex_url_data = {}
        for item in csv.reader(file.open()):
            course_name = item[0]
            period = item[1]
            year = item[2]
            month = item[3]
            day = item[4]
            week = item[5]
            time = item[6]
            subject_name = item[7]
            teacher = item[9]

            date = '%s-%s-%s' %(year, month, day)
            satisfaction_url = """{}/satisfaction1?course_name={}&period={}&date={}&teacher={}""".format(abs_url, course_name, period, date, teacher)
            if course_name == '丙種職業安全衛生業務主管':
                ex_url = "%s/surver1" % abs_url
            elif course_name == '荷重再一噸以上之堆高機操作人員':
                ex_url = "%s/surver2" % abs_url
            # 處理訓前網址
            if not ex_url_data.has_key(course_name):
                ex_url_data[course_name] = ex_url

            # 處理資料
            if data.has_key(course_name):
                data[course_name][subject_name] = [
                    period, date, week, time, teacher, satisfaction_url]
            else:
                data[course_name] = {subject_name: [ 
                     period, date, week, time, teacher, satisfaction_url ] }
            # import pdb;pdb.set_trace()
        self.data = data
        self.ex_url_data = ex_url_data
        return self.template()


class UploadCsvView(BrowserView):
    template = ViewPageTemplateFile('template/upload_csv_view.pt')
    def __call__(self):
        return self.template()


class UploadCsv(BrowserView):
    def __call__(self):
        request = self.request
        file_data = request.get('file_data')
        file_data = file_data.split(',')[1]
        text = base64.b64decode(file_data)
        f = StringIO(text)
        reader = csv.DictReader(f, delimiter=',')
        create_data = {}
        exist_data = {}
        course_list = {}
        portal = api.portal.get()
        result = api.content.find(context=portal, portal_type='Course')
        # 蒐集現有Course的名子及uid,方便後面比對
        for item in result:
            title = item.Title
            uid = item.UID
            course_list[title] = uid
        for item in reader:
            try:
                if item:
                    # 課程名稱 + '_' + 期間
                    course = '%s_%s' %(item['course'], item['period'])
                    date = '%s/%s/%s' %(item['year'], item['month'], item['date'])
                    data = '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(item['quiz'], date, item['time'],
                                item['week'], item['subject'], item['hour'], item['teacher'], item['number'], item['classroom'])
                    execStr = """INSERT INTO `course_list`(`course`, `period`, `date`, `time`, `week`, `subject`, `hour`, 
                        `teacher`, `number`, `classroom`, `quiz`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}')
                        """.format(item['course'], item['period'], date, item['time'], item['week'], item['subject'],
                              item['hour'], item['teacher'], item['number'], item['classroom'], item['quiz'])
                    execSql = SqlObj()
                    execSql.execSql(execStr)
                    if course in course_list.keys():
                        course_uid = course_list[course]
                        if exist_data.has_key(course_uid):
                            exist_data[course_uid] += data
                        else:
                            exist_data[course_uid] = data
                    else:
                        if create_data.has_key(course):
                            create_data[course] += data
                        else:
                            create_data[course] = data
            except Exception as e:
                print e
        # 更新
        for k,v in exist_data.items():
            api.content.get(UID=k).subject_list = v
        # 建立新的
        for k,v in create_data.items():
            obj = api.content.create(
                type='Course',
                title=k,
                subject_list=v,
                container=portal)
        api.portal.show_message(message='上傳成功!!!', type='info', request=request)
        request.response.redirect('%s/folder_contents' %portal.absolute_url())


class CourseView(BrowserView):
    template = ViewPageTemplateFile('template/course_view.pt')
    def __call__(self):
        context = self.context
        subject_list = context.subject_list
        data = []
        abs_url = api.portal.get().absolute_url()
        course_name = context.title.split('_')[0]
        period = context.title.split('_')[1]
        # effective_date = context.effective_date
        today = datetime.date.today()
        # if today > effective_date:
        #     return '填寫時間以過'
        for item in subject_list.split('\n'):
            if item:
                tmp = item.split(',')
                data.append( [ tmp[1], tmp[2] , tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8]])
        url = """{}/check_surver?course_name={}&period={}""".format(abs_url, course_name, period)
        # 製作qrcode
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.make_image().save('url.png')
        img = open('url.png', 'rb')
        b64_img = base64.b64encode(img.read())
        self.b64_img = b64_img
        self.data = data
        return self.template()


class CheckSurver(BrowserView):
    def __call__(self):
        request = self.request
        course_name = request.get('course_name')
        period = request.get('period')
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M')
        already_write = request.cookie.get('already_write')

        execSql = SqlObj()
        execStr = """SELECT * FROM course_list WHERE course_name = '{}' AND period = '{}' AND date <= '{}'
            """.format(course_name, period, date)
        result = execSql.execSql(execStr)

        for item in result:
            tmp = dict(item)




class ShowStatistics(BrowserView):
    template = ViewPageTemplateFile('template/show_statistics.pt')
    def __call__(self):
        return self.template()


class CalculateSatisfaction(BrowserView):
    template = ViewPageTemplateFile('template/calculate_satisfaction.pt')
    def __call__(self):
        request = self.request
        course = request.get('course')
        period = request.get('period')
        execSql = SqlObj()
        execStr = """SELECT * FROM `satisfaction` WHERE course = '{}' AND period = '{}'
            """.format(course, period)
        result = execSql.execSql(execStr)
        if not result:
            return 'error'
        tmp_data = {}
        anw_set = {}
        anw_set['count_A'] = []
        anw_set['count_B'] = []
        anw_set['count_C'] = []
        anw_set['count_D'] = []
        anw_set['count_E'] = []
        anw_set['count_F'] = []
        option1_data = []
        option2_data = []
        option3_data = []
        option4_data = []

        for item in result:
            tmp = dict(item)
            teacher = tmp['teacher'].strip()
            # question 1,2,3,4,5,8 為基本問題
            # 6,7 為輔導員及場地茶水問題
            # 9,10,11,12 為意見
            anwA = tmp['question1']
            anwB = tmp['question2']
            anwC = tmp['question3']
            anwD = tmp['question4']
            anwE = tmp['question5']
            anwF = tmp['question8']
            # 統計意見
            option1 = tmp['question9']
            option2 = tmp['question10']
            option3 = tmp['question11']
            option4 = tmp['question12']
            option1_data.append(option1)
            option2_data.append(option2)
            option3_data.append(option3)
            option4_data.append(option4)
            # 統計各題的回答
            anw_set['count_A'].append(anwA)
            anw_set['count_B'].append(anwB)
            anw_set['count_C'].append(anwC)
            anw_set['count_D'].append(anwD)
            anw_set['count_E'].append(anwE)
            anw_set['count_F'].append(anwF)
            # 統計老師的評分狀況
            if tmp_data.has_key(teacher):
                tmp_data[teacher].append(anwA)
                tmp_data[teacher].append(anwB)
                tmp_data[teacher].append(anwC)
                tmp_data[teacher].append(anwD)
                tmp_data[teacher].append(anwE)
                tmp_data[teacher].append(anwF)
            else:
                tmp_data[teacher] = [anwA, anwB, anwC, anwD, anwE, anwF]
        self.option1_data = option1_data
        self.option2_data = option2_data
        self.option3_data = option3_data
        self.option4_data = option4_data
        count_data = {}
        tmp_teacher_point = 0
        each_teacher_data = {}
        for k,v in tmp_data.items():
            count_5 = v.count(5)
            count_4 = v.count(4)
            count_3 = v.count(3)
            count_2 = v.count(2)
            count_1 = v.count(1)
            weight_5 = count_5 * 5
            weight_4 = count_4 * 4
            weight_3 = count_3 * 3
            weight_2 = count_2 * 2
            weight_1 = count_1 * 1
            point = round((float(weight_5) + float(weight_4) + float(weight_3) + float(weight_2) + float(weight_1)) / (float(count_5) + float(count_4) + float(count_3) + float(count_2) + float(count_1)),2)
            # 講師平均權值，加權分數再pt算
            count_data[k] = point
            # 總講師權值分數
            tmp_teacher_point += point * 20
            # 圓餅圖要顯示每個老師的個別資料
            each_teacher_data[k] = [count_5, count_4, count_3, count_2, count_1]
        self.each_teacher_data = json.dumps(each_teacher_data)
        self.count_data = count_data
        # 總講師權值分數
        self.point_teacher = round(float(tmp_teacher_point) / float(len(count_data)),2)

        tmp_space = [0, 0, 0, 0, 0]
        tmp_envir = [0, 0, 0, 0, 0]
        for item in result:
            tmp = dict(item)
            space = tmp['question6']
            environment = tmp['question7']
            if space == 5:
                tmp_space[0] += 1

            elif space == 4:
                tmp_space[1] += 1

            elif space == 3:
                tmp_space[2] += 1

            elif space == 2:
                tmp_space[3] += 1

            elif space == 1:
                tmp_space[4] += 1

            if environment == 5:
                tmp_envir[0] += 1

            elif environment == 4:
                tmp_envir[1] += 1

            elif environment == 3:
                tmp_envir[2] += 1

            elif environment == 2:
                tmp_envir[3] += 1

            elif environment == 1:
                tmp_envir[4] += 1
        # 計算環境分數
        origin_space = tmp_space[0] + tmp_space[1] + tmp_space[2] + tmp_space[3] + tmp_space[4] 
        weight_space = tmp_space[0] * 5 + tmp_space[1] * 4 + tmp_space[2] * 3 + tmp_space[3] * 2 + tmp_space[4] * 1
        self.point_space = round(float(weight_space) / float(origin_space) * 20, 2)

        origin_envir = tmp_envir[0] + tmp_envir[1] + tmp_envir[2] + tmp_envir[3] + tmp_envir[4] 
        weight_envir = tmp_envir[0] * 5 + tmp_envir[1] * 4 + tmp_envir[2] * 3 + tmp_envir[3] * 2 + tmp_envir[4] * 1
        self.point_envir = round(float(weight_envir) / float(origin_envir) * 20, 2)

        self.point_total = round((float(self.point_space * 10) + float(self.point_envir * 20) + float(self.point_teacher * 70)) / 100,2) 
        # 圓餅圖的資料整理
        execStr = """SELECT COUNT(DISTINCT(teacher)) as teacher_numbers FROM satisfaction"""
        result = execSql.execSql(execStr)
        teacher_numbers = dict(result[0])['teacher_numbers']
        anw_data = {}
        anw_5 = 0
        anw_4 = 0
        anw_3 = 0
        anw_2 = 0
        anw_1 = 0
        for k,v in anw_set.items():
            # 全部問題的元餅圖資料
            for item in v:
                if item == 5:
                    anw_5 += 1
                elif item == 4:
                    anw_4 += 1
                elif item == 3:
                    anw_3 += 1
                elif item == 2:
                    anw_2 += 1
                elif item == 1:
                    anw_1 += 1
            total_anw = [anw_5, anw_4, anw_3, anw_2, anw_1]
            # 單問題的圓餅圖資料
            anw_A = float(v.count(5)) / float(teacher_numbers)
            anw_B = float(v.count(4)) / float(teacher_numbers)
            anw_C = float(v.count(3)) / float(teacher_numbers)
            anw_D = float(v.count(2)) / float(teacher_numbers)
            anw_E = float(v.count(1)) / float(teacher_numbers)
            anw_data[k] = [anw_A, anw_B, anw_C, anw_D, anw_E]
        self.anw_data = anw_data
        self.total_anw = total_anw
        self.period = period
        self.course = course
        return self.template()


class CalculateTraining(BrowserView):
    template_manager = ViewPageTemplateFile('template/show_manager_statistics.pt')
    template_stacker = ViewPageTemplateFile('template/show_stacker_statistics.pt')
    template_ctype = ViewPageTemplateFile('template/show_ctype_statistics.pt')
    template_emergency = ViewPageTemplateFile('template/show_emergency_statistics.pt')
    def __call__(self):
        request = self.request
        course = request.get('course')
        period = request.get('period')
        execSql = SqlObj()
        if course == '職業安全衛生管理員':
            data = {
                '2': {},
                '3': {},
                '4': {},
                '5': {},
                '6': {},
                '7': {},
                '8': {},
                '9': {},
                '10': {},
                '11': {},
                '12': {},
                '13': {},
                '14': {},
            }
            execStr = """SELECT * FROM manager"""
            result = execSql.execSql(execStr)
            if not result:
                return 'error'
            for item in result:
                tmp = dict(item)
                if data['2'].has_key(tmp['anw2']):
                    data['2'][tmp['anw2']] += 1
                else:
                    data['2'][tmp['anw2']] = 1

                if data['3'].has_key(tmp['anw3']):
                    data['3'][tmp['anw3']] += 1
                else:
                    data['3'][tmp['anw3']] = 1

                if data['4'].has_key(tmp['anw4']):
                    data['4'][tmp['anw4']] += 1
                else:
                    data['4'][tmp['anw4']] = 1

                if data['5'].has_key(tmp['anw5']):
                    data['5'][tmp['anw5']] += 1
                else:
                    data['5'][tmp['anw5']] = 1
                # 複選
                for split_anw6 in tmp['anw6'].split(','):
                    if split_anw6:
                        if data['6'].has_key(split_anw6):
                            data['6'][split_anw6] += 1
                        else:
                            data['6'][split_anw6] = 1

                if data['7'].has_key(tmp['anw7']):
                    data['7'][tmp['anw7']] += 1
                else:
                    data['7'][tmp['anw7']] = 1

                if data['8'].has_key(tmp['anw8']):
                    data['8'][tmp['anw8']] += 1
                else:
                    data['8'][tmp['anw8']] = 1

                if data['9'].has_key(tmp['anw9']):
                    data['9'][tmp['anw9']] += 1
                else:
                    data['9'][tmp['anw9']] = 1

                if data['10'].has_key(tmp['anw10']):
                    data['10'][tmp['anw10']] += 1
                else:
                    data['10'][tmp['anw10']] = 1

                if data['11'].has_key(tmp['anw11']):
                    data['11'][tmp['anw11']] += 1
                else:
                    data['11'][tmp['anw11']] = 1

                if data['12'].has_key(tmp['anw12']):
                    data['12'][tmp['anw12']] += 1
                else:
                    data['12'][tmp['anw12']] = 1

                if data['13'].has_key(tmp['anw13']):
                    data['13'][tmp['anw13']] += 1
                else:
                    data['13'][tmp['anw13']] = 1

                if data['14'].has_key(tmp['anw14']):
                    data['14'][tmp['anw14']] += 1
                else:
                    data['14'][tmp['anw14']] = 1
            json_data = json.dumps(data)
            self.json_data = json_data
            self.result = result
            return self.template_manager()
        
        elif course == '荷重再一噸以上之堆高機操作人員':
            execStr = """SELECT * FROM stacker"""
            result = execSql.execSql(execStr)
            data = {
                    '2': {},
                    '3': {},
                    '4': {},
                    '5': {},
                    '6': {},
                    '7': {},
                    '8': {},
                    '9': {},
                }
            if not result:
                return 'error'
            for item in result:
                tmp = dict(item)
                if data['2'].has_key(tmp['anw2']):
                    data['2'][tmp['anw2']] += 1
                else:
                    data['2'][tmp['anw2']] = 1

                if data['3'].has_key(tmp['anw3']):
                    data['3'][tmp['anw3']] += 1
                else:
                    data['3'][tmp['anw3']] = 1

                if data['4'].has_key(tmp['anw4']):
                    data['4'][tmp['anw4']] += 1
                else:
                    data['4'][tmp['anw4']] = 1

                if data['5'].has_key(tmp['anw5']):
                    data['5'][tmp['anw5']] += 1
                else:
                    data['5'][tmp['anw5']] = 1

                # 複選
                for split_anw6 in tmp['anw6'].split(','):
                    if split_anw6:
                        if data['6'].has_key(split_anw6):
                            data['6'][split_anw6] += 1
                        else:
                            data['6'][split_anw6] = 1

                if data['7'].has_key(tmp['anw7']):
                    data['7'][tmp['anw7']] += 1
                else:
                    data['7'][tmp['anw7']] = 1

                if data['8'].has_key(tmp['anw8']):
                    data['8'][tmp['anw8']] += 1
                else:
                    data['8'][tmp['anw8']] = 1

                if data['9'].has_key(tmp['anw9']):
                    data['9'][tmp['anw9']] += 1
                else:
                    data['9'][tmp['anw9']] = 1

            json_data = json.dumps(data)
            self.json_data = json_data
            return self.template_stacker()

        elif course == '丙種職業安全衛生業務主管':
            execStr = """SELECT * FROM c_type"""
            result = execSql.execSql(execStr)
            data = {
                    '2': {},
                    '3': {},
                    '4': {},
                    '5': {},
                    '6': {},
                    '7': {},
                    '8': {},
                    '9': {},
                }
            if not result:
                return 'error'
            for item in result:
                tmp = dict(item)
                if data['2'].has_key(tmp['anw2']):
                    data['2'][tmp['anw2']] += 1
                else:
                    data['2'][tmp['anw2']] = 1

                if data['3'].has_key(tmp['anw3']):
                    data['3'][tmp['anw3']] += 1
                else:
                    data['3'][tmp['anw3']] = 1

                if data['4'].has_key(tmp['anw4']):
                    data['4'][tmp['anw4']] += 1
                else:
                    data['4'][tmp['anw4']] = 1

                if data['5'].has_key(tmp['anw5']):
                    data['5'][tmp['anw5']] += 1
                else:
                    data['5'][tmp['anw5']] = 1

                # 複選
                for split_anw6 in tmp['anw6'].split(','):
                    if split_anw6:
                        if data['6'].has_key(split_anw6):
                            data['6'][split_anw6] += 1
                        else:
                            data['6'][split_anw6] = 1

                if data['7'].has_key(tmp['anw7']):
                    data['7'][tmp['anw7']] += 1
                else:
                    data['7'][tmp['anw7']] = 1

                if data['8'].has_key(tmp['anw8']):
                    data['8'][tmp['anw8']] += 1
                else:
                    data['8'][tmp['anw8']] = 1

                if data['9'].has_key(tmp['anw9']):
                    data['9'][tmp['anw9']] += 1
                else:
                    data['9'][tmp['anw9']] = 1

            json_data = json.dumps(data)
            self.json_data = json_data
            return self.template_ctype()

        elif course == '急救人員':
            execStr = """SELECT * FROM emergency"""
            result = execSql.execSql(execStr)
            data = {
                    '2': {},
                    '3': {},
                    '4': {},
                    '5': {},
                    '6': {},
                    '7': {},
                    '8': {},
                    '9': {},
                    '10': {}
                }
            if not result:
                return 'error'
            for item in result:
                tmp = dict(item)
                if data['2'].has_key(tmp['anw2']):
                    data['2'][tmp['anw2']] += 1
                else:
                    data['2'][tmp['anw2']] = 1

                if data['3'].has_key(tmp['anw3']):
                    data['3'][tmp['anw3']] += 1
                else:
                    data['3'][tmp['anw3']] = 1

                if data['4'].has_key(tmp['anw4']):
                    data['4'][tmp['anw4']] += 1
                else:
                    data['4'][tmp['anw4']] = 1

                if data['5'].has_key(tmp['anw5']):
                    data['5'][tmp['anw5']] += 1
                else:
                    data['5'][tmp['anw5']] = 1

                # 複選
                for split_anw6 in tmp['anw6'].split(','):
                    if split_anw6:
                        if data['6'].has_key(split_anw6):
                            data['6'][split_anw6] += 1
                        else:
                            data['6'][split_anw6] = 1

                if data['7'].has_key(tmp['anw7']):
                    data['7'][tmp['anw7']] += 1
                else:
                    data['7'][tmp['anw7']] = 1

                if data['8'].has_key(tmp['anw8']):
                    data['8'][tmp['anw8']] += 1
                else:
                    data['8'][tmp['anw8']] = 1

                if data['9'].has_key(tmp['anw9']):
                    data['9'][tmp['anw9']] += 1
                else:
                    data['9'][tmp['anw9']] = 1
                if data['10'].has_key(tmp['anw10']):
                    data['10'][tmp['anw10']] += 1
                else:
                    data['10'][tmp['anw10']] = 1
            json_data = json.dumps(data)
            self.json_data = json_data
            return self.template_stacker()

