from setuptools import setup

setup(
    name='pelican-events',
    version='0.8',
    packages=['pelican_events'],
    url='https://github.com/rackerlabs/pelican-events',
    license='Apache 2.0',
    author='Bill Anderson',
    author_email='bill.anderson@rackspace.com',
    description='A pelican events plugin',
    install_requires = ['pelican','six']
)
