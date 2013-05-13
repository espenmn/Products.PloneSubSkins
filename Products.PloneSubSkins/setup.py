from setuptools import setup, find_packages
import os

version = '4.7.5'

setup(name='Products.PloneSubSkins',
      version=version,
      description="Manage Plone skins CSS, logo, and base colors dynamically from the Plone control panel",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone skin skinning customization',
      author='Eric BREHAULT',
      author_email='eric.brehault@makina-corpus.org',
      url='http://plone.org/products/subskins',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'medialog.subskins'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
