from setuptools import setup, find_packages

readme = open('README.rst')

setup(name="githubscraper",
      version="dev",
      packages=find_packages(),
      namespace_packages=['githubscraper'],
      include_package_data=True,
      author='Dan Colish',
      author_email='dcolish@gmail.com',
      description='',
      long_description=readme.read(),
      zip_safe=False,
      platforms='any',
      license='BSD',
      url='http://www.github.com/dcolish/github-scraper',

      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        ],

      entry_points={
        'console_scripts': [
            'makegraph=githubscraper.graph:main',
            ],
        },

      install_requires=[
        'numpy',
        'matplotlib',
        'pygraphviz',
        'networkx',
        'couchdb',
        ],
      )

readme.close()
