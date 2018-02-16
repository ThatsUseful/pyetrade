#!/usr/bin/env python3

from distutils.core import setup

# requirements
with open('requirements.txt') as requirements:
    req = [i.strip() for i in requirements]

setup(name='pyetrade',
      version='0.8.0',
      description='eTrade API wrappers',
      author='Jesse Cooper, Scott Rutherford',
      author_email='jesse_cooper@codeholics.com, scott@thatsuseful.com',
      url='https://github.com/thatsuseful/pyetrade',
      license='GPLv3',
      packages=['tu-pyetrade'],
      package_dir={'tu-pyetrade':'tu-pyetrade'},
      install_requires=req,
      platforms=['any'],
      keywords=['etrade', 'pyetrade', 'stocks'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Financial and Insurance Industry',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries'
          ]
     )
