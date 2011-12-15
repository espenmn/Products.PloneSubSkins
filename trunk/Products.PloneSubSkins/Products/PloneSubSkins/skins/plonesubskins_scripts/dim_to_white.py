## Script (Python) "get_base_properties"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=color, percent
##title=
##
return context.restrictedTraverse('dim_to').white(color, percent)
