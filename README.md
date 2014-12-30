# Anovelmous

### Let's write together.

Anovelmous facilitates an anonymous internet community's writing of a novel.

## Installation

To build upon the existing anovelmous API and get a local instance up and running:

    python setup.py install
    
Set the ANOVELMOUS_SETTINGS environment variable to point to your desired configuration file.

i.e.
    
    export ANOVELMOUS_SETTINGS=../development.cfg

The following is a configuration file template:

    DEBUG = True
    SECRET_KEY = "development_key"
    SQLALCHEMY_DATABASE_URI = "driver+dialect://user:password@host:port/database"
    

## Development

If you would wish to work on the production product, use the requirements.txt

    pip install -r requirements.txt
    
Make sure to be in a virtualenv to guarantee a clean installation.

Then, follow the instructions concerning the configuration file stated [above](#Installation).

#### Note:

You will need to use a valid python connector (psycopg, mysql-python) 
depending on your backend store (MySQL, PostgreSQL, etc)