# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from cshm.content.testing import CSHM_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that cshm.content is properly installed."""

    layer = CSHM_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cshm.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cshm.content'))

    def test_browserlayer(self):
        """Test that ICshmContentLayer is registered."""
        from cshm.content.interfaces import (
            ICshmContentLayer)
        from plone.browserlayer import utils
        self.assertIn(ICshmContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CSHM_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cshm.content'])

    def test_product_uninstalled(self):
        """Test if cshm.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cshm.content'))

    def test_browserlayer_removed(self):
        """Test that ICshmContentLayer is removed."""
        from cshm.content.interfaces import \
            ICshmContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICshmContentLayer, utils.registered_layers())
