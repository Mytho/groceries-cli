from setuptools import setup


setup(
    name='groceries-cli',
    version='0.0.1',
    py_modules=['groceries'],
    install_requires=[
        'click==5.1',
        'flake8==2.4.1',
        'pyyaml==3.11',
        'requests==2.7.0',
    ],
    entry_points='''
        [console_scripts]
        groceries=groceries.core:cli
    ''',
)
