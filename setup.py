from distutils.core import setup

setup(
    name='pelican-events',
    version='0.8',
    packages=['events'],
    url='https://github.com/rackerlabs/pelican-events',
    license='AGPL',
    author='Bill Anderson',
    author_email='bill.anderson@rackspace.com',
    description='A pelican events plugin',
    install_requires = ['pelican',]
)
