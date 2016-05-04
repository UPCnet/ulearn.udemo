from Acquisition import aq_inner
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
