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
import requests
from email.mime.text import MIMEText
import xlsxwriter
import inspect
import urllib
import smtplib
from email.header import Header


class CreateNews(BrowserView):
    def __call__(self):
        import pdb;pdb.set_trace()

class SatisfactionFirst(BrowserView):
    template = ViewPageTemplateFile('template/satisfaction_first.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        abs_url = portal.absolute_url()
        self.date = request.get('date')
        self.course_name = request.get('course_name')
        self.period = request.get('period')
        self.teacher = request.get('teacher')
        self.subject_name = request.get('subject_name')
        seat_number = request.get('seat_number')
#        cookie_seat_number = request.cookies.get('seat_number', '')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.seat_number = seat_number
#        if cookie_seat_number != seat_number:
#            request.response.setCookie('seat_number', seat_number)

#        already_write = request.cookies.get('already_write', [])
#        if already_write:
#            already_write = json.loads(already_write)
#        else:
#            already_write = []

        ex_url = ''
        ex_data = []
        execSql = SqlObj()
        execStr = """SELECT * FROM course_list WHERE course = '{}' AND period = '{}' AND start_time < '{}' ORDER BY
                start_time DESC """.format(request.get('course_name'), request.get('period'), now_time)
        result = execSql.execSql(execStr)

        execStr = """SELECT course,period,subject FROM `satisfaction` WHERE seat = '{}' AND course = '{}' AND 
            period = '{}'""".format(seat_number, request.get('course_name'), request.get('period'))
        satisfaction_result = execSql.execSql(execStr)
        already_write = []
        for item in satisfaction_result:
            tmp = dict(item)
            course = tmp['course']
            period = tmp['period']
            subject = tmp['subject']
            already_write.append('%s_%s_%s' %(course, period, subject))

        for item in result:
            tmp = dict(item)
            course = tmp['course']
            period = tmp['period']
            subject = tmp['subject']
            item_datetime = tmp['start_time'].strftime('%Y-%m-%d %H:%M:%S')
            teacher = tmp['teacher']
            identify = '%s_%s_%s' %(course, period, subject)
            if identify not in already_write and request.get('subject_name') != subject:
                if item[5] == '是':
                    ex_url = """{}/@@satisfaction_sec?subject_name={}&date={}&teacher={}&course_name={}&period={}&seat_number={}""".format(abs_url, subject, item_datetime, teacher, course, period, seat_number)
                else:
                   ex_url = """{}/@@satisfaction_first?subject_name={}&date={}&teacher={}&course_name={}&period={}&seat_number={}""".format(abs_url, subject, item_datetime, teacher, course, period, seat_number)
                ex_data.append( ['%s %s' %(item_datetime, subject), ex_url] )
        if not ex_data:
            self.ex_data = False
        else:
            self.ex_data = ex_data

        return self.template()


class SatisfactionSec(BrowserView):
    template = ViewPageTemplateFile('template/satisfaction_sec.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        abs_url = portal.absolute_url()
        self.date = request.get('date')
        self.course_name = request.get('course_name')
        self.period = request.get('period')
        self.teacher = request.get('teacher')
        self.subject_name = request.get('subject_name')
        seat_number = request.get('seat_number', '')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#        cookie_seat_number = request.cookies.get('seat_number', '')
        self.seat_number = seat_number
#        if cookie_seat_number != seat_number:
#            request.response.setCookie('seat_number', seat_number)

#        already_write = request.cookies.get('already_write', [])
#        if already_write:
#            already_write = json.loads(already_write)
#        else:
#            already_write = []
        ex_url = ''
        ex_data = []
        execSql = SqlObj()
        execStr = """SELECT * FROM course_list WHERE course = '{}' AND period = '{}' AND start_time < '{}' ORDER BY
                start_time DESC """.format(request.get('course_name'), request.get('period'), now_time)
        result = execSql.execSql(execStr)

        execStr = """SELECT course,period,subject FROM `satisfaction` WHERE seat = '{}' AND course = '{}' AND 
            period = '{}'""".format(seat_number, request.get('course_name'), request.get('period'))
        satisfaction_result = execSql.execSql(execStr)
        already_write = []
        for item in satisfaction_result:
            tmp = dict(item)
            course = tmp['course']
            period = tmp['period']
            subject = tmp['subject']
            already_write.append('%s_%s_%s' %(course, period, subject))

        for item in result:
            tmp = dict(item)
            course = tmp['course']
            period = tmp['period']
            subject = tmp['subject']
            item_datetime = tmp['start_time'].strftime('%Y-%m-%d %H:%M:%S')
            teacher = tmp['teacher']
            identify = '%s_%s_%s' %(course, period, subject)
            if identify not in already_write and request.get('subject_name') != subject:
                if item[5] == '是':
                    ex_url = """{}/@@satisfaction_sec?subject_name={}&date={}&teacher={}&course_name={}&period={}&seat_number={}""".format(abs_url, subject, item_datetime, teacher, course, period, seat_number)
                else:
                   ex_url = """{}/@@satisfaction_first?subject_name={}&date={}&teacher={}&course_name={}&period={}&seat_number={}""".format(abs_url, subject, item_datetime, teacher, course, period, seat_number)
                ex_data.append( ['%s %s' %(item_datetime, subject), ex_url] )
        if not ex_data:
            self.ex_data = False
        else:
            self.ex_data = ex_data

        return self.template()


class ResultSatisfaction(BrowserView):
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        abs_url = portal.absolute_url()
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

        execStr = """SELECT course FROM satisfaction WHERE course = '{}' AND period = '{}' AND seat = '{}' AND subject = '{}'
            """.format(course, period, seat, subject_name)
        if execSql.execSql(execStr):
            api.portal.show_message(message='請勿重複填寫問卷', type='error', request=request)
        else:
            execStr = """INSERT INTO `satisfaction`(`user`, `course`, `subject`, `period`, `date`, 
                `teacher`, `question1`, `question2`, `question3`, `question4`, `question5`, 
                `question6`, `question7`, `question8`,question9,question10,question11,question12,seat) 
                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',
                '{}','{}','{}','{}','{}')""".format(user, course, subject_name, 
                period, date, teacher, question1, question2, question3, question4, question5, 
                question6, question7, question8, question9, question10, question11, question12, seat)
            execSql.execSql(execStr)

        # 寄信通知
            if len(question9) >= 15 or len(question10) >= 15 or len(question11) >= 15 or len(question12) >= 15:
                execStr = """SELECT location FROM course_list WHERE course = '{}' AND period = '{}' AND subject = '{}'
                    """.format(course, period, subject_name)
                location = execSql.execSql(execStr)
                flag = True
                try:
                    location = location[0][0]
                    if location:
                        content = api.content.find(context=portal['contact'][location], portal_type='Document')[0].getObject()
                        email = content.description.split('\r\n')
                        trainingCenter = content.title
                    else:
                        trainingCenter = '台北'
                        email = api.content.find(context=portal['contact']['taipei'], portal_type='Document')[0].getObject().description.split('\r\n')
                except:
                    trainingCenter = '台北'
                    email = api.content.find(context=portal['contact']['taipei'], portal_type='Document')[0].getObject().description.split('\r\n')
                    flag = False

                body_str = """科目:%s<br>課程:%s<br>期數:%s<br>座號:%s<br>講師:%s<br>時間:%s<br>教學中心:%s<br>意見提供:<br>%s<br/>%s<br/>%s<br>%s
                    """ %(course, subject_name, period, seat, teacher, date, trainingCenter, question9, question10, question11, question12)
                if not flag:
                    body_str += '教學中心設定錯誤，請去更改\r教學中心設定錯誤，請去更改'

                mime_text = MIMEText(body_str, 'html', 'utf-8')
                mime_text['Subject'] = Header("%s-%s-%s  意見提供" %(course, period, trainingCenter), 'utf-8')

                smtpObj = smtplib.SMTP('localhost')
                smtpObj.sendmail('henry@mingtak.com.tw', 'yutin@cshm.org.tw', mime_text.as_string())

                for i in email:
                    smtpObj.sendmail('henry@mingtak.com.tw', i, mime_text.as_string())

            api.portal.show_message(message='填寫完成', type='info', request=request)

        request.response.redirect('%s/check_surver?course_name=%s&period=%s&seat_number=%s' %(abs_url, course, period, seat))


class Manager(BrowserView):
    template = ViewPageTemplateFile('template/manager.pt')
    def __call__(self):
        try:
            self.course_title = base64.b64decode(self.request.get('course_title'))
        except:
            self.course_title = self.request.get('course_title')

        self.uid = self.request.get('uid')
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
#        uid = self.context.UID()
        uid = request.get('uid')

        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6

        execSql = SqlObj()
        execStr = """INSERT INTO `manager`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, 
            `anw6`, `anw7`, `anw8`, `anw9`, `anw10`, `anw11`, `anw12`, `anw13`, `anw14`, `uid`) VALUES 
            ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}')
            """.format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, anw9, anw10, anw11, 
            anw12, anw13, anw14, uid)
        execSql.execSql(execStr)
        return '填寫完成'
        api.portal.show_message(message='填寫完成', type='info', request=request)
        course_title = base64.b64encode('%s_%s' %(course_name, course_period))
        request.response.redirect('%s/@@manager?course_title=%s&uid=%s' %(api.portal.get().absolute_url(), course_title, uid) )


class Stacker(BrowserView):
    template = ViewPageTemplateFile('template/stacker.pt')
    def __call__(self):
        try:
            self.course_title = base64.b64decode(self.request.get('course_title'))
        except:
            self.course_title = self.request.get('course_title')
        self.uid = self.request.get('uid')
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
#        uid = self.context.UID()
        uid = request.get('uid')

        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6
        execSql = SqlObj()
        execStr = """INSERT INTO `stacker`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, `anw6`, 
            `anw7`, `anw8`, `anw9`, uid) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}', '{}')""".format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, 
            anw9, uid)
        execSql.execSql(execStr)
        return '填寫完成'
        api.portal.show_message(message='填寫完成', type='info', request=request)
        course_title = base64.b64encode('%s_%s' %(course_name, course_period))
        request.response.redirect('%s/@@stacker?course_title=%s&uid=%s'
                                  %(api.portal.get().absolute_url(), course_title, uid) )


