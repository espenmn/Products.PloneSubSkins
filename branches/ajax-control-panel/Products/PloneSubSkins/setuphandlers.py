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

__author__ = """Eric BREHAULT <ebrehault@gmail.com>"""
__docformat__ = 'plaintext'


from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger('PloneSubSkins: setuphandlers')


def setupHideToolsFromNavigation(context):
    """hide tools"""
    # uncatalog tools
    shortContext = context._profile_path.split('/')[-3]
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

    shortContext = context._profile_path.split('/')[-3]
    if shortContext != 'PloneSubSkins': # avoid infinite recursions
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def upgrade_from_unknown(context):
    QI = getToolByName(context, 'portal_quickinstaller')
    QI.reinstallProducts(('PloneSubSkins'))
