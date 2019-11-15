# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.auto import safeWrite
from db.connect.browser.views import SqlObj
import json
import csv
import datetime
from StringIO import StringIO
import requests
import xlsxwriter
import inspect


class DownloadTeacherStatistics(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        teacher = request.get('teacher')
        execSql = SqlObj()

        user = api.user.get_current()
        groups = user.getGroups()

        sqlStr = """SELECT * FROM `satisfaction` WHERE teacher = '{}'""".format(teacher)

        data = {}
        result = execSql.execSql(sqlStr)
        for i in result:
            course = i['course']
            period = i['period']
            subject = i['subject']
            q1 = i['question1']
            q2 = i['question2']
            q3 = i['question3']
            q4 = i['question4']
            q5 = i['question5']
            q8 = i['question8'] or 0

            title = '%s_%s_%s' %(course, period, subject)
            if not data.has_key(title):
                data[title] = {
                    'count': {5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0:0},
                    'date': i['date'][:16]
                }

            data[title]['count'][q1] += 1
            data[title]['count'][q2] += 1
            data[title]['count'][q3] += 1
            data[title]['count'][q4] += 1
            data[title]['count'][q5] += 1
            data[title]['count'][q8] += 1


        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        merge_format = workbook.add_format({
            'bold': 1,   
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        merge_format2 = workbook.add_format({
            'bold': 1,   
            'border': 1,
        })

        worksheet1 = workbook.add_worksheet('Sheet1')

        worksheet1.set_column('A:A', 20)
        worksheet1.set_column('B:B', 50)
        worksheet1.set_column('D:D', 50)

        worksheet1.write('A1', '時間', merge_format)
        worksheet1.write('B1', '課程', merge_format)
        worksheet1.write('C1', '期別', merge_format)
        worksheet1.write('D1', '科目', merge_format)
        worksheet1.write('E1', '平均權值', merge_format)
        worksheet1.write('F1', '權值分數', merge_format)

        index = 2
        data = sorted(data.items(), key=lambda x: x[1]['date'], reverse=True)
        for i in data:
            v = i[1]['count']
            weight = float(v[5] * 5 + v[4] * 4 + v[3] * 3 + v[2] *2 + v[1] * 1)
            score = round(weight / float(v[5] + v[4] + v[3] + v[2] + v[1]), 2)

            worksheet1.write('A%s' %index, i[1]['date'], merge_format2)
            worksheet1.write('B%s' %index, i[0].split('_')[0], merge_format2)
            worksheet1.write('C%s' %index, i[0].split('_')[1], merge_format2)
            worksheet1.write('D%s' %index, i[0].split('_')[2], merge_format2)
            worksheet1.write('E%s' %index, str(score), merge_format2)
            worksheet1.write('F%s' %index, str(round(float(score) * 20.0, 2)), merge_format2)
            index += 1
        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s.xlsx"' %(teacher))
        return output.getvalue()


class DownloadOpinion(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        portal = api.portal.get()
        course = request.get('course')
        period = request.get('period')
        execSql = SqlObj()

        user = api.user.get_current()
        groups = user.getGroups()
        # 判斷課程的location 跟登入者的是否一致
        if user.id != 'admin':
            locationList = ['taipei', 'hualien', 'taoyuan', 'lieutenant', 'chiayi', 'nanke', 'kaohsiung', 'taichung']
            for i in locationList:
                if i in groups:
                    location = i
                    break
            sqlStr = """SELECT id FROM  course_list WHERE course = '{}' AND period = {} AND location = '{}'
                     """.format(course, period, location)
            if not execSql.execSql(sqlStr):
                response.redirect('%s/show_satisfaction' %portal.absolute_url())
                api.portal.show_message(message='查詢不到課程'.encode(), request=request, type='error')
                return

        sqlStr = """SELECT seat, subject, date, teacher, question9, question10, question11, question12 FROM satisfaction WHERE
                    (question9 != '' OR question10 != '' OR question11 != '' OR question12 != '') AND course = '{}' AND period = {}
                    ORDER BY date""".format(course, period)
        result = execSql.execSql(sqlStr)

        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })

        worksheet1 = workbook.add_worksheet('Sheet1')

        worksheet1.merge_range('A1:D1', '課程', merge_format)
        worksheet1.merge_range('E1:F1', '座號', merge_format)
        worksheet1.merge_range('G1:I1', '上課時間', merge_format)
        worksheet1.merge_range('J1:K1', '老師', merge_format)
        worksheet1.merge_range('L1:O1', '意見一', merge_format)
        worksheet1.merge_range('P1:S1', '意見二', merge_format)
        worksheet1.merge_range('T1:W1', '意見三', merge_format)
        worksheet1.merge_range('X1:AA1', '意見四', merge_format)

        index = 2
        for i in result:
            worksheet1.merge_range('A%s:D%s' %(index, index), i[1], merge_format)
            worksheet1.merge_range('E%s:F%s' %(index, index), str(i[0]), merge_format)
            worksheet1.merge_range('G%s:I%s' %(index, index), i[2], merge_format)
            worksheet1.merge_range('J%s:K%s' %(index, index), i[3].encode(), merge_format)
            worksheet1.merge_range('L%s:O%s' %(index, index), i[4].encode(), merge_format)
            worksheet1.merge_range('P%s:S%s' %(index, index), i[5].encode(), merge_format)
            worksheet1.merge_range('T%s:W%s' %(index, index), i[6].encode(), merge_format)
            worksheet1.merge_range('X%s:AA%s' %(index, index), i[7].encode(), merge_format)
            index += 1
        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s 意見回饋.xlsx"' %(course, period))
        return output.getvalue()



class DownloadManagerExcel(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        data = json.loads(request.get('data'))
        course = request.get('course')
        period = request.get('period')

        execSql = SqlObj()
#        execStr = """SELECT COUNT(id), uid FROM manager WHERE period = '{}' GROUP by uid""".format(period)
#        count_result = execSql.execSql(execStr)[0]
#        count = count_result[0]
#        uid = count_result[1]

        execStr = """SELECT COUNT(id) FROM manager WHERE period = '{}'""".format(period)
        count = execSql.execSql(execStr)[0][0]
        execStr = """SELECT uid FROM manager WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
        uid = execSql.execSql(execStr)[0][0]


        content = api.content.get(UID=uid)
        numbers = content.numbers
        if numbers:
            rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
        else:
            rate = False

        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet('Sheet1')
        worksheet2 = workbook.add_worksheet('Sheet2')

        worksheet2.write_column('A1', data['2'].keys())
        worksheet2.write_column('B1', data['2'].values())
        worksheet2.write_column('C1', data['3'].keys())
        worksheet2.write_column('D1', data['3'].values())
        worksheet2.write_column('E1', data['4'].keys())
        worksheet2.write_column('F1', data['4'].values())
        worksheet2.write_column('G1', data['5'].keys())
        worksheet2.write_column('H1', data['5'].values())
        worksheet2.write_column('I1', data['6'].keys())
        worksheet2.write_column('J1', data['6'].values())
        worksheet2.write_column('K1', data['7'].keys())
        worksheet2.write_column('L1', data['7'].values())
        worksheet2.write_column('M1', data['8'].keys())
        worksheet2.write_column('N1', data['8'].values())
        worksheet2.write_column('O1', data['9'].keys())
        worksheet2.write_column('P1', data['9'].values())
        worksheet2.write_column('Q1', data['10'].keys())
        worksheet2.write_column('R1', data['10'].values())
        worksheet2.write_column('S1', data['11'].keys())
        worksheet2.write_column('T1', data['11'].values())
        worksheet2.write_column('U1', data['12'].keys())
        worksheet2.write_column('V1', data['12'].values())
        worksheet2.write_column('W1', data['13'].keys())
        worksheet2.write_column('X1', data['13'].values())
        worksheet2.write_column('Y1', data['14'].keys())
        worksheet2.write_column('Z1', data['14'].values())

        title_style = workbook.add_format({'align': 'center','valign': 'vcenter', 'font_size': '20'})

        worksheet1.merge_range('A1:P3', '中國勞工安全衛生管理學會', title_style)
        worksheet1.merge_range('A4:P6', '第%s期   【   %s   】   訓練班'  %(period, course), title_style)
        worksheet1.merge_range('A7:P9', '訓前調查表', title_style)

        worksheet1.merge_range('Q1:W2', '已填份數 / 總份數 = 回收率', title_style)
        if rate:
            worksheet1.merge_range('Q3:W4', '%s / %s = %s' %(count, numbers, rate), title_style)
        else:
            worksheet1.merge_range('Q3:W4', '尚未設定人數', title_style)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A10', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I10', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$3',
            'values':     '=Sheet2!$L$1:$L$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '據您所知，職業安全衛生法之中央主管機關為何單位', 'name_font': {'size': 13}})
        worksheet1.insert_chart('I41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$3',
            'values':     '=Sheet2!$N$1:$N$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '防止職業災害，保障工作者健康及安全為下列合法之宗旨', 'name_font': {'size': 13}})
        worksheet1.insert_chart('A56', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$3',
            'values':     '=Sheet2!$P$1:$P$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '何者為符合資格之職業安全衛生管理員'})
        worksheet1.insert_chart('I56', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$Q$1:$Q$3',
            'values':     '=Sheet2!$R$1:$R$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '王先生受雇於OO建設有限公司，某日上班再公司內不小心跌倒導致右手閉骨折，是否屬於職業災害', 'name_font': {'size': 9}})
        worksheet1.insert_chart('A71', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$S$1:$S$3',
            'values':     '=Sheet2!$T$1:$T$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '職業安全衛生法已字103.7.3正式施行，其適用範圍(行業)為何', 'name_font': {'size': 13}})
        worksheet1.insert_chart('I71', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$U$1:$U$3',
            'values':     '=Sheet2!$V$1:$V$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '僱主對勞工實施必要之安全衛生教育訓練'})
        worksheet1.insert_chart('A86', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$W$1:$W$3',
            'values':     '=Sheet2!$X$1:$X$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '作業中有物體飛落致為害勞工之虞，下列何者正確'})
        worksheet1.insert_chart('I86', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$Y$1:$Y$3',
            'values':     '=Sheet2!$Z$1:$Z$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '下列何項為高架作業'})
        worksheet1.insert_chart('A101', chart_total)

        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s.xlsx"' %(course, period))
        return output.getvalue()


class DownloadStackerExcel(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        data = json.loads(request.get('data'))
        course = request.get('course')
        period = request.get('period')

        execSql = SqlObj()
#        execStr = """SELECT COUNT(id), uid FROM stacker WHERE period = '{}' GROUP by uid""".format(period)
#        count_result = execSql.execSql(execStr)[0]
#        count = count_result[0]
#        uid = count_result[1]

        execStr = """SELECT COUNT(id) FROM stacker WHERE period = '{}'""".format(period)
        count = execSql.execSql(execStr)[0][0]
        execStr = """SELECT uid FROM stacker WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
        uid = execSql.execSql(execStr)[0][0]

        content = api.content.get(UID=uid)
        numbers = content.numbers
        if numbers:
            rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
        else:
            rate = False

        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet('Sheet1')
        worksheet2 = workbook.add_worksheet('Sheet2')

        worksheet2.write_column('A1', data['2'].keys())
        worksheet2.write_column('B1', data['2'].values())
        worksheet2.write_column('C1', data['3'].keys())
        worksheet2.write_column('D1', data['3'].values())
        worksheet2.write_column('E1', data['4'].keys())
        worksheet2.write_column('F1', data['4'].values())
        worksheet2.write_column('G1', data['5'].keys())
        worksheet2.write_column('H1', data['5'].values())
        worksheet2.write_column('I1', data['6'].keys())
        worksheet2.write_column('J1', data['6'].values())
        worksheet2.write_column('K1', data['7'].keys())
        worksheet2.write_column('L1', data['7'].values())
        worksheet2.write_column('M1', data['8'].keys())
        worksheet2.write_column('N1', data['8'].values())
        worksheet2.write_column('O1', data['9'].keys())
        worksheet2.write_column('P1', data['9'].values())

        title_style = workbook.add_format({'align': 'center','valign': 'vcenter', 'font_size': '20'})

        worksheet1.merge_range('A1:P3', '中國勞工安全衛生管理學會', title_style)
        worksheet1.merge_range('A4:P6', '第%s期   【   %s   】   訓練班'  %(period, course), title_style)
        worksheet1.merge_range('A7:P9', '訓前調查表', title_style)

        worksheet1.merge_range('Q1:W2', '已填份數 / 總份數 = 回收率', title_style)
        if rate:
            worksheet1.merge_range('Q3:W4', '%s / %s = %s' %(count, numbers, rate), title_style)
        else:
            worksheet1.merge_range('Q3:W4', '尚未設定人數', title_style)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A11', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I11', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$4',
            'values':     '=Sheet2!$L$1:$L$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '學歷'})
        worksheet1.insert_chart('I41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$3',
            'values':     '=Sheet2!$N$1:$N$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '有無汽車駕駛執照'})
        worksheet1.insert_chart('A56', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$3',
            'values':     '=Sheet2!$P$1:$P$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '堆高機'})
        worksheet1.insert_chart('I56', chart_total)

        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s.xlsx"' %(course, period))
        return output.getvalue()


class DownloadCtypeExcel(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        data = json.loads(request.get('data'))
        course = request.get('course')
        period = request.get('period')

        execSql = SqlObj()
#        execStr = """SELECT COUNT(id), uid FROM c_type WHERE period = '{}' GROUP by uid""".format(period)
#        count_result = execSql.execSql(execStr)[0]
#        count = count_result[0]
#        uid = count_result[1]

        execStr = """SELECT COUNT(id) FROM c_type WHERE period = '{}'""".format(period)
        count = execSql.execSql(execStr)[0][0]
        execStr = """SELECT uid FROM c_type WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
        uid = execSql.execSql(execStr)[0][0]

        content = api.content.get(UID=uid)
        numbers = content.numbers
        if numbers:
            rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
        else:
            rate = False

        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet('Sheet1')
        worksheet2 = workbook.add_worksheet('Sheet2')

        worksheet2.write_column('A1', data['2'].keys())
        worksheet2.write_column('B1', data['2'].values())
        worksheet2.write_column('C1', data['3'].keys())
        worksheet2.write_column('D1', data['3'].values())
        worksheet2.write_column('E1', data['4'].keys())
        worksheet2.write_column('F1', data['4'].values())
        worksheet2.write_column('G1', data['5'].keys())
        worksheet2.write_column('H1', data['5'].values())
        worksheet2.write_column('I1', data['6'].keys())
        worksheet2.write_column('J1', data['6'].values())
        worksheet2.write_column('K1', data['7'].keys())
        worksheet2.write_column('L1', data['7'].values())
        worksheet2.write_column('M1', data['8'].keys())
        worksheet2.write_column('N1', data['8'].values())
        worksheet2.write_column('O1', data['9'].keys())
        worksheet2.write_column('P1', data['9'].values())

        title_style = workbook.add_format({'align': 'center','valign': 'vcenter', 'font_size': '20'})

        worksheet1.merge_range('A1:P3', '中國勞工安全衛生管理學會', title_style)
        worksheet1.merge_range('A4:P6', '第%s期   【   %s   】   訓練班'  %(period, course), title_style)
        worksheet1.merge_range('A7:P9', '訓前調查表', title_style)

        worksheet1.merge_range('Q1:W2', '已填份數 / 總份數 = 回收率', title_style)
        if rate:
            worksheet1.merge_range('Q3:W4', '%s / %s = %s' %(count, numbers, rate), title_style)
        else:
            worksheet1.merge_range('Q3:W4', '尚未設定人數', title_style)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A11', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I11', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$4',
            'values':     '=Sheet2!$L$1:$L$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '職業安全衛生法之中央主管機關為何單位'})
        worksheet1.insert_chart('I41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$3',
            'values':     '=Sheet2!$N$1:$N$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '勞動契約係以下列何種目的為正確'})
        worksheet1.insert_chart('A56', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$3',
            'values':     '=Sheet2!$P$1:$P$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '丙種職業安全衛生業務主管式用於僱用多少人以下之事業單位', 'name_font': {'size': 13}})
        worksheet1.insert_chart('I56', chart_total)

        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s.xlsx"' %(course, period))
        return output.getvalue()


class DownloadEmergencyExcel(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        data = json.loads(request.get('data'))
        course = request.get('course')
        period = request.get('period')

        execSql = SqlObj()

#        execStr = """SELECT COUNT(id), uid FROM emergency WHERE period = '{}' GROUP by uid""".format(period)
#        count_result = execSql.execSql(execStr)[0]
#        count = count_result[0]
#        uid = count_result[1]

        execStr = """SELECT COUNT(id) FROM emergency WHERE period = '{}'""".format(period)
        count = execSql.execSql(execStr)[0][0]
        execStr = """SELECT uid FROM emergency WHERE period = '{}' and uid != '' LIMIT 1""".format(period)
        uid = execSql.execSql(execStr)[0][0]

        content = api.content.get(UID=uid)
        numbers = content.numbers
        if numbers:
            rate = '%s%%' %round(float(count) / float(numbers) * 100, 1)
        else:
            rate = False

        output = StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet('Sheet1')
        worksheet2 = workbook.add_worksheet('Sheet2')

        worksheet2.write_column('A1', data['2'].keys())
        worksheet2.write_column('B1', data['2'].values())
        worksheet2.write_column('C1', data['3'].keys())
        worksheet2.write_column('D1', data['3'].values())
        worksheet2.write_column('E1', data['4'].keys())
        worksheet2.write_column('F1', data['4'].values())
        worksheet2.write_column('G1', data['5'].keys())
        worksheet2.write_column('H1', data['5'].values())
        worksheet2.write_column('I1', data['6'].keys())
        worksheet2.write_column('J1', data['6'].values())
        worksheet2.write_column('K1', data['7'].keys())
        worksheet2.write_column('L1', data['7'].values())
        worksheet2.write_column('M1', data['8'].keys())
        worksheet2.write_column('N1', data['8'].values())
        worksheet2.write_column('O1', data['9'].keys())
        worksheet2.write_column('P1', data['9'].values())
        worksheet2.write_column('Q1', data['10'].keys())
        worksheet2.write_column('R1', data['10'].values())

        title_style = workbook.add_format({'align': 'center','valign': 'vcenter', 'font_size': '20'})

        worksheet1.merge_range('A1:P3', '中國勞工安全衛生管理學會', title_style)
        worksheet1.merge_range('A4:P6', '第%s期   【   %s   】   訓練班'  %(period, course), title_style)
        worksheet1.merge_range('A7:P9', '訓前調查表', title_style)

        worksheet1.merge_range('Q1:W2', '已填份數 / 總份數 = 回收率', title_style)
        if rate:
            worksheet1.merge_range('Q3:W4', '%s / %s = %s' %(count, numbers, rate), title_style)
        else:
            worksheet1.merge_range('Q3:W4', '尚未設定人數', title_style)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A11', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I11', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I26', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$2',
            'values':     '=Sheet2!$L$1:$L$2',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '是否曾經從事醫護工作'})
        worksheet1.insert_chart('I41', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$4',
            'values':     '=Sheet2!$N$1:$N$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '預觸電患者急救時應先'})
        worksheet1.insert_chart('A56', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$4',
            'values':     '=Sheet2!$P$1:$P$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '遇到車禍事件，發現有人員受傷躺在現場，可否移動患者', 'name_font': {'size': 13},})
        worksheet1.insert_chart('I56', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$Q$1:$Q$3',
            'values':     '=Sheet2!$R$1:$R$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({
            'name': '發現民眾倒臥再旁，且呈現無意識，缺氧狀快，應於幾分鐘內施予急救',
            'name_font': {'size': 13},
        })
        worksheet1.insert_chart('A71', chart_total)

        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s.xlsx"' %(course, period))
        return output.getvalue()

