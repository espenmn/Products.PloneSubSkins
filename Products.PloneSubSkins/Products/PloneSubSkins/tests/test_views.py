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
    def test_image_view(self):
        browser = Browser()
        browser.handleErrors = False
        browser.open(self.portal.absolute_url() +
                     '/subskins_getimage/%23ff44aa/SubSkinsTool.gif')
    def test_color_dim(self):
        dim = self.portal.restrictedTraverse('@@dim_to')
        gray = dim.black('#ffffff', '50')
        self.failUnlessEqual(gray, '#808080')
        gray = dim.white('#000000', '50')
        self.failUnlessEqual(gray, '#808080')
        gray = dim.black('#408020', '50')
        self.failUnlessEqual(gray, '#204010')
        gray = self.portal.dim_to_black('#408020', '50')
        self.failUnlessEqual(gray, '#204010')

def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(TestViews),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

