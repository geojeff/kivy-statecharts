from setuptools import setup, find_packages
import os

version = '0.1'

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    TODO = open(os.path.join(here, 'TODO.txt')).read()
except IOError:
    TODO = ''
try:
    AUTHORS = open(os.path.join(here, 'AUTHORS.txt')).read()
except IOError:
    AUTHORS = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    CHANGES = ''

development_requires = [
]
tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'pytest-xdist',
]

long_description = README + '\n\n' + TODO + '\n\n' + AUTHORS + '\n\n' + CHANGES

setup(name='kivy_statecharts',
      version=version,
      description="Kivy Statecharts -- adds a statechart system to kivy",
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Artistic Software',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: User Interfaces',
      ],
      keywords='kivy statecharts',
      author='Jeff Pittman',
      author_email='geojeff@geojeff.org',
      url='http://github.com/geojeff/kivy_statecharts',
      bugtrack_url='https://github.com/geojeff/kivy_statecharts/issues',
      license=' MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Kivy>=1.4.1',
      ],
      tests_require=tests_require,
      extras_require={
          'testing': tests_require,
          'development': development_requires,
          },
      )
