import psycopg2


def get_connection(config):
    return psycopg2.connect(config.get_dbstring())