class Emergency(BrowserView):
    template = ViewPageTemplateFile('template/emergency.pt')
    def __call__(self):
        try:
            self.course_title = base64.b64decode(self.request.get('course_title'))
        except:
            self.course_title = self.request.get('course_title')
        self.uid = self.request.get('uid')
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
#        uid = self.context.UID()
        uid = request.get('uid')

        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6
        execSql = SqlObj()
        execStr = """INSERT INTO `emergency`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, `anw6`, 
            `anw7`, `anw8`, `anw9`, `anw10`, uid) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}','{}', '{}')""".format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, 
            anw9, anw10, uid)
        execSql.execSql(execStr)
        return '填寫完成'
        api.portal.show_message(message='填寫完成', type='info', request=request)
        course_title = base64.b64encode('%s_%s' %(course_name, course_period))
        request.response.redirect('%s/@@emergency?course_title=%s&uid=%s' %(api.portal.get().absolute_url(), course_title, uid) )


class Ctype(BrowserView):
    template = ViewPageTemplateFile('template/c_type.pt')
    def __call__(self):
        try:
            self.course_title = base64.b64decode(self.request.get('course_title'))
        except:
            self.course_title = self.request.get('course_title')
        self.uid = self.request.get('uid')
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
#        uid = self.context.UID()
        uid = request.get('uid')

        # 處理複選
        new_anw6= ''
        if type(anw6) == list:
            for item in anw6:
                new_anw6 += '%s,' %item
        elif type(anw6) == str:
            new_anw6 = anw6
        execSql = SqlObj()
        execStr = """INSERT INTO `c_type`(course, period, `user`, `anw2`, `anw3`, `anw4`, `anw5`, `anw6`, 
            `anw7`, `anw8`, `anw9`, uid) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}',
            '{}','{}','{}', '{}')""".format(course_name, course_period, anw1, anw2, anw3, anw4, anw5, new_anw6, anw7, anw8, 
            anw9, uid)
        execSql.execSql(execStr)
        return '填寫完成'
        api.portal.show_message(message='填寫完成', type='info', request=request)
        course_title = base64.b64encode('%s_%s' %(course_name, course_period))
        request.response.redirect('%s/@@c_type?course_title=%s_%s' %(api.portal.get().absolute_url(), course_title, uid) )


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
            elif course_name == '荷重在一公噸以上之堆高機操作人員':
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

    def checkCourseName(self, course):
        courseList = ['test', '職業安全管理師','職業衛生管理師','職業安全衛生管理員','甲種職業安全衛生業務主管','乙種職業安全衛生業務主管','丙種職業安全衛生業務主管','現場安全衛生監督人員','營造業甲種職業安全衛生業務主管','營造業乙種職業安全衛生業務主管','營造業丙種職業安全衛生業務主管','施工安全評估人員','製程安全評估人員','擋土支撐作業主管','模板支撐作業主管','隧道等挖掘作業主管','隧道等襯砌作業主管','施工架組配作業主管','鋼構組配作業主管','露天開挖作業主管','屋頂作業主管','有機溶劑作業主管','鉛作業主管','缺氧作業主管','特定化學物質作業主管','粉塵作業主管','防火管理人初訓','防火管理人複訓','急救人員','危險物品運送人員專業訓練(初訓)','吊升荷重在三公噸以上之固定式起重機操作人員','吊升荷重在三公噸以上之移動式起重機操作人員','甲級鍋爐操作人員','乙級鍋爐操作人員','丙級鍋爐操作人員','第一種壓力容器操作人員','高壓氣體特定設備操作人員','高壓氣體容器操作人員','高壓氣體製造安全主任','高壓氣體供應及消費作業主管','高壓氣體製造安全作業主管','高壓室內作業主管','小型鍋爐操作人員','荷重在一公噸以上之堆高機操作人員','吊升荷重在零點五公噸以上未滿三公噸之固定式起重機操作人員','吊升荷重在零點五公噸以上未滿三公噸之移動式起重機操作人員','使用起重機具從事吊掛作業人員','以乙炔熔接裝置或氣體集合裝置從事金屬之熔接、切斷或加熱作業人員','小型裝載機(小山貓)','一般安全衛生教育訓練','南科一般安全衛生教育訓練','隧道挖掘機考照班','挖掘機操作人員(輔導技能檢定)','乙級檢定考複習班','消防設備師','甲級安全師總複習班','甲級衛生師總複習班','堆高機技術士檢定輔導班','勞工安全衛生管理員輔導考照班','甲級廢棄物處裡技術人員(嘉藥科大專班)','乙級廢棄物處裡技術人員(嘉藥科大專班)','丙級廢棄物處裡技術人員(嘉藥科大專班)','三公噸以上固定式起重機架空式-地上操作輔導考照班','三公噸以上固定式起重機架空式-機上操作輔導考照班','三公噸以上移動式起重機伸臂可伸縮式輔導考照班','固定式起重機操作技術士檢定輔導班','室內空氣品質維護管理專責人員','業務主管結業測驗複習班','公寓大廈事務管理人員訓練','公寓大廈防火避難設施管理人員訓練','公寓大廈設備安全管理人員訓練','營造業工地主任220小時職能訓練','勞工健康服務護理人員','人因性危害評估專業人員','保稅工廠保稅業務人員','火藥爆破作業人員安全衛生訓練','一般高壓氣體類作業主管訓練','職業安全衛生業務主管暨職業安全衛生管理人員在職教育訓練','營造業職業安全衛生業務主管暨職業安全衛生管理人員在職教育訓練','擋土支撐作業主管在職教育訓練','模板支撐作業主管在職教育訓練','施工架組配作業主管在職教育訓練','隧道等挖掘作業主管在職教育訓練','隧道等襯砌作業主管在職教育訓練','有機溶劑作業主管在職教育訓練','鉛作業主管在職教育訓練','粉塵作業主管在職教育訓練','缺氧作業主管在職教育訓練','特定化學物質作業主管在職教育訓練','急救人員在職教育訓練','固定式起重機操作人員在職教育訓練','移動式起重機操作人員在職教育訓練','荷重在一公噸以上之堆高機操作人員在職教育訓練','使用起重機具從事吊掛作業人員在職教育訓練','鍋爐操作人員在職教育訓練','第一種壓力容器操作人員安全衛生在職教育訓練','高壓氣體特定設備操作人員安全衛生在職教育訓練','有害作業主管在職教育訓練','以乙炔熔接裝置或氣體集合裝置從事金屬之熔接、切斷或加熱作業人員安全衛生在職教育訓練','營造業法施行前領有建築工程管理甲級或乙級技術士證者回訓課程講習','高壓室內作業人員在職教育訓練','高壓氣體、室內作業主管在職教育訓練','起重機操作及吊掛作業人員安全衛生在職教育訓練','具有危險性之機械操作人員在職教育訓練','具有危險性之設備操作人員在職教育訓練','各級業務主管在職教育訓練','高壓氣體作業主管在職教育訓練','營造作業主管在職教育訓練','一般安全衛生在職教育訓練','小型鍋爐操作人員在職教育訓練','火藥爆破作業人員在職教育訓練','露天開挖作業主管在職教育訓練','危險物品運送人員專業訓練(複訓)','起重機操作人員安全衛生在職教育訓練','鋼構組配作業主管在職教育訓練','高壓氣體容器操作人員安全衛生在職教育訓練','營造業業務主管人員在職教育訓練','施工安全評估人員在職教育訓練','危險性之設備操作人員(鍋爐、一壓、小鍋)在職教育訓練','製程安全評估人員在職教育訓練','人字臂起重桿操作人員安全衛生在職教育訓練','勞工健康服務護理人員在職教育訓練','具有危險性之設備暨小型鍋爐操作人員在職教育訓練','職業安全衛生管理人員在職教育訓練','職業安全衛生業務主管在職教育訓練','屋頂作業主管在職教育訓練','研討會','其他活動','98北市府專案一般安全衛生教育訓練─營造業','98北市府專案一般安全衛生教育訓練─局限空間作業','98北市府專案一般安全衛生教育訓練─住宿業','98北市府專案一般安全衛生教育訓練─製造業','98北市府專案一般安全衛生教育訓練─批發零售業','98北市府專案一般安全衛生教育訓練─金融及保險業','98北市府專案一般安全衛生教育訓練─醫療保健服務業','98北市府專案一般安全衛生教育訓練─餐館業','98北市府專案一般安全衛生教育訓練─建築物清潔服務業','98北市府專案一般安全衛生教育訓練─不動產及租賃業','98北市府專案一般安全衛生教育訓練─學校實驗室及實習工廠','98北市府專案一般安全衛生教育訓練─水電及燃氣供應業','98北市府專案一般安全衛生教育訓練─運輸及倉儲業','98北市府專案一般安全衛生教育訓練─保全業','98北市府專案一般安全衛生教育訓練─停車場業','98北市府專案一般安全衛生教育訓練─廢棄物處理及清除業','89勞委會委託辦理中小企業丙種勞工安全衛生業務主管函授教育訓練','一般安全衛生教育訓練-營造業','一般安全衛生教育訓練-營造業土木工程業','一般安全衛生教育訓練-營造業機電、電信及電路設備安裝業','一般安全衛生教育訓練-營造業屋頂作業','一般安全衛生教育訓練-營造業施工架作業','一般安全衛生教育訓練-營造業模板作業','一般安全衛生教育訓練-營造業泥作作業','一般安全衛生教育訓練-營造業清潔作業','一般安全衛生教育訓練-營造業金屬工程作業','一般安全衛生教育訓練-營造業拆除作業','一般安全衛生教育訓練-營造業鋼筋作業','一般安全衛生教育訓練-營造業油漆作業','一般安全衛生教育訓練-局限空間','一般安全衛生教育訓練-一般行業','一般安全衛生教育訓練-一般行業保全服務業','一般安全衛生教育訓練-一般行業餐旅業','一般安全衛生教育訓練-一般行業清潔服務業','一般安全衛生教育訓練-一般行業金融及保險業','一般安全衛生教育訓練-一般行業大眾傳播業','一般安全衛生教育訓練-一般行業水電燃氣業','一般安全衛生教育訓練-一般行業醫療保健服務業','一般安全衛生教育訓練-學校實驗室暨實習工廠','缺氧危害預防研討會','ISO45001說明會','安全衛生教育訓練單位之專責輔導員講習']
        return course in courseList

    def __call__(self):
        request = self.request
        portal = api.portal.get()
        file_data = request.get('file_data')
        file_data = file_data.split(',')[1]

        try:
            file_name = request.get('file_name', '')
            file_name = file_name.split('_')[1].split('.csv')[0]

            file_dict = {
                '台北': 'taipei',
                '花蓮': 'hualien',
                '桃園': 'taoyuan',
                '中壢': 'lieutenant',
                '嘉義': 'chiayi',
                '南科': 'nanke',
                '高雄': 'kaohsiung',
                '台中': 'taichung'
            }
            location = file_dict[file_name]
        except:
                api.portal.show_message(message='地點錯誤!!!!', type='error', request=request)
                request.response.redirect('%s/folder_contents' %portal.absolute_url())
                return


        text = base64.b64decode(file_data)
        try:
            text = text.decode('utf-8')
        except:
            text = text.decode('big5')

        f = StringIO(text)
        reader = csv.DictReader(f, delimiter=',')
        create_data = {}
        exist_data = {}
        course_list = {}
        result = api.content.find(context=portal['surver_content'], portal_type='Course')
        execSql = SqlObj()
        count = 0
        flag = True
        for item in reader:
            course = item['course']
            year = int(item['year'])
            if course:
                if not self.checkCourseName(course):
                    flag = course
                    break
                if year < 1000:
                    flag = year

        if type(flag) == str:
            api.portal.show_message(message='%s 不再課程名稱內!!!!' %flag, type='error', request=request)
            request.response.redirect('%s/folder_contents' %portal.absolute_url())
            return
        if type(flag) == int:
            api.portal.show_message(message='%s 年份錯誤!!!!' %flag, type='error', request=request)
            request.response.redirect('%s/folder_contents' %portal.absolute_url())
            return


        # 蒐集現有Course的名子及uid,方便後面比對
        for item in result:
            title = item.Title
            uid = item.UID
            course_list[title] = uid

        f = StringIO(text)
        reader = csv.DictReader(f, delimiter=',')
        for item in reader:
            try:
                if item and item['course']:
                    # 課程名稱 + '_' + 期間
                    course = item['course']
                    period = item['period']
                    subject = item['subject']
                    course_period = '%s_%s' %(course, period)
                    date = '%s/%s/%s' %(item['year'], item['month'], item['date'])
                    # 用在顯示格別科目
                    data = '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(item['quiz'], date, item['time'],
                                item['week'], subject, item['hour'], item['teacher'], item['number'], item['classroom'])
                    start_time = '%s %s:%s:00' %(date, item['time'][:2], item['time'][2:4])
                    # 寫進資料庫，之後用來顯示問卷
                    execStr = """SELECT * FROM course_list WHERE course = '{}' AND period = '{}' AND subject = '{}'
                                """.format(course, period, subject)
                    if execSql.execSql(execStr):
                        execStr = """UPDATE course_list SET start_time='{}', week='{}', hour='{}', teacher='{}', 
                                    number='{}', classroom='{}' WHERE course = '{}' AND period = '{}' AND subject = '{}' AND location = '{}'
                                    """.format(start_time, item['week'], item['hour'], item['teacher'], 
                                    item['number'], item['classroom'], course, period, subject, location)
                    else:
                        execStr = """INSERT INTO `course_list`(`course`, `period`, `start_time`, `week`, `subject`, `hour`, 
                            `teacher`, `number`, `classroom`, `quiz`, `location`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}', '{}')
                            """.format(course, period, start_time, item['week'], subject,
                               item['hour'], item['teacher'], item['number'], item['classroom'], item['quiz'], location)
                    print '33333'
