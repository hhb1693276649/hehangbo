from flask import Blueprint

# 创建蓝图对象
user_blu = Blueprint('user', __name__, url_prefix='/user')

# 4. 关联视图函数
from .views import *