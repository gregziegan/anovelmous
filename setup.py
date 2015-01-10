from setuptools import setup, find_packages

setup(
    name='anovelmous',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    url='http://anovelmous.com',
    license='MIT',
    author='Greg Ziegan, John Maroli',
    author_email='greg.ziegan@gmail.com, jmmaroli@aol.com',
    description='Let\'s write together.',
    install_requires=[
        'flask>=0.10.1',
        'Werkzeug>=0.9.5',
        'sqlalchemy',
        'flask-migrate',
        'flask-restless',
        'flask-sqlalchemy',
        'flask-user',
        'nltk',
        'redis',
        'amqp',
        'requests',
        'arrow',
        'numpy',
        'sqlalchemy-utils'
    ]
)