from setuptools import setup, find_packages

setup(
    name='anovelmous',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    url='http://anovelmous.com',
    license='MIT',
    author='Greg Ziegan, John Maroli',
    author_email='greg.ziegan@gmail.com, jmmaroli@aol.com',
    description='Let\'s write together.',
    install_requires=[
        'flask',
        'sqlalchemy',
        'flask-restless',
        'flask-sqlalchemy',
        'nltk',
        'redis',
        'amqp',
        'requests',
        'arrow',
        'numpy'
    ]
)
