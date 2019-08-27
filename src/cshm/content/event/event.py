# -*- coding: utf-8 -*-
from plone import api
from zope.globalrequest import getRequest


def initUser(event):
    request = getRequest()
    request.response.redirect('course_listing')

def compeleteEdit(content, event):
    abs_url = api.portal.get().absolute_url()
    request = getRequest()
    title = content.title.split('_')
    request.response.redirect('%s/course_view?course=%s&period=%s' %(abs_url, title[0], title[1]))
