## Script (Python) "get_base_properties"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

thescheme = context.restrictedTraverse('@@subskins_get_base_properties')()

#comment out the lines below for foldersubskins thanks to moo-_- for help with hasattr

#for name in ['SubSkinsColor1', 'SubSkinsColor2', 'SubSkinsColor3', 'SubSkinsColor4', 'SubSkinsColor5', 'SubSkinsColor6', 'SubSkinsWidth1', 'SubSkinsWidth2', 'SubSkinsWidth3']:
#    if hasattr(context, name):
#        valor = getattr(context, name)
#        x = {name: valor }
#        thescheme.update(x)

return thescheme

