from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='mytop',
      version='0.0.2',
      description='mytop',
      #long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='mytop',
      url='https://github.com/flyingcoconut/mytop',
      author='Patrick Charron',
      author_email='patrick.charron.pc@gmail.com',
      license='GPL v3',
      packages=['mytop', 'mytop/drivers'],
      install_requires=[
      ],
      #scripts=['bin/mytop'],
      include_package_data=True,
      zip_safe=False)
