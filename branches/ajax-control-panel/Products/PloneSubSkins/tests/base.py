from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.Five.testbrowser import Browser as BaseBrowser
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ptc.setupPloneSite()

import Products.PloneSubSkins
ptc.setupPloneSite(products=['PloneSubSkins'])

@onsetup
def setup_product():
        fiveconfigure.debug_mode = True
        from Products.PloneSubSkins.tests import testSkinsPackage
        zcml.load_config('configure.zcml',
                         testSkinsPackage)
        fiveconfigure.debug_mode = False
setup_product()

class  IntegrationTestCase(ptc.FunctionalTestCase):
    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal.portal_quickinstaller.installProduct('PloneSubSkins.tests.testSkinsPackage')
        self.css_url = self.portal.portal_css.absolute_url() + "/subskinstest"
        self.portal.portal_subskinstool._updateProperty('colorschemes','colors_test')
    def is_css_enabled(self,cssname):
        return self.portal.portal_css.getResourcesDict()[cssname].getEnabled()

class Browser(BaseBrowser):
    def addAuthorizationHeader(self, user=PloneTestCase.portal_owner, password=PloneTestCase.default_password):
        """ add an authorization header using the given or default credentials """
        self.addHeader('Authorization', 'Basic %s:%s' % (user, password))


