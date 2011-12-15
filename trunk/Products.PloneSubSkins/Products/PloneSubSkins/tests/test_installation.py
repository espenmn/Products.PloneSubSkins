import unittest
from base import Browser
from base import IntegrationTestCase
from urllib2 import HTTPError

class TestInstallation(IntegrationTestCase):
    def setUp(self):
        # we uninstall PloneSubskins and install a product that depends on it.
        # some wandering in Products.PloneTestCase source convinced me
        # not to try the more sane "don't install it in the first place" approach
        super(TestInstallation, self).setUp()
        self.loginAsPortalOwner()
        qi = self.portal.portal_quickinstaller
        installed_products = [p['id'] for p in qi.listInstalledProducts()
                              if 'SubSkins' in p['id']]
        qi.uninstallProducts(installed_products)
        # I'm using a Browser because portal_quickinstaller methods
        # don't give me the expected results
        browser = Browser()
        browser.addAuthorizationHeader()
        browser.open(self.portal.absolute_url() + '/prefs_install_products_form/')
        install_control = browser.getControl(name='products:list', index=0)
        name_of_product = [prod for prod in install_control.options
                           if 'tests.testSkinsPackage' in prod]
        install_control.value = name_of_product
        try:
            control = browser.getControl('Activate')
        except LookupError, err:
            control = browser.getControl('Install') # Plone 3.x
        try:
            control.click()
        except HTTPError, err:
            pass # It works in real browser. 
            # here in the test I get redirected to
            # http://nohost/plone/portal_quickinstaller/localhost
        browser.handleErrors = False
    def test_no_empty_choices(self):
        tool = self.portal.portal_subskinstool
        for option_name in ['base', 'top', 'text',
                            'globalnav', 'portlets', 'navigation', 
                            'calendar', 'bottom']:
            self.failUnless(getattr(tool, option_name),
                "The option %s is empty" % option_name)
        # we don't want any extra to be set on installation
        self.failIf(tool.extra)
            
def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(TestInstallation),
        ])
