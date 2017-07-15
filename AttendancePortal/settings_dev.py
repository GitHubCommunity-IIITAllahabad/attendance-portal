import os

DEBUG = True
SECRET_KEY = '7)p19%x(tj$_6@+uu!1oo(nj3tfuxj53z0i-zwn+)1zb=tqg4*'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'attendance_portal',
        'USER': 'postgres',
        'PASSWORD': os.environ['postgres_password'],
        'HOST': 'localhost',
        'PORT': '',
    }
}


