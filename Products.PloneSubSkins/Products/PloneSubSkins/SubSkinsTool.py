# -*- coding: utf-8 -*-
#
# File: SubSkinsTool.py
#
# Copyright (c) 2008 by Espen MOE-NILSSEN / Eric BREHAULT
# Generator: ArchGenXML Version 2.0-beta11
#            http://plone.org/products/archgenxml
#
# Zope Public License (ZPL)
#

__author__ = """Eric BREHAULT <ebrehault@gmail.com>, Silvio Tomatis <silviot@gmail.com>, Espen Moe-Nilssen <espen@medialog.no>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFCore.utils import SimpleItemWithProperties
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.PloneSubSkins.config import *


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
from Products.CMFCore.permissions import ManagePortal
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SubSkinsTool_schema = BaseSchema.copy() + \
    getattr(SimpleItemWithProperties, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section after-schema

class SubSkinsTool(UniqueObject, BaseContent, SimpleItemWithProperties, BrowserDefaultMixin):
    "A persistent tool to hold configuration of chosen stylesheets"
    security = ClassSecurityInfo()
    implements(interfaces.ISubSkinsTool)

    meta_type = 'SubSkinsTool'
    _at_rename_after_creation = True

    schema = SubSkinsTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_subskinstool')
        self.setTitle('')
        
        ##code-section constructor-footer #fill in your manual code here
        for c in sub_skins_categories:
            self._setProperty(c['id'], '', 'string')
            
        self._setProperty('colorschemes', '', 'string')
        self._setProperty('SubSkinsWidth1', '880px', 'string')
        self._setProperty('SubSkinsWidth2', '150px', 'string')
        self._setProperty('SubSkinsWidth3', '150px', 'string')
        self._setProperty('SubSkinsCSS', '', 'string')
        self._setProperty('brosho', 0, 'boolean')


        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declareProtected(ManagePortal, 'getAvailableChoices')
    def getAvailableChoices(self,category):
        """
        """
        skintool=getToolByName(self, 'portal_skins')
        defaultskinname=skintool.getDefaultSkin()
        if hasattr(skintool, defaultskinname+'_'+category):
            choices = getattr(skintool, defaultskinname+'_'+category).objectValues()
            choices_dicts = [dict(title=(c.title or c.id), id=c.id) for c in choices]
            return sorted(choices_dicts, key=lambda c: c['title'])
        else:
            return ()

    def set_choice(self, category_id, choices):
        # store current choice
        if self.hasProperty(category_id):
            self._updateProperty(category_id, choices)
        # in case of the colorschemes category we're done
        if category_id == 'colorschemes':
            return
        if not isinstance(choices, list):
            choices = [choices] # always handle lists for simplicity later
        skintool=getToolByName(self, 'portal_skins')
        cssregistry=getToolByName(self, 'portal_css')
        defaultskinname=skintool.getDefaultSkin()
        category=getattr(skintool, defaultskinname+'_'+category_id, None)
        # remove all stylesheet from the category
        for s in category.objectIds():
            if s not in choices:
                cssregistry.unregisterResource(s)
        # enable according to user choice
        for choice in choices:
            if choice and hasattr(category, choice):
                self.registerStylesheet(dict(id=choice))

    security.declareProtected(ManagePortal, 'saveStylesheetChoices')
    def saveStylesheetChoices(self,REQUEST):
        """
        """
        skintool=getToolByName(self, 'portal_skins')
        cssregistry=getToolByName(self, 'portal_css')
        defaultskinname=skintool.getDefaultSkin()
        for c in sub_skins_categories:
            category=getattr(skintool, defaultskinname+'_'+c['id'], None)
            if category:
                choice=REQUEST.get(c['id']+'_choice')
                self.set_choice(c['id'], choice)
        
        # store color schemes choice
        choice=REQUEST.get('colorschemes_choice')
        self._updateProperty('colorschemes', choice)

        # store widths and extra css
        for propname in ['SubSkinsWidth1', 'SubSkinsWidth2', 'SubSkinsWidth3', 'SubSkinsCSS']:
            choice=REQUEST.get(propname.lower(), '')
            if choice:   
                self._updateProperty(propname, choice)

        # store brosho setting
        for propname in ['brosho']:
            choice=REQUEST.get(propname.lower(), '')
            if choice:   
                self._updateProperty(propname, choice)
            else:
                self._updateProperty(propname, 0)

        if REQUEST.get('came_from'):
            REQUEST.RESPONSE.redirect(REQUEST.get('came_from'))
        else:
            REQUEST.RESPONSE.redirect(self.portal_url()+'/portal_subskinstool/subskins_control_panel')
        cssregistry.cookResources()


    security.declareProtected(ManagePortal, 'getStylesheetCategories')
    def getStylesheetCategories(self):
        """
        """
        return sub_skins_categories
    
    security.declarePublic('getBaseProperties')
    def getBaseProperties(self):
        #next line is a workaround for a theme without dtml
        sheetname='SubSkinsColors-igly'
        if self.REQUEST.get('colorscheme'):
            sheetname = self.REQUEST.get('colorscheme')
        else:
            sheetname = self.getProperty('colorschemes')
        result = dict(getattr(self, sheetname).propertyItems())
        for propname in ['SubSkinsWidth1', 'SubSkinsWidth2', 'SubSkinsWidth3', 'SubSkinsCSS']:
            result[propname] = getattr(self, propname)
        return result
               
    security.declarePublic('getFolderBaseProperties')
    def getFolderBaseProperties(self):
        context=self.context
        if self.REQUEST.get('colorscheme'):
            sheetname = self.REQUEST.get('colorscheme')
        else:
            sheetname = self.getProperty('colorschemes')
        result = dict(getattr(self, sheetname).propertyItems())
        for propname in ['SubSkinsWidth1', 'SubSkinsWidth2', 'SubSkinsWidth3', 'SubSkinsCSS']:
            result[propname] = getattr(self, propname)
        
        #now we will check if this item has other colours set
        #try:
        #    localsheet = dict(context.colorschemes.propertyItems())
        #    result.update(localsheet)
        #finally:
        #    pass
            
        myresult = dict()
        for propname in ['SubSkinsColor1', 'SubSkinsColor2','SubSkinsColor3','SubSkinsColor4','SubSkinsColor5','SubSkinsColor6','SubSkinsWidth1', 'SubSkinsWidth2', 'SubSkinsWidth3',]:
            try: 
                myresult[propname] = getattr(context, propname)
            except AttributeError:  
                pass
            
        result.update(myresult)        
               
        return result

    security.declareProtected(ManagePortal, 'registerStylesheet')
    def registerStylesheet(self, resource):
        tool = getToolByName(self, 'portal_css')
        existing = tool.getResourceIds()
        resource_default = {'media': 'screen', 'rendering': 'import',
                            'enabled': True}
        resource_default.update(resource)
        resource = resource_default
        if not resource['id'] in existing:
            tool.registerStylesheet(**resource)

    security.declareProtected(ManagePortal, 'listColors')
    def listColors(self):
        skintool=getToolByName(self, 'portal_skins')
        defaultskinname=skintool.getDefaultSkin()
        result=[]
        if hasattr(skintool, defaultskinname+'_colorschemes'):
            for bp in getattr(skintool, defaultskinname+'_colorschemes').getChildNodes():
                name=bp.id
                colors=[]
                if hasattr(bp, 'propertyIds'):
                    #check if 'custom' version exists
                    if hasattr(skintool.custom, name):
                        bp=getattr(skintool.custom, name)
                    for p in bp.propertyIds():
                        if 'color' in p.lower() or '#' in bp.getProperty(p):
                            colors.append(bp.getProperty(p))
                    result.append([name, colors])
        return result

    # The following, borrowed from Products.CacheSetup, avoids the tool to be
    # catalogued
    isReferenceable = None
    def _register(self, *args, **kwargs): pass
    def _updateCatalog(self, *args, **kwargs): pass
    def _referenceApply(self, *args, **kwargs): pass
    def indexObject(self, *args, **kwargs): pass
    def reindexObject(self, *args, **kwargs): pass

registerType(SubSkinsTool, PROJECTNAME)
# end of class SubSkinsTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer


