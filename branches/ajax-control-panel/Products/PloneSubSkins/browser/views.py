from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface

class ChoiceForm(BrowserView):
    @property
    def tool_url(self):
        return self.tool.absolute_url()
    @property
    def tool(self):
        return getToolByName(self.context, 'portal_subskinstool')
    def portal_url(self):
        return self.context.aq_inner.aq_parent.absolute_url()
    @property
    def detatched(self):
        return self.request.get('detatched')

class CssDebugModeControl(BrowserView):
    def __call__(self):
        """ Used by Javascript with ajax
            If either disable or enable parameters are in the request
            debug mode will be enabled/disabled
        """
        if self.request.get('enable'):
            self.enable()
        if self.request.get('disable'):
            self.disable()
        return self.isEnabled() and 'true' or 'false'
    def __init__(self, *args, **kwargs):
        super(CssDebugModeControl, self).__init__(*args, **kwargs)
        self.tool =  getToolByName(self.context, 'portal_css')
    def isEnabled(self):
        return self.tool.getDebugMode()
    def enable(self):
        self.tool.setDebugMode(True)
    def disable(self):
        self.tool.setDebugMode(False)


class ICssDebugModeControl(Interface):
    def isEnabled(self):
        " Checks if the css tool is in debug mode "
    def enable(self):
        "enables the css debug mode on the portal"
    def disable(self):
        "disables the css debug mode on the portal"

