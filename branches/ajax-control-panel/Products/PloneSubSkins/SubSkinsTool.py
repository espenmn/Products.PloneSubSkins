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

__author__ = """Eric BREHAULT <ebrehault@gmail.com>"""
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
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declareProtected(ManagePortal, 'getAvailableStyleSheets')
    def getAvailableStyleSheets(self,category):
        """
        """
        self.updateAvailableStyleSheets()
        skintool=getToolByName(self, 'portal_skins')
        defaultskinname=skintool.getDefaultSkin()
        if hasattr(skintool, defaultskinname+'_'+category):
            return getattr(skintool, defaultskinname+'_'+category).objectIds()
        else:
            return ()

    security.declareProtected(ManagePortal, 'saveStylesheetChoices')
    def saveStylesheetChoices(self,REQUEST):
        """
        """
        skintool=getToolByName(self, 'portal_skins')
        cssregistry=getToolByName(self, 'portal_css')
        defaultskinname=skintool.getDefaultSkin()
        for c in sub_skins_categories:
            if hasattr(skintool, defaultskinname+'_'+c['id']):
                # disable all stylesheet from the category
                category=getattr(skintool, defaultskinname+'_'+c['id'])
                for s in category.objectIds():
                    stylesheet = cssregistry.getResourcesDict().get(s, None)
                    if stylesheet is not None:
                        stylesheet.setEnabled(False)
                    
                # enable according user choice
                choice=REQUEST.get(c['id']+'_choice')
                if hasattr(category, choice):
                    stylesheet = cssregistry.getResourcesDict().get(choice, None)
                    if stylesheet is not None:
                        stylesheet.setEnabled(True)
                
                # refresh CSS registry
                resources = [r.copy() for r in cssregistry.getResources()]
                cssregistry.resources=tuple(resources)
                cssregistry.cookResources()
                
                # store current choice
                if self.hasProperty(c['id']):
                    self._updateProperty(c['id'], choice)
                    
        # store color schemes choice
        choice=REQUEST.get('colorschemes_choice')
        self._updateProperty('colorschemes', choice)
    
        if REQUEST.get('came_from'):
            REQUEST.RESPONSE.redirect(REQUEST.get('came_from'))
        else:
            REQUEST.RESPONSE.redirect(self.portal_url()+'/portal_subskinstool/subskins_control_panel')

    security.declareProtected(ManagePortal, 'getStylesheetCategories')
    def getStylesheetCategories(self):
        """
        """
        return sub_skins_categories
    
    security.declarePublic('getBaseProperties')
    def getBaseProperties(self):
        if self.REQUEST.get('colorscheme'):
            sheetname = self.REQUEST.get('colorscheme')
        else:
            sheetname = self.getProperty('colorschemes')
        return getattr(self, sheetname)
    
    security.declareProtected(ManagePortal, 'getAvailableColorSchemes')
    def getAvailableColorSchemes(self):
        skintool=getToolByName(self, 'portal_skins')
        defaultskinname=skintool.getDefaultSkin()
        if hasattr(skintool, defaultskinname+'_colorschemes'):
            return getattr(skintool, defaultskinname+'_colorschemes').objectIds()
        else:
            return ()
            
    security.declareProtected(ManagePortal, 'updateAvailableStyleSheets')
    def updateAvailableStyleSheets(self):
        skintool=getToolByName(self, 'portal_skins')
        defaultskinname=skintool.getDefaultSkin()
        ressources=[]
        for c in skintool.objectIds():
            if c.startswith(defaultskinname):
                skindir=getattr(skintool,c)
                for s in skindir.objectIds():
                    if s.endswith('.css'):
                        ressources.append({'id': s, 'media': 'screen', 'rendering': 'import', 'enabled': False})
        self.registerStylesheet(ressources)
    
    security.declareProtected(ManagePortal, 'updateAvailableStyleSheets')
    def registerStylesheet(self, resources):
        tool = getToolByName(self, 'portal_css')
        existing = tool.getResourceIds()
        for resource in resources:
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

    security.declareProtected(ManagePortal, 'updateLogo')
    def updateLogo(self, REQUEST):
        logo_id='logo.jpg'
        submit_upload=REQUEST.get('submit_upload')
        skintool=getToolByName(self, 'portal_skins')
        if submit_upload:
            f=REQUEST.get("newlogo")
            if logo_id in skintool.custom.objectIds():
                skintool.custom.manage_delObjects(logo_id)
            skintool.custom.manage_addImage(logo_id, f.read())
        else:
            if logo_id in skintool.custom.objectIds():
                skintool.custom.manage_delObjects(logo_id)
        REQUEST.RESPONSE.redirect(self.portal_url()+'/portal_subskinstool/subskins_control_panel')
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



