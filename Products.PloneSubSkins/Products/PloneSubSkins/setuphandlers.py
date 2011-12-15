# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2008 by Espen MOE-NILSSEN / Eric BREHAULT
# Generator: ArchGenXML Version 2.0-beta11
#            http://plone.org/products/archgenxml
#
# Zope Public License (ZPL)
#

__author__ = """Eric BREHAULT <ebrehault@gmail.com>, Silvio Tomatis <silviot@gmail.com>"""
__docformat__ = 'plaintext'


from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
#from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles
import logging
import os

logger = logging.getLogger('PloneSubSkins: setuphandlers')


def setupHideToolsFromNavigation(context):
    """hide tools"""
    # uncatalog tools
    #shortContext = context._profile_path.split('/')[-3]
    #Changed the above line ( http://plone.org/products/subskins/issues/12 )
    shortContext = context._profile_path.split(os.sep)[-3]
    if shortContext != 'PloneSubSkins': # avoid infinite recursions
        return
    site = context.getSite()
    toolnames = ['portal_subskinstool']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""

    site = context.getSite()
    #shortContext = context._profile_path.split('/')[-3]
    #Changed the above line ( http://plone.org/products/subskins/issues/12 )
    shortContext = context._profile_path.split(os.sep)[-3]
    if shortContext != 'PloneSubSkins': # avoid infinite recursions
        return
    wft = getToolByName(site, 'portal_workflow')
    wft.updateRoleMappings()
    site.portal_subskinstool.manage_permission(
        'Access contents information', acquire=1)

def upgrade_from_unknown(context):
    #site = context.getSite()
    QI = getToolByName(context, 'portal_subskinstool')
    #QI.reinstallProducts(('PloneSubSkins'))
    try:
        QI.manage_addProperty(id='SubSkinsCSS', value='', type='string')
    except:
        pass
    try:
        QI.manage_addProperty(id='brosho', value=False, type='boolean')
    except:
        pass
    
    try:
        QI.manage_addProperty(id='extra', value=False, type='string')
    except:
        pass
    
def ensure_all_options_are_set(context):
    datafile = context.openDataFile('subskins_choices.xml')
    if not datafile:
        return
    tool = getToolByName(context.getSite(), 'portal_subskinstool')
    categories = tool.getStylesheetCategories()
    categories += ({'id':'colorschemes'},)
    for category in categories:
        if not getattr(tool, category['id']) and category['id'] != 'extra':
            possible_choices = tool.getAvailableChoices(category['id'])
            if possible_choices:
                chosen_value = possible_choices[0]['id']
                tool.set_choice(category['id'], chosen_value)
    cssregistry=getToolByName(context.getSite(), 'portal_css')
    cssregistry.cookResources()