#                    import pdb; pdb.set_trace()
                    execSql.execSql(execStr)

                    if course_period in course_list.keys():
                        course_uid = course_list[course_period]
                        if exist_data.has_key(course_uid):
                            exist_data[course_uid] += data
                        else:
                            exist_data[course_uid] = data
                    else:
                        if create_data.has_key(course_period):
                            create_data[course_period] += data
                        else:
                            create_data[course_period] = data
            except Exception as e:
                count += 1
                print e
                import pdb;pdb.set_trace()
        if count == 0:
            try:
                # 更新
                for k,v in exist_data.items():
                    api.content.get(UID=k).subject_list = v
                # 建立新的
                for k,v in create_data.items():
                    obj = api.content.create(
                        type='Course',
                        title=k,
                        subject_list=v,
                        container=portal['surver_content'])
                api.portal.show_message(message='上傳成功！！！', type='info', request=request)
            except:
                api.portal.show_message(nessage='更新或建立失敗！！！', type='error', request=request)
        else:
            api.portal.show_message(message='上傳格式有錯！！！', type='error', request=request)
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
        today = datetime.date.today()
        course = context.title.split('_')[0]
        period = context.title.split('_')[1]
        uid = context.UID()
        numbers = context.numbers
        execSql = SqlObj()
        for item in subject_list.split('\n'):
            if item:
                tmp = item.split(',')
                subject= tmp[4]
                execStr = """SELECT DISTINCT(seat) FROM satisfaction WHERE course = '{}' AND period = '{}' AND subject = '{}'
                    ORDER BY seat""".format(course, period, subject)
                result = execSql.execSql(execStr)
                result = [i[0] for i in result ]

                count = len(result)
                seat_str = ','.join([str(i) for i in result])
                notWrite = []

                if numbers:
                    rate ='%s%%' %(round(float(count) / float(numbers), 2) * 100)
                    for i in range(1, numbers + 1):
                        if i not in result:
                             notWrite.append(i)
                    not_seat_str = ','.join([str(i) for i in notWrite])
                else:
                    rate = '尚未設定學生人數'
                    not_seat_str = '尚未設定學生人數'
                data.append( [ tmp[1], tmp[2] , tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8], seat_str , rate, not_seat_str, count])
