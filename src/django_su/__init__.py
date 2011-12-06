import os

# The fake password we will use to authenticate su'ed users
SECRET_PASSWORD = os.urandom(64)
