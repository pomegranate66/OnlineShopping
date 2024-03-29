"""
Django settings for OnlineShopping project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#  --------------------------- 配置app的根目录 --------------------------------
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '40pofi)zunc^1mnx^ma7$k4ird^(@753f9eo*2b@m62(q(zw-0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user',
    'apps.goods',
    'apps.cart',
    'apps.order',
    # ---------------------------- 富文本编辑器 -----------------------
    'tinymce',
    # ---------------------------- 全文搜索框架 -----------------------
    'haystack',
    'whoosh'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OnlineShopping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ------------------------------ 定义user的session ----------------------------
                'apps.user.get_user_session.get_session',
            ],
        },
    },
]

WSGI_APPLICATION = 'OnlineShopping.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'onlineshopping',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': 3306,
        'HOST': '127.0.0.1'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# --------------------------- 富文本编辑器 ---------------------------
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',  # theme主题 ,advanced高级
    'width': 600,
    'height': 400,
}
# ----------------------- 静态文件地址 --------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

#  ------------------------- 配置图片的位置 ------------------------
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#  ------------------------- 发送邮件的配置信息 --------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 发送邮件配置
EMAIL_HOST = 'smtp.163.com'  # smpt服务地址
EMAIL_PORT = 25  # 固定端口
EMAIL_HOST_USER = 'wqzhpu@163.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'admin123'  # 在邮箱中设置的客户端授权密码
EMAIL_FROM = '小店<wqzhpu@163.com>'  # 收件人看到的发件人

# ------------------------- Redis数据库链接配置 -------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# -------------------------- 全文搜索框架基础配置 ----------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        #     使用whoosh引擎
        #     ’ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'apps.goods.whoosh_backend.WhooshEngine',
        #     索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index')
    }
}

# 当对数据进行增删改时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
