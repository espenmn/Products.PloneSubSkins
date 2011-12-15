import unittest
import StringIO
from base import Browser
from base import IntegrationTestCase

class ControlPanelAnonymousTest(IntegrationTestCase):
    def test_anonymous_cannot_change_styles(self):
        browser = Browser()
        controlpanel_url = self.portal.absolute_url() + '/portal_subskinstool/subskins_control_panel'
        browser.open(controlpanel_url)
        self.failIfEqual(browser.url,controlpanel_url)
    def test_tool_anonymous_can_view(self):
        browser = Browser()
        browser.handleErrors= False
        css_url = self.portal.absolute_url() + '/base_test.css'
        browser.open(css_url)
        #self.failUnlessEqual(css_url, browser.url)

class ControlPanelTest(IntegrationTestCase):
    def setUp(self):
        super(ControlPanelTest, self).setUp()
        self.browser = Browser()
        self.browser.addAuthorizationHeader()
        self.controlpanel_url = self.portal.absolute_url() + '/portal_subskinstool'
        self.browser.open(self.controlpanel_url)
    def test_tool_admin_can_view(self):
        self.failUnlessEqual(self.browser.url,self.controlpanel_url)
    def test_save_widths(self):
        self.browser.getControl(name='subskinswidth1').value='100px'
        self.browser.getControl(name='subskinswidth2').value='100px'
        self.browser.getControl(name='subskinswidth3').value='100px'
        self.browser.getControl("Save").click()
        tool = self.portal.portal_subskinstool
        self.failUnless(tool.SubSkinsWidth1)
        self.failUnless(tool.SubSkinsWidth2)
        self.failUnless(tool.SubSkinsWidth3)
    def test_choice_with_titles_for_css(self):
        top_choice = self.browser.getControl(name="top_choice")
        top_choice.value = ['top_test.css']
        self.failUnlessEqual(top_choice.displayValue[0], 
                             "A test css file for PloneSubSkins")
    def test_choice_with_titles_for_colorschemes(self):
        colorschemes_choice = self.browser.getControl(name="colorschemes_choice")
        colorschemes_choice.value = ['colors_test']
        self.failUnlessEqual(colorschemes_choice.displayValue[0], 
                             "SubSkins test colorscheme")
    def test_choices_sorted_by_titles(self):
        "We want choices to be sorted in alphabetical order by title"
        for choice_name in ['top_choice', 'base_choice', 'colorschemes_choice']:
            choice = self.browser.getControl(name=choice_name)
            # the first item will be "None"
            self.failUnlessEqual(sorted(choice.displayOptions[1:]), 
                                 choice.displayOptions[1:])
    def test_choice(self):
        top_choice = self.browser.getControl(name="top_choice")
        top_options = top_choice.options
        self.assertTrue('top_test.css' in top_options)
        top_choice.value = ['top_test.css']
        extra_choice = self.browser.getControl(name="extra_choice")
        self.failUnless('some_extra.css' in extra_choice.options)
        extra_choice.value = ['more_extra.css']
        self.browser.getControl("Save").click()
        self.failUnless(self.is_css_enabled('top_test.css'))
        self.failUnless(self.is_css_enabled('more_extra.css'))
        self.failIf(self.is_css_enabled('some_extra.css'))
        extra_choice = self.browser.getControl(name="extra_choice")
        extra_choice.value = ['more_extra.css', 'some_extra.css']
        self.browser.getControl("Save").click()
        self.failUnless(self.is_css_enabled('more_extra.css'))
        self.failUnless(self.is_css_enabled('some_extra.css'))
        current_value = self.browser.getControl(name="extra_choice").value
        self.failUnlessEqual(sorted(current_value),
                             ['more_extra.css', 'some_extra.css'])
    def test_colorscheme(self):
        self.browser.open(self.css_url + "/top_test.css")
        self.failUnless('#00ff44' in self.browser.contents)
    def test_colorscheme_not_registered_in_portal_css(self):
        colorschemes_choice = self.browser.getControl(name="colorschemes_choice")
        colorschemes_choice.value = ['colors_test']
        self.browser.getControl("Save").click()
        css_tool = self.portal.portal_css
        self.failIf('colors2_test' in css_tool.getResourceIds(),
                    "The color scheme should not be registered in portal_css")
    def test_colorscheme_choice(self):
        colorscheme_choice = self.browser.getControl(name="colorschemes_choice")
        colorscheme_choice_options = colorscheme_choice.options
        self.assertTrue('colors2_test' in colorscheme_choice_options)
        colorscheme_choice.value = ['colors2_test']
        self.browser.getControl("Save").click()
        self.browser.open(self.css_url + "/top_test.css")
        self.failUnless('#abdd44' in self.browser.contents)
    def test_colorscheme_on_the_fly_change(self):
        self.browser.open(self.css_url + "/top_test.css?colorscheme=colors2_test")
        self.failUnless('#abdd44' in self.browser.contents)
    def test_change_logo(self):
        myPhoto = StringIO.StringIO('my logo')
        file_control = self.browser.getControl(name='newlogo').mech_control
        file_control.add_file(myPhoto, filename='myPhoto.gif')
        self.browser.getControl('Update').click()
        custom = self.portal.portal_skins.custom
        self.failUnless('logo_medialog.png' in custom.objectIds())
        image_url = custom['logo_medialog.png'].absolute_url()
        self.browser.open(image_url)
        self.failUnlessEqual('my logo', self.browser.contents)

def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(ControlPanelTest),
            unittest.makeSuite(ControlPanelAnonymousTest),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

