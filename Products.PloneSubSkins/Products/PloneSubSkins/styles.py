from Products.ResourceRegistries.browser.styles import StylesView as StylesViewBase
from Products.CMFCore.utils import getToolByName


class StylesView(StylesViewBase):
    def styles(self):
        cssregistry = self.registry()
        oldDebugMode = cssregistry.getDebugMode() 
        cssregistry.setDebugMode(True)
        result = super(StylesView, self).styles()
        cssregistry.setDebugMode(oldDebugMode)
        tool = getToolByName(self.context, 'portal_subskinstool')
        colorscheme = tool.getProperty('colorschemes')
        for sheet in result:
            if sheet['rendering'] == 'import':
                sheet['src'] = sheet['src'].replace('.css', '.css?colorscheme=' + colorscheme)
        return result
