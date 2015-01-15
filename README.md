# Anovelmous

### Let's write together.

Anovelmous facilitates an anonymous internet community's writing of a novel.

## Documentation

Currently developing our documentation site.


## Development

To build upon the existing anovelmous API and get a local instance up and running, you must set the following
environment variables:

    DEBUG=True
    DATABASE_URL="driver+dialect://user:password@host:port/database"
    
For provisioning:

    pip install -r requirements.txt
    
Make sure to be in a virtualenv to guarantee a clean installation.


#### Note:

You will need to use a valid python connector (psycopg, mysql-python) 
depending on your backend store (MySQL, PostgreSQL, etc)