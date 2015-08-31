from setuptools import find_packages, setup


setup(
    name='groceries-cli',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==5.1',
        'coverage==3.7.1',
        'coveralls==0.5',
        'flake8==2.4.1',
        'mock==1.3.0',
        'pytest==2.7.2',
        'pyyaml==3.11',
        'requests==2.7.0',
    ],
    entry_points='''
        [console_scripts]
        groceries=groceries.core:cli
    ''',
)
