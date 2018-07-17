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


class DownloadManagerExcel(BrowserView):
    def __call__(self):
        request = self.request
        response = request.response
        data = json.loads(request.get('data'))
        course = request.get('course')
        period = request.get('period')

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


        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$3',
            'values':     '=Sheet2!$L$1:$L$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '據您所知，職業安全衛生法之中央主管機關為何單位'})
        worksheet1.insert_chart('I31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$3',
            'values':     '=Sheet2!$N$1:$N$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '保障工作者健康及安全為下列合法之宗旨'})
        worksheet1.insert_chart('A46', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$3',
            'values':     '=Sheet2!$P$1:$P$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '何者為符合資格之職業安全衛生管理員'})
        worksheet1.insert_chart('I46', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$Q$1:$Q$3',
            'values':     '=Sheet2!$R$1:$R$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '王先生受雇於OO建設有限公司'})
        worksheet1.insert_chart('A61', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$S$1:$S$3',
            'values':     '=Sheet2!$T$1:$T$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '職業安全衛生法已字103.7.3正式施行'})
        worksheet1.insert_chart('I61', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$U$1:$U$3',
            'values':     '=Sheet2!$V$1:$V$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '僱主對勞工實施必要之安全衛生教育訓練'})
        worksheet1.insert_chart('A76', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$W$1:$W$3',
            'values':     '=Sheet2!$X$1:$X$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '作業中有物體飛落致為害勞工之虞'})
        worksheet1.insert_chart('I76', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$Y$1:$Y$3',
            'values':     '=Sheet2!$Z$1:$Z$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '下列何項為高架作業'})
        worksheet1.insert_chart('A91', chart_total)

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

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$4',
            'values':     '=Sheet2!$L$1:$L$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '學歷'})
        worksheet1.insert_chart('I31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$3',
            'values':     '=Sheet2!$N$1:$N$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '有無汽車駕駛執照'})
        worksheet1.insert_chart('A46', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$3',
            'values':     '=Sheet2!$P$1:$P$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '堆高機'})
        worksheet1.insert_chart('I46', chart_total)

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

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$4',
            'values':     '=Sheet2!$L$1:$L$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '職業安全衛生法之中央主管機關為何單位'})
        worksheet1.insert_chart('I31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$3',
            'values':     '=Sheet2!$N$1:$N$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '勞動契約係以下列何種目的為正確'})
        worksheet1.insert_chart('A46', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$3',
            'values':     '=Sheet2!$P$1:$P$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '僱用多少人以下之事業單位'})
        worksheet1.insert_chart('I46', chart_total)

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

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$A$1:$A$4',
            'values':     '=Sheet2!$B$1:$B$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '參訓目的'})
        worksheet1.insert_chart('A1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$C$1:$C$4',
            'values':     '=Sheet2!$D$1:$D$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '年齡'})
        worksheet1.insert_chart('I1', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$E$1:$E$11',
            'values':     '=Sheet2!$F$1:$F$11',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '行業別'})
        worksheet1.insert_chart('A16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$G$1:$G$5',
            'values':     '=Sheet2!$H$1:$H$5',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您是如何知道本項訓練課程'})
        worksheet1.insert_chart('I16', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$I$1:$I$4',
            'values':     '=Sheet2!$J$1:$J$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '您選擇本中心得因素(複選)'})
        worksheet1.insert_chart('A31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$K$1:$K$2',
            'values':     '=Sheet2!$L$1:$L$2',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '是否曾經從事醫護工作'})
        worksheet1.insert_chart('I31', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$M$1:$M$4',
            'values':     '=Sheet2!$N$1:$N$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '預觸電患者急救時應先'})
        worksheet1.insert_chart('A46', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$O$1:$O$4',
            'values':     '=Sheet2!$P$1:$P$4',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '可否移動患者'})
        worksheet1.insert_chart('I46', chart_total)

        chart_total = workbook.add_chart({'type': 'pie'})
        chart_total.add_series({
            'name':       'Pie sales data',
            'categories': '=Sheet2!$Q$1:$Q$3',
            'values':     '=Sheet2!$R$1:$R$3',
            'data_labels': {'percentage': True},
        })
        chart_total.set_title({'name': '應於幾分鐘內施予急救'})
        worksheet1.insert_chart('A61', chart_total)

        workbook.close()

        response.setHeader('Content-Type',  'application/x-xlsx')
        response.setHeader('Content-Disposition', 'attachment; filename="%s-%s.xlsx"' %(course, period))
        return output.getvalue()

