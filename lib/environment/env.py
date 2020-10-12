import os


# ENVIRONMENT

def env():
    return os.environ.get('ENV', 'test')


def is_production():
    return env() == 'prod'

def is_staging():
    return env() == 'staging'

def is_dev():
    return env() == 'dev'


def is_test():
    return (not is_dev() and not is_production() and not is_staging())


def is_local():
    return is_console()
