# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.auto import safeWrite
from db.connect.browser.views import SqlObj
import json


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
