This product provides a control panel to be used by subskins, a Plone product that
provides many css and color schemes to customize the site layout.
Together, the two allow quick and easy customization of the Plone skin.
If you want this functionality, you should install medealog.subskins.
It will pull this product as a dependency.
If you want to write a product similar to subskins read ahead.

PloneSubSkins allows to switch to specific CSS files handling such or such aspects of your Plone skin.

By default, this hacked version of PloneSubSkins manage the following categories:
- Base
- Top
- Navigation
- Text
- Global navigation
- Portlets
- Bottom
- Extra (multiple choices)

Another category is dedicated to manage your different base_properties files, named MySkin_colorschemes.

To use PloneSubSkin you just need to respect the following naming convention:
1 - if your skin product is named MySkin, the navigation-related CSS must be stored in a sub-folder named MySkin_navigation,
text related CCS must be in MySkin_text, etc.

It will produce the following directory structure:
/Products
	/MySkin
		/skins
			/MySkin
				main_template.pt
				some.gif
				other.pt
				/MySkin_colorschemes
					bluetheme_base_properties.prop
					yellowtheme_base_properties.prop
				/MySkin_navigation
					navYellow.css
					navYellow2.css
				/MySkin_text
					small.css
					normal.css
					all_arial.css
				/MySkin_globalnav
					globalnav.css
					globalnavOld.css
				/MySkin_calendar
					cal1.css
					cal2.css		
etc.

2 - In your css files, add the following line:
<dtml-with get_base_properties mapping>
before the existing line:
<dtml-with base_properties> (do not remove this)
and add the line
/* </dtml-with> */
at the end of the file

3 - Depend on this product in your metadata.xml
4 - Put a file named subskins_choices.xml in your profile directory

You can modify those categories or add your own ones by editing /Products/PloneSubSkins/AppConfig.py


