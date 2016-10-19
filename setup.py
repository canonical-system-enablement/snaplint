from distutils.core import setup

setup(name='snaplint',
      version='0.1',
      description='Clean up your snap',
      author='Scott Sweeny',
      author_email='scott.sweeny@canonical.com',
      scripts=['bin/snaplint'],
      packages=['snaplint',
                'snaplint.rules']
     )
