from setuptools import setup


setup(
    name='groceries-cli',
    version='0.0.1',
    py_modules=['groceries'],
    install_requires=[
        'Click',
        'PyYaml',
    ],
    entry_points='''
        [console_scripts]
        groceries=groceries.core:cli
    ''',
)
