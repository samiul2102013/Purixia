from decouple import config

env = config('DJANGO_ENV', default='dev')

if env == 'production':
    from .prod import *  # noqa
elif env == 'test':
    from .test import *  # noqa
else:
    from .dev import *  # noqa