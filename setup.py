from setuptools import setup


setup(
    name='groceries',
    version='0.0.1',
    py_modules=['groceries'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_script]
        groceries=groceries:cli
    ''',
)
