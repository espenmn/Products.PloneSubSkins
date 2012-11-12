from cStringIO import StringIO
from PIL import Image
from PIL import ImageOps
from PIL.PngImagePlugin import PngImageFile
from PIL.ImageColor import getrgb
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.interface import Interface

class subskins_get_base_properties(BrowserView):
    def __call__(self):
        tool = getToolByName(self, 'portal_subskinstool')
        #next line is a workaround for a theme without dtml
        sheetname=SubSkinsColors-igly
        if self.REQUEST.get('colorscheme'):
            sheetname = self.REQUEST.get('colorscheme')
        else:
            sheetname = tool.getProperty('colorschemes')
        result = dict(getattr(self, sheetname).propertyItems())
        for propname in ['SubSkinsWidth1', 'SubSkinsWidth2', 'SubSkinsWidth3', 'SubSkinsCSS']:
            result[propname] = getattr(self, propname)
        return result
 
class ChoiceForm(BrowserView):
    @property
    def tool_url(self):
        return self.tool.absolute_url()
    @property
    def tool(self):
        return getToolByName(self.context, 'portal_subskinstool')
    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()
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

class UpdateLogo(BrowserView):
    def __call__(self):
        logo_id='logo_medialog.png'
        submit_upload=self.request.get('submit_upload')
        skintool=getToolByName(self, 'portal_skins')
        if submit_upload:
            f=self.request.get("newlogo")
            if logo_id in skintool.custom.objectIds():
                skintool.custom.manage_delObjects(logo_id)
            skintool.custom.manage_addImage(logo_id, f.read())
        else:
            if logo_id in skintool.custom.objectIds():
                skintool.custom.manage_delObjects(logo_id)
        self.request.RESPONSE.redirect(
            self.context.portal_url()+'/portal_subskinstool/subskins_control_panel')

class ColorizedImage(BrowserView):
    "Use this view as follows: /subskins_getimage/aaa/logo_medialog.png"
    def __bobo_traverse__(self, REQUEST, name):
        if not hasattr(self, 'color'):
            getrgb(name) # as a side effect it validates or throws an exception
            self.color = name
            self.__doc__ = "An accessible traversable view" # Make the Zope publisher happy
            return self
        elif not hasattr(self, 'filename'):
            self.filename = name
            self.__doc__ = "An accessible traversable view"
            return self
        else:
            raise AttributeError
    def __call__(self):
        portal_skins = getToolByName(self.context, 'portal_skins')
        if not hasattr(self, 'filename'):
            self.filename = self.request.img
        if not hasattr(self, 'color'):
            self.color = self.request.color
        color = self.color
        img = portal_skins.restrictedTraverse(self.filename)
        img_data = getattr(img, '_data', False) or getattr(img, 'data', False)
        image = Image.open(StringIO(img_data))
        alpha = None
        if image.mode == 'RGBA':
            alpha = image.split()[3]
        elif image.mode == 'P' and image.format == 'PNG':
            # PNG images can have transparency and be palette-based.
            # This is probably not the most clever method but it works
            alpha = image.convert('RGBA').split()[3]
        r,g,b = getrgb(color)
        if image.mode != 'L':
            grayscale_image = image.convert('L')
        else:
            grayscale_image = image
        newimage = ImageOps.colorize(grayscale_image, (r,g,b),(255,255,255))
        output = StringIO()
        if alpha:
            newimage.putalpha(alpha)
        newimage.save(output, format='PNG')
        self.request.response.setHeader('Content-Type','image/png')
        return output.getvalue()


class ColorDimTo(BrowserView):
    def black(self, colorstring, percent):
        factor = int(percent)/100.0
        r,g,b = getrgb(colorstring)
        colors = map(lambda x: int((x+1)*factor), (r,g,b) )
        return get_colorstring(*colors)
    def white(self, colorstring, percent):
        factor = (100-int(percent))/100.0
        r,g,b = getrgb(colorstring)
        colors = map(lambda x: int(256 - (255-x+1)*factor), (r,g,b) )
        return get_colorstring(*colors)

def get_colorstring(r,g,b):
    colors = map(lambda x:hex(x)[2:], (r,g,b))
    for i in range(3):
        if len(colors[i])<2:
            colors[i] = '0' + colors[i]
    return '#' + ''.join(colors)
    
    
