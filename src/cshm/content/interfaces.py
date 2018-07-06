# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from cshm.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.namedfile.field import NamedBlobFile


class ICshmContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITask(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )


class ISurver(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    file = NamedBlobFile(
        title=_(u'File'),
        required=True
    )

class ICourse(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    subject_list = schema.Text(
        title=_(u'subject list'),
        required=True,
    )

    numbers = schema.Int(
        title=_(u'number of student'),
        required=False,
    )

