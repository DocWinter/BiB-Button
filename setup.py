from setuptools import setup

setup(
    name='BIBButton',
    version='0.0.1',
    author='Thomas Sauze',
    author_email='thomas.sauze@seasonlabs.com',
    description='Buttton script for the BiB\'s opening.',
    license='MIT',
    keyword='bib, button, script',
    packages=['bibbutton'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'TwitterAPI'
    ]
)