#        course_name = base64.b64encode(course_name)
        course_name = urllib.quote(course_name.encode('utf-8'))
        url = """{}/check_surver?course_name={}&period={}""".format(abs_url, course_name, period)
        # 滿意度
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.make_image().save('url.png')
        img = open('url.png', 'rb')
        b64_img = base64.b64encode(img.read())

        # 四個訓前
        if course in ['職業安全衛生管理員', '丙種職業安全衛生業務主管', '急救人員', '荷重在一公噸以上之堆高機操作人員']:
            self.exSurvy = True
            qr1 = qrcode.QRCode()
            title = base64.b64encode(context.title)
            qr1.add_data('%s/@@manager?course_title=%s&uid=%s' %(context.absolute_url(), title, uid))
            qr1.make_image().save('url.png')
            img = open('url.png', 'rb')
            self.managerQRcode = base64.b64encode(img.read())

            qr2 = qrcode.QRCode()
            qr2.add_data('%s/@@stacker?course_title=%s&uid=%s' %(context.absolute_url(), title, uid))
            qr2.make_image().save('url.png')
            img = open('url.png', 'rb')
            self.stackerQRcode = base64.b64encode(img.read())

            qr3 = qrcode.QRCode()
            qr3.add_data('%s/@@c_type?course_title=%s&uid=%s' %(context.absolute_url(), title, uid))
            qr3.make_image().save('url.png')
            img = open('url.png', 'rb')
            self.c_typeQRcode = base64.b64encode(img.read())

            qr4 = qrcode.QRCode()
            qr4.add_data('%s/@@emergency?course_title=%s&uid=%s' %(context.absolute_url(), title, uid))
            qr4.make_image().save('url.png')
            img = open('url.png', 'rb')
            self.emergencyQRcode = base64.b64encode(img.read())
        else:
            self.exSurvy = False

        self.url = url
        self.b64_img = b64_img
        self.data = data
        return self.template()


