from decouple import config

ENVIRONMENT = config('ENV')

if ENVIRONMENT == 'dev':
    from .dev import *
else:
    from .prod import *
    