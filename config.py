import logging
from datetime import timedelta

from redis import StrictRedis


class Config(object):  # 自定义配置类
    DEBUG = True  # 开启调试模式
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/info16'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库变化
    REDIS_HOST = '127.0.0.1'  # redis的ip
    REDIS_PORT = 6379   # redis的端口
    SESSION_TYPE = 'redis'  # session 的存储类型
    # 设置session的存储使用的redis连接对象
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 对cookie中   保存的sessionid进行加密（使用app的密钥）
    SESSION_USE_SIGNER = True
    # SECRET_KEY = 'TEST'
    #  设置session的存储时间（sesion会默认进行持久化）
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # 开启数据修改时自动提交配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 设置数据发生修改后自动提交


class DevelopConfig(Config):  # 定义开发环境的配置
    DEBUG = True
    LOGLEVEL = logging.DEBUG


class ProductConfig(Config):  # 定义生产环境配置
    DEBUG = False
    LOGLEVEL = logging.ERROR

# 设置配置字典
config_dict = {
    'dev': DevelopConfig, 'pro': ProductConfig
}