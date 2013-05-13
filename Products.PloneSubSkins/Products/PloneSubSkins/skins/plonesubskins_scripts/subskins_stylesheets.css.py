## Script (Python) "the_stylesheets.css"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Rendered subskins CSS for extracting css to use it with a new theme
##
portal_css = context.portal_css
stylesheets = portal_css.getEvaluatedResources(context)

for stylesheet in stylesheets:
    if stylesheet.getBundle() =='subskins':
        print portal_css.getInlineResource(stylesheet.getId(), context)

duration = 1
seconds = float(duration) * 24.0 * 3600.0
response = context.REQUEST.RESPONSE
#response.setHeader('Expires',rfc1123_date((DateTime() + duration).timeTime()))
response.setHeader('Cache-Control', 'max-age=%d' % int(seconds))
response.setHeader('Content-Type', 'text/css')

return printed
