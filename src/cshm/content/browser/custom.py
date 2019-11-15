# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.auto import safeWrite
from db.connect.browser.views import SqlObj
import json
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
import smtplib


class SendOpinion(BrowserView):
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        execSql = SqlObj()

        contact = {}
        locationDict = {}
        for i in portal['contact'].getChildNodes():
            locationDict[i.id] = i.title
            contact[i.id] = {
                'good': '',
                'bad': '',
                'mail': i.description
            }

        now = datetime.now().strftime('%Y-%m-%d')
        sqlStr = """SELECT sa.*, co.location FROM satisfaction as sa, course_list as co 
            WHERE (question9 != '' OR question10 != '' OR question11 != '' OR question12 != '') 
            AND sa.timestamp LIKE '{}%%' AND sa.course = co.course AND sa.period = co.period 
            AND sa.subject = co.subject ORDER BY course
            """.format(now)

        result = execSql.execSql(sqlStr)
        for i in result:
            formatStr = """科目:{}<br>課程:{}<br>期數:{}<br>座號:{}<br>教學中心:{}<br>講師:{}<br>時間:{}<br>意見提供:<br>1. {}<br/>2. {}<br/>3. {}<br>4. {}<hr>
                """.format(i['course'], i['subject'], i['period'], i['seat'], locationDict[i['location']]
                , i['teacher'], i['date'], i['question9'], i['question10'], i['question11']
                , i['question12'])
            questionList = [i['question%s' %k] for k in range(1, 9)]
            location = i['location']
            if 1 in questionList or 2 in questionList:
                contact[location]['bad'] += formatStr
                contact['all']['bad'] += formatStr
            else:
                contact[location]['good'] += formatStr
                contact['all']['good'] += formatStr
        
        smtpObj = smtplib.SMTP('localhost')

        for k,v in contact.items():
            mail = v['mail']
            good = v['good']
            bad = v['bad']
            if good or bad:
                mailStr = '<h1>好的評論</h1>' + good + '<h1>壞的評論</h1>' + bad
                for m in mail.split('\r\n'):
                    if m:
                        mime_text = MIMEText(mailStr, 'html', 'utf-8')
                        mime_text['Subject'] = Header("%s  意見提供" %(now), 'utf-8')
                        # smtpObj.sendmail('henry@mingtak.com.tw', 'henry@mingtak.com.tw', mime_text.as_string())
                        print 'send mail to %s' %k


class SelectExcept(BrowserView):
    template = ViewPageTemplateFile('template/select_except.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        course = request.get('course')
        period = request.get('period')
        exceptList = request.get('exceptList')
        execSql = SqlObj()

        if exceptList:
            try:
                for k, v in json.loads(exceptList).items():
                    tmp = [i for i in v.split(',') if i]
                    sqlStr = """UPDATE course_list SET exceptList = %s WHERE course = '%s' AND period = '%s' and subject = '%s'
                             """ %(json.dumps(','.join(sorted(set(tmp), key=lambda x: int(x)))), course, period, k)
                    execSql.execSql(sqlStr)

                api.portal.show_message(message='更新成功!!'.encode(), request=request)
                return 'success'
            except:
                return 'error'

        if course and period:
            sqlStr = """SELECT subject, exceptList, start_time FROM course_list WHERE course = '%s' AND period = '%s' ORDER BY start_time
                     """ %(course, period)
            self.result = execSql.execSql(sqlStr)


        self.course = course
        self.period = period
        return self.template()



class CourseListing(BrowserView):
    template = ViewPageTemplateFile('template/course_listing.pt')
    def __call__(self):
        request = self.request
        if api.user.is_anonymous():
            request.response.redirect('login')
            return
        user = api.user.get_current()
        groups = user.getGroups()
        self.id = user.id

        offset = request.get('offset', 0)

        location = self.getLocation(groups)
        execSql = SqlObj()
        if user.id != 'admin':
            sqlStr = """SELECT course, period, MAX(timestamp) as maxtime FROM `course_list` WHERE location = '{}' GROUP BY course, period
                        ORDER BY `maxtime` DESC""".format(location)
        else:
            sqlStr = """SELECT course, period, MAX(timestamp) as maxtime, location FROM `course_list` GROUP BY course, period, location
                        ORDER BY maxtime  DESC"""

        self.courseList = execSql.execSql(sqlStr)
        return self.template()

    def getDateRange(self, course, period):
        execSql = SqlObj()
        sqlStr = """SELECT MAX(start_time) AS start, MIN(start_time) AS end FROM `course_list` WHERE course = '{}' and period = {}
                 """.format(course, period)
        result = execSql.execSql(sqlStr)[0]
        return '%s~%s' %(result['end'].strftime('%Y-%m-%d %H:%M'), result['start'].strftime('%Y-%m-%d %H:%M'))

    def getUrl(self, course, period):
        content = api.content.find(index_course='%s_%s' %(course, period))
        if content:
            return content[0].getObject().absolute_url()
        else:
            return 'error'

    def getLocation(self, groups):
        locationList = ['taipei', 'hualien', 'taoyuan', 'lieutenant', 'chiayi', 'nanke', 'kaohsiung', 'taichung']
        for i in locationList:
            if i in groups:
                return i
