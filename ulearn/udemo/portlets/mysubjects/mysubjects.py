# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from ulearn.core.controlpanel import IUlearnControlPanelSettings
import requests


class IMySubjectsPortlet(IPortletDataProvider):
    """ A portlet which can show actived.
    """


class Assignment(base.Assignment):
    implements(IMySubjectsPortlet)

    title = _(u'label_subjects', default=u'My Subjects')


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('mysubjects.pt')

    def getSubjects(self):
        """ return list of user subjects to show in portlet """

        mtool = self.context.portal_membership
        userid = mtool.getAuthenticatedMember().id

        payload = {"wstoken": 'dd767d33520a27a30d15a96415655b1b',
                   "wsfunction": 'local_blanquerna_get_pending_tasks',
                   "moodlewsrestformat": 'json',
                   "username": userid.lower(),
                   }

        req = requests.post("http://eva.blanquerna.edu/webservice/rest/server.php",
                            data=payload,
                            verify=False)
        # userSubjects = json.loads(req.json())
        userSubjects = {"teacherCourses": [{"name": "Curso de buenas prácticas", "link": "http://campus.upcnet.es/course/view.php?id=6","activities":[],"alerts":0},
                                           {"name": "Curso eLearning UPCnet", "link": "http://campus.upcnet.es/course/view.php?id=15","activities":[{"name":"Tasca","link":"http:\\/\\/eva.blanquerna.edu\\/local\\/blanquerna\\/blanquernaActivities.php?id=c4f8635f&amp;idUser=c2f9615d&amp;module=94ba2505105d&amp;items=ccf86f4046027962","pending":2}],"alerts":2}],
                        "studentCourses": [{"name": "English 2.0", "link": "http://campus.upcnet.es/course/view.php?id=2","activities":[{"name":"Tasca","link":"http:\\/\\/eva.blanquerna.edu\\/local\\/blanquerna\\/blanquernaActivities.php?id=c4f8635e&amp;idUser=c2f9615d&amp;module=94ba2505105d&amp;items=c4fb645d","pending":1}],"alerts":1}]}
        return userSubjects

    def getPrimaryColor(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IUlearnControlPanelSettings)
        return settings.main_color


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
