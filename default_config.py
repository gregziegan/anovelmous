config = {
    'database': {
        'driver': '',
        'host': '',
        'user': '',
        'passwd': '',
        'database': '',
    },
    'secret_key': 'development_key'
}


def get_db_uri():
    db_config = config['database']
    db_uri = '{driver}://{user}:{passwd}@{host}/{db}'.format(
        driver=db_config['driver'],
        user=db_config['user'],
        passwd=db_config['passwd'],
        host=db_config['host'],
        db=db_config['database']
    )
    return db_uri