class CheckSurver(BrowserView):
    template = ViewPageTemplateFile('template/check_surver.pt')
    finished = ViewPageTemplateFile('template/finished.pt')
    overtime = ViewPageTemplateFile('template/overtime.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        abs_url = portal.absolute_url()

        course_name = request.get('course_name')
        period = request.get('period')
        if not api.content.find(Title='%s_%s' %(course_name, period)):
            course_name = base64.b64decode(course_name)

        seat_number = request.get('seat_number', '')
        ignore = request.get('ignore', False)
        if seat_number:
            now = datetime.datetime.now()
            now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
            url = ''
            data = {}
            already_write = []
            execSql = SqlObj()

            sqlStr = """SELECT MAX(start_time) as max  FROM course_list WHERE course = '{}' AND period = '{}'""".format(course_name, period)
            maxTime = execSql.execSql(sqlStr)[0]['max']
#            maxTime = datetime.datetime.combine(maxTime + datetime.timedelta(days=1), datetime.time(12,0))
            maxTime = maxTime.date() + datetime.timedelta(days=2)

            if not ignore and maxTime <= now.date() and ((course_name != '缺氧作業主管' and period != '412') and (course_name != '使用起重機具從事吊掛作業人員' and period != '333') and (course_name != '吊升荷重在零點五公噸以上未滿三公噸之移動式起重機操作人員' and period != '8') and (course_name != '荷重在一公噸以上之堆高機操作人員' and period != '1261')):
                return self.overtime()

            execStr = """SELECT * FROM course_list WHERE course = '{}' AND period = '{}' AND start_time <= '{}' ORDER BY            
                start_time DESC""".format(course_name, period, now_datetime)
            result = execSql.execSql(execStr)

            execStr = """SELECT course,period,subject FROM `satisfaction` WHERE seat = '{}' AND course = '{}' AND 
                period = '{}'""".format(seat_number, course_name, period)
            satisfaction_result = execSql.execSql(execStr)


            for item in satisfaction_result:
                tmp = dict(item)
                course = tmp['course']
                period = tmp['period']
                subject = tmp['subject']
                already_write.append('%s_%s_%s' %(course, period, subject))

            for item in result:
                tmp = dict(item)
                course = tmp['course']
                period = tmp['period']
                subject = tmp['subject']
                quiz = tmp['quiz']
                item_datetime = tmp['start_time']
                teacher = tmp['teacher']
                identify = '%s_%s_%s' %(course, period, subject)
                if identify not in already_write:
                    if quiz == '是':
                        url = """{}/@@satisfaction_sec?subject_name={}&date={}&teacher={}&course_name={}&period={}&seat_number={}""".format(abs_url, subject, item_datetime, teacher, course, period, seat_number)
                    else:
                        url = """{}/@@satisfaction_first?subject_name={}&date={}&teacher={}&course_name={}&period={}&seat_number={}""".format(abs_url, subject, item_datetime, teacher, course, period, seat_number)
                    break;
            if url:
                request.response.redirect(url)
                return
            else:
                return self.finished()

        self.course = course_name
        self.period = period
        return self.template()


class ShowStatistics(BrowserView):
    template = ViewPageTemplateFile('template/show_statistics.pt')
    def __call__(self):
        execSql = SqlObj()

        execStr = """SELECT DISTINCT(course) FROM `course_list`"""
        result = execSql.execSql(execStr)
        self.mode = self.request.get('mode', 0)
        self.result = result
        return self.template()


class CalculateSatisfaction(BrowserView):
    template = ViewPageTemplateFile('template/calculate_satisfaction.pt')
    def __call__(self):
        request = self.request
        course = request.get('course')
        period = request.get('period')
        self.course = course
        self.period = period
        execSql = SqlObj()
        execStr = """SELECT * FROM `satisfaction` WHERE course = '{}' AND period = '{}'
            """.format(course, period)
        result = execSql.execSql(execStr)
        if not result:
            return 'error'
        tmp_data = {}
        tmp_date_teacher = {}
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

        courseContent = api.content.find(portal_type='Course', index_course='%s_%s' %(course, period))[0].getObject()
        numbers = courseContent.numbers
        if not numbers:
            return '<h3>請設定學生人數</h3>'

        sqlStr = """SELECT COUNT(id), subject FROM `satisfaction` WHERE course = '{}' AND period = {} GROUP BY subject""".format(course, period)
        writeResult = execSql.execSql(sqlStr)
        writeCount = {}
        count = 0
        for i in writeResult:
            writeCount[i[1]] = round((float(i[0]) / float(numbers) * 100), 2)
            count += i[0]
        self.writeCount = writeCount
        self.count = count
        self.numbers = numbers * len(writeCount.keys())
        self.write_rate = round((float(count) / float(self.numbers) * 100) , 2)
#        self.count = write_number[0][0]
#        self.numbers = numbers * countSubject
#        self.numbers = countNumbers
#        self.write_rate = round((float(write_number[0][0]) / float(self.numbers) * 100) , 2)


#        subject_list = courseContent.subject_list

#        execStr = """SELECT COUNT(id) FROM `satisfaction` WHERE course = '{}' AND period = '{}'""".format(course, period)
#        write_number = execSql.execSql(execStr)

#        execStr = """SELECT DISTINCT(subject) FROM `satisfaction` WHERE course = '{}' AND period = '{}'""".format(course, period)
#        countSubject = execSql.execSql(execStr)

        # 在content的subject_list自定義課程人數
#        customData = {}
#        for item in subject_list.split('\r\n'):
#            course = item.split(',')[4]
#            try:
#                customNumber = item.split(',')[9]
#                customData[course] = customNumber
#            except:
#                pass
#        if numbers:
#            countNumbers = 0
#            for subject in countSubject:
#                import pdb;pdb.set_trace()
#                subject = subject[0]
#                if customData.has_key(subject):
                    # 有可能是空值
#                    if customData[subject]:
#                        countNumbers += int(customData[subject])
#                    else:
#                        countNumbers += numbers
#                else:
#                    countNumbers += numbers

#            self.count = write_number[0][0]
#            self.numbers = numbers * countSubject
#            self.numbers = countNumbers
#            self.write_rate = round((float(write_number[0][0]) / float(self.numbers) * 100) , 2)
#        else:
#            return '<h3>請設定學生人數</h3>'
        for item in result:
            tmp = dict(item)
            teacher = tmp['teacher'].strip()
            date = tmp['date'][:10]
            subject = tmp['subject']
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
            # 表格的各老師分數，以data為key
            if tmp_date_teacher.has_key(date):
                if tmp_date_teacher[date].has_key(teacher):
                    if tmp_date_teacher[date][teacher].has_key(subject):
                        tmp_date_teacher[date][teacher][subject].append(anwA)
                        tmp_date_teacher[date][teacher][subject].append(anwB)
                        tmp_date_teacher[date][teacher][subject].append(anwC)
                        tmp_date_teacher[date][teacher][subject].append(anwD)
                        tmp_date_teacher[date][teacher][subject].append(anwE)
                        tmp_date_teacher[date][teacher][subject].append(anwF)
                    else:
                        tmp_date_teacher[date][teacher][subject] = [anwA, anwB, anwC, anwD, anwE, anwF]
                else:
                    tmp_date_teacher[date][teacher] = {subject: [anwA, anwB, anwC, anwD, anwE, anwF]}
#                    tmp_date_teacher[date][teacher] = [anwA, anwB, anwC, anwD, anwE, anwF]
            else:
                tmp_date_teacher[date] = {teacher: {subject: [anwA, anwB, anwC, anwD, anwE, anwF]}}
#                tmp_date_teacher[date] = {teacher: [[anwA, anwB, anwC, anwD, anwE, anwF], subject]}

        date_teacher = []
        for k,v in tmp_date_teacher.items():
            for k2,v2 in v.items():
                for k3,v3 in v2.items():
                    count_5 = v3.count(5)
                    count_4 = v3.count(4)
                    count_3 = v3.count(3)
                    count_2 = v3.count(2)
                    count_1 = v3.count(1)
                    weight_5 = count_5 * 5
                    weight_4 = count_4 * 4
                    weight_3 = count_3 * 3
                    weight_2 = count_2 * 2
                    weight_1 = count_1 * 1
                    point = round((float(weight_5) + float(weight_4) + float(weight_3) + float(weight_2) + float(weight_1)) / (float(count_5) + float(count_4) + float(count_3) + float(count_2) + float(count_1)),2)
                    date_teacher.append([k, k2, point, k3])
        self.date_teacher = sorted(date_teacher, key=lambda x:x[0])
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

        self.envir_data = [tmp_envir[0], tmp_envir[1], tmp_envir[2], tmp_envir[3], tmp_envir[4]]
        self.space_data = [tmp_space[0], tmp_space[1], tmp_space[2], tmp_space[3], tmp_space[4]]

        # 計算環境分數
        origin_space = tmp_space[0] + tmp_space[1] + tmp_space[2] + tmp_space[3] + tmp_space[4] 
        weight_space = tmp_space[0] * 5 + tmp_space[1] * 4 + tmp_space[2] * 3 + tmp_space[3] * 2 + tmp_space[4] * 1
        self.point_space = round(float(weight_space) / float(origin_space) * 20, 2)

        origin_envir = tmp_envir[0] + tmp_envir[1] + tmp_envir[2] + tmp_envir[3] + tmp_envir[4] 
        weight_envir = tmp_envir[0] * 5 + tmp_envir[1] * 4 + tmp_envir[2] * 3 + tmp_envir[3] * 2 + tmp_envir[4] * 1
        self.point_envir = round(float(weight_envir) / float(origin_envir) * 20, 2)

        self.point_total = round((float(self.point_space * 10) + float(self.point_envir * 20) + float(self.point_teacher * 70)) / 100,2) 
        # 圓餅圖的資料整理
#        execStr = """SELECT COUNT(DISTINCT(teacher)) as teacher_numbers FROM satisfaction"""
#        result = execSql.execSql(execStr)
#        teacher_numbers = dict(result[0])['teacher_numbers']
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
            anw_A = int(v.count(5))
            anw_B = int(v.count(4))
            anw_C = int(v.count(3))
            anw_D = int(v.count(2))
            anw_E = int(v.count(1))
            anw_data[k] = [anw_A, anw_B, anw_C, anw_D, anw_E]

        self.anw_data = anw_data
        self.total_anw = total_anw
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
        self.course = course
        self.period = period
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
            execStr = """SELECT COUNT(id) FROM manager WHERE period = '{}'""".format(period)
            count = execSql.execSql(execStr)[0][0]
            execStr = """SELECT uid FROM manager WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
            uid = execSql.execSql(execStr)[0][0]

            content = api.content.get(UID=uid)
            numbers = content.numbers
            if numbers:
                self.count = count
                self.numbers = numbers
                self.rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
            else:
                self.rate = False
                self.abs_url = content.absolute_url()

            execStr = """SELECT * FROM manager WHERE period = '{}'""".format(period)
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

        elif course == '荷重在一公噸以上之堆高機操作人員':

            execStr = """SELECT COUNT(id) FROM stacker WHERE period = '{}'""".format(period)
            count = execSql.execSql(execStr)[0][0]
            execStr = """SELECT uid FROM stacker WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
            uid = execSql.execSql(execStr)[0][0]

            content = api.content.get(UID=uid)
            numbers = content.numbers
            if numbers:
                self.count = count
                self.numbers = numbers
                self.rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
            else:
                self.rate = False
                self.abs_url = content.absolute_url()

            execStr = """SELECT * FROM stacker WHERE period = '{}'""".format(period)
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
            execStr = """SELECT COUNT(id) FROM c_type WHERE period = '{}'""".format(period)
            count = execSql.execSql(execStr)[0][0]
            execStr = """SELECT uid FROM c_type WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
            uid = execSql.execSql(execStr)[0][0]

            content = api.content.get(UID=uid)
            numbers = content.numbers
            if numbers:
                self.count = count
                self.numbers = numbers
                self.rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
            else:
                self.rate = False
                self.abs_url = content.absolute_url()

            execStr = """SELECT * FROM c_type WHERE period = '{}'""".format(period)
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
            execStr = """SELECT COUNT(id) FROM emergency WHERE period = '{}'""".format(period)
            count = execSql.execSql(execStr)[0][0]
            execStr = """SELECT uid FROM emergency WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
            uid = execSql.execSql(execStr)[0][0]

            content = api.content.get(UID=uid)
            numbers = content.numbers
            if numbers:
                self.count = count
                self.numbers = numbers
                self.rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
            else:
                self.rate = False
                self.abs_url = content.absolute_url()
            execStr = """SELECT * FROM emergency WHERE period = '{}'""".format(period)
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
            return self.template_emergency()


class DownloadExcel(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response

        count_A = []
        count_B = []
        count_C = []
        count_D = []
        count_E = []
        count_F = []
        envir_data = []
        space_data = []
        each_teacher_data = json.loads(request.get('each_teacher_data'))
        total_anw = []

        for item in request.get('count_A').split('[')[1].split(']')[0].split(','):
            count_A.append(int(item))
        for item in request.get('count_B').split('[')[1].split(']')[0].split(','):
            count_B.append(int(item))
        for item in request.get('count_C').split('[')[1].split(']')[0].split(','):
            count_C.append(int(item))
        for item in request.get('count_D').split('[')[1].split(']')[0].split(','):
            count_D.append(int(item))
        for item in request.get('count_E').split('[')[1].split(']')[0].split(','):
            count_E.append(int(item))
        for item in request.get('count_F').split('[')[1].split(']')[0].split(','):
            count_F.append(int(item))
        for item in request.get('space_data').split('[')[1].split(']')[0].split(','):
            space_data.append(int(item))
        for item in request.get('envir_data').split('[')[1].split(']')[0].split(','):
            envir_data.append(int(item))
        for item in request.get('total_anw').split('[')[1].split(']')[0].split(','):
            total_anw.append(int(item))

        period = request.get('period')
        course = request.get('course')
        date_teacher = json.loads(request.get('date_teacher'))
        point_space = request.get('point_space')
        point_envir = request.get('point_envir')
        point_teacher = request.get('point_teacher')
        point_total = request.get('point_total')
        writeCount = json.loads(request.get('writeCount'))

        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet('Sheet1')
        worksheet2 = workbook.add_worksheet('Sheet2')

        data = [
            ['非常满意', '满意', '尚可', '不满意', '非常不满意'],
            total_anw,
            count_A,
            count_B,
            count_C,
            count_D,
            count_E,
            count_F,
            envir_data,
            space_data,
        ]

        worksheet2.write_column('A1', data[0])
        worksheet2.write_column('B1', data[1])
        worksheet2.write_column('C1', data[2])
        worksheet2.write_column('D1', data[3])
        worksheet2.write_column('E1', data[4])
        worksheet2.write_column('F1', data[5])
        worksheet2.write_column('G1', data[6])
        worksheet2.write_column('H1', data[7])
        worksheet2.write_column('I1', data[8])
        worksheet2.write_column('J1', data[9])

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$B$1:$B$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '講師總整體滿意度'})
        worksheet1.insert_chart('A1', chart_total)

        chart1 = workbook.add_chart({'type': 'pie'})
        chart1.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$C$1:$C$5',
            'data_labels': {'percentage': True},
        })
        chart1.set_title({'name': '教學態度'})
        worksheet1.insert_chart('A16', chart1)

        chart2 = workbook.add_chart({'type': 'pie'})
        chart2.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$D$1:$D$5',
            'data_labels': {'percentage': True},
        })
        chart2.set_title({'name': '教學方式能啟發學員'})
        worksheet1.insert_chart('I16', chart2)

        chart3 = workbook.add_chart({'type': 'pie'})
        chart3.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$E$1:$E$5',
            'data_labels': {'percentage': True},
        })
        chart3.set_title({'name': '能依課程、教材、內容有進度、系統講授'})
        worksheet1.insert_chart('A32', chart3)

        chart4 = workbook.add_chart({'type': 'pie'})
        chart4.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$F$1:$F$5',
            'data_labels': {'percentage': True},
        })
        chart4.set_title({'name': '講授易懂，實務化'})
        worksheet1.insert_chart('I32', chart4)

        chart5 = workbook.add_chart({'type': 'pie'})
        chart5.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$G$1:$G$5',
            'data_labels': {'percentage': True},
        })
        chart5.set_title({'name': '上課音量、口音表達適當、清晰'})
        worksheet1.insert_chart('A48', chart5)

        chart6 = workbook.add_chart({'type': 'pie'})
        chart6.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart6.set_title({'name': '提供技能檢定或考照之建議或協助'})
        worksheet1.insert_chart('I48', chart6)

        chart7 = workbook.add_chart({'type': 'pie'})
        chart7.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$I$1:$I$5',
            'data_labels': {'percentage': True},
        })
        chart7.set_title({'name': '學習環境'})
        worksheet1.insert_chart('A64', chart7)

        chart8 = workbook.add_chart({'type': 'pie'})
        chart8.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$5',
            'values':     '=Sheet2!$J$1:$J$5',
            'data_labels': {'percentage': True},
        })
        chart8.set_title({'name': '訓練服務'})
        worksheet1.insert_chart('I64', chart8)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        merge_format2 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': '#FFFFFF',
            'bg_color': '#000000'
        })

        worksheet1.merge_range('A80:D81', '第%s期' %period, merge_format2)
        worksheet1.merge_range('E80:I81', course, merge_format2)
        worksheet1.merge_range('J80:N81', '訓練班', merge_format2)
        worksheet1.merge_range('A83:N83', '總體權值分數', merge_format2)
        worksheet1.merge_range('A84:N84', point_total, merge_format)
        worksheet1.merge_range('A85:D85', '環境權值分數', merge_format2)
        worksheet1.merge_range('E85:J85', '輔導員權值分數', merge_format2)
        worksheet1.merge_range('K85:N85', '講師整體權值分數', merge_format2)
        worksheet1.merge_range('A86:D86', point_space, merge_format)
        worksheet1.merge_range('E86:J86', point_envir, merge_format)
        worksheet1.merge_range('K86:N86', point_teacher, merge_format)

        worksheet1.merge_range('A87:B87', '日期', merge_format2)
        worksheet1.merge_range('C87:F87', '科目', merge_format2)
        worksheet1.merge_range('G87:H87', '講師', merge_format2)
        worksheet1.merge_range('I87:J87', '平均權值', merge_format2)
        worksheet1.merge_range('K87:L87', '權值分數', merge_format2)
        worksheet1.merge_range('M87:N87', '填寫率', merge_format2)


        write_rate = request.get('write_rate')
        count = request.get('count')
        numbers = request.get('numbers')
        worksheet1.merge_range('P87:S87', '已填人數 / 總人數 = 回收率', merge_format2)
        worksheet1.merge_range('P88:S88', '%s / %s = %s%%' %(count, numbers, write_rate), merge_format)

        count = 1
        row = 88
        for i in date_teacher:
            worksheet1.merge_range('A%s:B%s' %(row, row), i[0], merge_format)
            worksheet1.merge_range('C%s:F%s' %(row, row), i[3], merge_format)
            worksheet1.merge_range('G%s:H%s' %(row, row), i[1], merge_format)
            worksheet1.merge_range('I%s:J%s' %(row, row), i[2], merge_format)
            worksheet1.merge_range('K%s:L%s' %(row, row), i[2] * 20, merge_format)
            worksheet1.merge_range('M%s:N%s' %(row, row), '%s%%' %writeCount[i[3]], merge_format)

            count += 1
            row += 1
        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s.xlsx"' %(course, period))
        return output.getvalue()
