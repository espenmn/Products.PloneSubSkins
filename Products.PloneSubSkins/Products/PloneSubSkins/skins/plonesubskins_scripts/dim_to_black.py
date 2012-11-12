## Script (Python) "dim_to_black"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=color, percent
##title=
##
return context.restrictedTraverse('dim_to').black(color, percent)
