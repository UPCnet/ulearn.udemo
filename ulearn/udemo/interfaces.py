# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from ulearn.theme.browser.interfaces import IUlearnTheme


class IUlearnUdemoLayer(IUlearnTheme):
    """Marker interface that defines a Zope 3 browser layer."""
