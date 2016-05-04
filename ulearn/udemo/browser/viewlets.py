# -*- coding: utf-8 -*-
from five import grok
from Acquisition import aq_inner
from zope.interface import Interface
from zope.component.hooks import getSite
from zope.security import checkPermission

from plone.app.contenttypes.interfaces import INewsItem
from plone.app.layout.viewlets.interfaces import IAboveContentTitle
from plone.memoize.view import memoize_contextless

from ulearn.udemo.interfaces import IUlearnUdemoLayer
from Products.CMFCore.utils import getToolByName
from genweb.core.adapters import IImportant
from genweb.core.utils import genweb_config

grok.context(Interface)


class viewletBase(grok.Viewlet):
    grok.baseclass()

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def genweb_config(self):
        return genweb_config()

    def pref_lang(self):
        """ Extracts the current language for the current user
        """
        lt = getToolByName(self.portal(), 'portal_languages')
        return lt.getPreferredLanguage()


class importantNews(viewletBase):
    grok.name('genweb.important')
    grok.context(INewsItem)
    grok.template('important')
    grok.viewletmanager(IAboveContentTitle)
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IUlearnUdemoLayer)

    def permisos_important(self):
        # TODO: Comprovar que l'usuari tingui permisos per a marcar com a important
        return not IImportant(self.context).is_important and checkPermission("plone.app.controlpanel.Overview", self.portal())

    def permisos_notimportant(self):
        # TODO: Comprovar que l'usuari tingui permisos per a marcar com a notimportant
        return IImportant(self.context).is_important and checkPermission("plone.app.controlpanel.Overview", self.portal())

    def isNewImportant(self):
        context = aq_inner(self.context)
        is_important = IImportant(context).is_important
        return is_important
