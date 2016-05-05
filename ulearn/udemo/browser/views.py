from five import grok
from plone import api
from Acquisition import aq_inner
from zope.interface import Interface
from ulearn.udemo.interfaces import IUlearnUdemoLayer
from Products.CMFCore.utils import getToolByName
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.contenttypes.behaviors.collection import ICollection


class SummaryViewNews(FolderView):
    # grok.name('summary_view_news')
    # grok.context(ISyndicatableCollection)
    # grok.require('zope2.View')
    # grok.template('summary_view_news')
    # grok.layer(IGebropharmaLayer)

    def __init__(self, *args, **kwargs):
        super(SummaryViewNews, self).__init__(*args, **kwargs)
        context = aq_inner(self.context)
        self.collection_behavior = ICollection(context)
        self.b_size = self.collection_behavior.item_count

    def results(self, **kwargs):
        """Return a content listing based result set with results from the
        collection query.

        :param **kwargs: Any keyword argument, which can be used for catalog
                         queries.
        :type  **kwargs: keyword argument

        :returns: plone.app.contentlisting based result set.
        :rtype: ``plone.app.contentlisting.interfaces.IContentListing`` based
                sequence.
        """
        # Extra filter
        contentFilter = self.request.get('contentFilter', {})
        contentFilter.update(kwargs.get('contentFilter', {}))
        kwargs.setdefault('custom_query', contentFilter)
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)

        results = self.collection_behavior.results(**kwargs)
        return results

    def batch(self):
        # collection is already batched.
        return self.results()

    def getFoldersAndImages(self, **kwargs):
        context = aq_inner(self.context)
        wrapped = ICollection(context)
        return wrapped.getFoldersAndImages(**kwargs)

    def selectedViewFields(self):
        """Returns a list of all metadata fields from the catalog that were
           selected.
        """
        context = aq_inner(self.context)
        wrapped = ICollection(context)
        return wrapped.selectedViewFields()

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

    def effectiveDate(self, item):
        if item.EffectiveDate() == 'None':
            date = str(item.creation_date.day()) + '/' + str(item.creation_date.month()) + '/' + str(item.creation_date.year()),
        else:
            date = str(item.effective_date.day()) + '/' + str(item.effective_date.month()) + '/' + str(item.effective_date.year()),
        return date[0]

    def abreviaText(self, item):
        text = self.abrevia(item.text.raw, 180)
        return text


class ContentsPrettyView(grok.View):
    """ Show content in a pretty way for every folder. """
    grok.name('contents_pretty_view')
    grok.context(Interface)
    grok.require('genweb.member')
    grok.template('contents_pretty')
    grok.layer(IUlearnUdemoLayer)

    def getItemPropierties(self):
        all_items = []

        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        nElements = 2
        llistaElements = []

        items = catalog.searchResults(path={'query': path, 'depth': 1},
                                      sort_on="getObjPositionInParent")
        all_items += [{'item_title': item.Title,
                       'item_desc': item.Description[:110],
                       'item_type': item.portal_type,
                       'item_url': item.getURL(),
                       'item_path': item.getPath(),
                       'item_state': item.review_state,
                       } for item in items if item.exclude_from_nav is False]

        if len(all_items) > 0:
            # Retorna una llista amb els elements en blocs de 2 elements
            llistaElements = [all_items[i:i + nElements] for i in range(0, len(all_items), nElements)]
        return llistaElements

    def getBlocs(self):
        llistaElements = self.getItemPropierties()
        return len(llistaElements)

    def getSubItemPropierties(self, item_path):
        all_items = []
        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        path = item_path

        items = catalog.searchResults(path={'query': path, 'depth': 1},
                                      sort_on="getObjPositionInParent")
        all_items += [{'item_title': item2.Title,
                       'item_desc': item2.Description[:120],
                       'item_type': item2.portal_type,
                       'item_url': item2.getURL(),
                       'item_state': item2.review_state
                       } for item2 in items if item2.exclude_from_nav is False]
        return all_items
