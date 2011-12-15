import unittest
from base import IntegrationTestCase
from Products.PloneSubSkins.browser.views import CssDebugModeControl
from zope.publisher.browser import TestRequest
from base import Browser

class TestViews(IntegrationTestCase):
    def test_css_debug_mode_view(self):
        browser = Browser()
        browser.addAuthorizationHeader()
        browser.open(self.portal.absolute_url() + '/css_debug_mode_control')
        self.failUnlessEqual(browser.contents, 'false')
        view = CssDebugModeControl(self.portal, TestRequest())
        view.disable()
        self.failIf(view.isEnabled())
        view.enable()
        self.failUnless(view.isEnabled())
        browser.open(self.portal.absolute_url() + '/css_debug_mode_control')
        self.failUnlessEqual(browser.contents, 'true')
        browser.open(self.portal.absolute_url() + '/css_debug_mode_control?disable=1')
        self.failUnlessEqual(browser.contents, 'false')
        self.failIf(view.isEnabled())

def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(TestViews),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

