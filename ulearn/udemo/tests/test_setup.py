# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ulearn.udemo.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ulearn.udemo into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ulearn.udemo is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ulearn.udemo'))

    def test_uninstall(self):
        """Test if ulearn.udemo is cleanly uninstalled."""
        self.installer.uninstallProducts(['ulearn.udemo'])
        self.assertFalse(self.installer.isProductInstalled('ulearn.udemo'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IUlearnUdemoLayer is registered."""
        from ulearn.udemo.interfaces import IUlearnUdemoLayer
        from plone.browserlayer import utils
        self.failUnless(IUlearnUdemoLayer in utils.registered_layers())
