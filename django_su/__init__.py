import os

# The fake password we will use to authenticate su'ed users
SECRET_PASSWORD = os.urandom(64)
VERSION = (0, 4, 8)

__version__ = '.'.join([str(n) for n in VERSION])
