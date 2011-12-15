import Lifetime
import tempfile
import unittest
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneSubSkins.tests.base import IntegrationTestCase
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.layer import PloneSite
from random import choice
from Testing.ZopeTestCase.utils import startZServer
from zope.testing.testrunner.runner import Runner
import os

ptc.setupPloneSite(products=['medialog.subskinsiii'])

@onsetup
def setup_product():
        fiveconfigure.debug_mode = True
        import medialog.subskinsiii 
        zcml.load_config('configure.zcml',
                         medialog.subskinsiii)
        fiveconfigure.debug_mode = False
setup_product()

class ZopeServerLayer(PloneSite):
    "Code borrowed from collective.ploneseltest"
    _site = 'plone'
    @classmethod
    def setUp(cls):
        """Start the ZServer thread
        """
        # Start the Zope server with five threads
        host, port = startZServer(5)
        cls.url = "http://%s:%s/%s" % (host, port, cls._site)
    @classmethod
    def tearDown(cls):
        """Stop the the ZServer thread
        """
        Lifetime.shutdown(0, fast=1)

class ComputeImages(IntegrationTestCase):
    layer = ZopeServerLayer
    def setUp(self):
        super(ComputeImages, self).setUp()
        self.portal.portal_quickinstaller.installProduct('medialog.subskinsiii')
    def test_compute_images(self):
        tool = self.portal.portal_subskinstool
        colorschemes = tool.getAvailableColorSchemes()
        stylesheets = {}
        categories = [catdict['id'] for catdict in tool.getStylesheetCategories()]
        destination_dir = '/tmp/subPreviews'
        if not os.path.isdir(destination_dir):
            os.mkdir(destination_dir)
        url= self.layer.url
        for category in categories:
            stylesheets[category] =  tool.getAvailableStyleSheets(category)

        self.portal['front-page'].setText(self.portal['front-page'].getText()[:3000])
        possible_skins = reduce(lambda x,y:x*y,[len(a) for a in stylesheets] +
                                [len(colorschemes)]) # That is 81285120 as I write this!
        for i in range(200):
            REQUEST = DummyRequest()
            REQUEST.update({
                'colorschemes_choice':choice(colorschemes),
            })
            for category in categories:
                REQUEST[category + '_choice'] = choice(stylesheets[category])
            tool.saveStylesheetChoices(REQUEST)
            pdfFile = tempfile.mktemp('.pdf')
            os.system("wkhtmltopdf --orientation Landscape %s %s" % (url, pdfFile))
            destination = os.path.join(destination_dir,os.path.basename(tempfile.mktemp('.png')))
            os.system("convert %s %s" % (pdfFile, destination))
            os.unlink(pdfFile)

        pass
        a = 1

class DummyRequest(dict):
    class DummyResponse:
        def redirect(self,url):
            pass
    RESPONSE = DummyResponse() 




def run_script():
    compute_images = unittest.TestSuite([unittest.makeSuite(ComputeImages)])
    Runner(found_suites=compute_images).run()



"""
The above approach has many limits (it's cumbersome and it doesn't allow to clip
the png to a dom element).
This is the PyQt approach:

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl("http://plone.org"))
web.show()

time.sleep(1)

painter = QPainter()
image = QImage(200,200,QImage.Format_ARGB32)
painter.begin(image)
web.render(painter)
painter.end()
image.save('/tmp/uuu.png' )
"""
