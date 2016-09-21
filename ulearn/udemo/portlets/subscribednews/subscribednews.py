# -*- coding: utf-8 -*-
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema
from plone import api
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from zope.component.hooks import getSite
from plone.memoize.view import memoize_contextless
from DateTime.DateTime import DateTime

from souper.soup import get_soup
from repoze.catalog.query import Eq


class ISubscribedNewsPortlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=20)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )


class Assignment(base.Assignment):
    implements(ISubscribedNewsPortlet)

    def __init__(self, count=20, state=('published', )):
        self.count = count
        self.state = state

    @property
    def title(self):
        return _(u"My Subscribed News")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('subscribednews.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    # @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return self.data.count > 0 and len(self._data())

    @memoize_contextless
    def portal(self):
        return getSite()

    def published_news_items(self):
        return self._data()

    def get_noticias_folder_url(self):
        url = self.portal().absolute_url() + '/noticies'
        return url

    def dadesNoticies(self):
        noticies = self._data()
        return noticies

    def id_noticies(self, noticies):
        info_id = []
        for item in noticies:
            info_id.append(item['id'])

        return info_id

    @memoize
    def _data(self):
        # facultiesList = faculties(None).by_value.keys()
        news = []
        news_filtered = []
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        path = portal_state.navigation_root_path()
        limit = self.data.count
        state = self.data.state

        portal = getSite()
        current_user = api.user.get_current()
        userid = current_user.id

        soup_tags = get_soup('user_subscribed_tags', portal)
        tags_soup = [r for r in soup_tags.query(Eq('id', userid))]
        if tags_soup:
            tags = tags_soup[0].attrs['tags']
            news += self.get_news(context, state, path, limit, tags)
            for newObject in news:
                if newObject not in news_filtered and newObject['subject'] is not ():
                    news_filtered.append(newObject)

            newsSorted = sorted(news_filtered, key=lambda new: new['date'], reverse=True)
            return newsSorted
        else:
            return []

    def get_news(self, context, state, path, limit, tags):
        catalog = getToolByName(context, 'portal_catalog')
        now = DateTime()
        for tag in tags:
            results = catalog(portal_type='News Item',
                              review_state=state,
                              path=path,
                              expires={'query': now, 'range': 'min', },
                              sort_on='created',
                              sort_order='reverse',
                              sort_limit=limit,
                              Subject=tag)
            noticies = self.dades(results)
            for item in noticies:
                yield item

    def dades(self, noticies):
        dades = []
        for noticia in noticies:
            noticiaObj = noticia.getObject()
            if noticiaObj.text is None:
                text = None
            else:
                if noticiaObj.description:
                    text = self.abrevia(noticiaObj.description, 150)
                else:
                    text = self.abrevia(noticiaObj.text.raw, 150)
            info = {'id': noticia.id,
                    'text': text,
                    'url': noticia.getURL(),
                    'title': self.abrevia(noticia.Title, 70),
                    'new': noticiaObj,
                    'date': str(noticiaObj.modification_date.day()) + '/' + str(noticiaObj.modification_date.month()) + '/' + str(noticiaObj.modification_date.year()),
                    'image': noticiaObj.image,
                    'subject': noticiaObj.subject,
                    }

            dades.append(info)

        return dades

    def abrevia(self, summary, sumlenght):
        """ Retalla contingut de cadenes
        """
        bb = ''

        if sumlenght < len(summary):
            bb = summary[:sumlenght]

            lastspace = bb.rfind(' ')
            cutter = lastspace
            precut = bb[0:cutter]

            if precut.count('<b>') > precut.count('</b>'):
                cutter = summary.find('</b>', lastspace) + 4
            elif precut.count('<strong>') > precut.count('</strong>'):
                cutter = summary.find('</strong>', lastspace) + 9
            bb = summary[0:cutter]

            if bb.count('<p') > precut.count('</p'):
                bb += '...</p>'
            else:
                bb = bb + '...'
        else:
            bb = summary

        return bb


class AddForm(base.AddForm):
    form_fields = form.Fields(ISubscribedNewsPortlet)
    label = _(u"Add Subscribed News Portlet")
    description = _(u"This portlet displays subscribed News Items.")

    def create(self, data):
        return Assignment(count=data.get('count', 20), state=data.get('state', ('published', )))


class EditForm(base.EditForm):
    form_fields = form.Fields(ISubscribedNewsPortlet)
    label = _(u"Edit Subscribed News Portlet")
    description = _(u"This portlet displays subscribed News Items.")
