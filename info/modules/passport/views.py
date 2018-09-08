import random
from datetime import datetime

from flask import request, abort, make_response, current_app, jsonify,session,Response
import re
from info import sr, db
from info.modules.passport import passport_blu
from utils.captcha.pic_captcha import captcha
from utils.response_code import RET, error_map
from info.lib.yuntongxun.sms import CCP
from info.models import User


# # 获取图片验证码
# @passport_blu.route('/get_img_code')
# def get_img_code():
#     # 获取参数 校验参数　生成图片验证码　将图片key 和验证码文字保存到数据中　
#     # 返回验证码图片　（　创建响应头　设置响应头的格式　image/jpeg)
#     # 获取参数
#     img_code_id = request.args.get('img_code_id')
#     # 校验参数
#     if not img_code_id:
#         return abort(403)
#     # 生成图片验证码
#     img_name, img_code_text, img_code_types = captcha.generate_captcha()
#     # 将图片key　和图片验证码文字保存到数据库中
#     try:
#         sr.set('img_code_id_'+img_code_id,img_code_text,ex=180)
#     except BaseException as e:
#         current_app.logger.error(e)
#         return abort(500)
#     # 返回验证码图片　（创建响应头　设置响应头）
#     response = make_response(img_code_types)
#     response.content_type = 'image/jpeg'
#     return response
#
#
# # 获取短信验证码
# @passport_blu.route('/get_sms_code', methods=['POST'])
# def get_sms_code():
#     # 获取参数(图片key　手机号　输入的验证码)　request.json可以获取application/json格式传过来的数据
#     img_code_id = request.json.get('img_code_id')
#     mobile = request.json.get('mobile')
#     img_code = request.json.get('img_code')
#     # 校验参数
#     if not all([img_code_id,mobile,img_code]):
#         return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PAPAMRR])
#
#     # 检验手机格式
#     if not re.match(r"1[35678]\d{9}$", mobile):
#         return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
#     # 根据图片格式key　和取出验证码文字
#     try:
#         real_img_code = sr.get('img_code_id_'+img_code_id)
#     except BaseException as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.PARAMERR,errmsg=error_map[RET.PARAMERR])
#
#     # 校验图片验证码
#     if not real_img_code:  # 检验是否过期
#         return jsonify(errno=RET.PARAMERR,errmsg='验证码已过期')
#     # 将验证码统一转大写再比较
#     if img_code.upper() != real_img_code:  # 检验短信验证码是否正确
#         return jsonify(errno=RET.PARAMERR,errmsg='验证码错误')
#     # 根据手机号从数据库中取数据
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except BaseException as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
#
#     # 判断该用户是否存在
#     if user: # 提示用户已存在
#         return jsonify(errno=RET.DATAEXIST,errmsg=error_map[RET.DATAEXIST])
#
#     # 如果校验成功，发送短信　生成四位随机i数字　将短信验证码保存到redis中
#     # res_code = CCP().send_template_sms(mobile,[sms_code,5],1)
#     sms_code = '%04d'%random.randint(0,9999)
#     current_app.logger.info('短信验证码为：%s'%sms_code)
#     res_code = CCP().send_template_sms('18715221675', [sms_code, 5], 1)
#     print(res_code)
#     if res_code == -1: # 短信发送失败
#         return jsonify(errno=RET.THIRDERR,errmsg=error_map[RET.THIRDERR])
#
#     # 根据发送结果使用json 返回
#     try:
#         sr.set('sms_code_id_'+mobile, sms_code, ex=60)
#     except BaseException as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg=errno_map[RET.DBERR])
#     # 将短信发送结果使用json返回
#     print('校验成功，发送短信')
#
#     return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])
#
#
# #用户注册
# @passport_blu.route('/register', methods=['POST'])
# def register():
#     # 获取参数  request.json可以获取到application/json格式传过来的json数据
#     mobile = request.json.get("mobile")
#     password = request.json.get("password")
#     sms_code = request.json.get("sms_code")
#     # 校验参数
#     if not all([mobile, password, sms_code]):
#         return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
#
#     # 校验手机号格式
#     if not re.match(r"1[35678]\d{9}$", mobile):
#         return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
#
#     # 根据手机号取出短信验证码文字
#     try:
#         real_sms_code = sr.get("sms_code_id_" + mobile)
#     except BaseException as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
#     # 校验图片验证码
#     if not real_sms_code:  # 校验是否已过期
#         return jsonify(errno=RET.PARAMERR, errmsg="验证码已过期")
#
#     if sms_code != real_sms_code:  # 校验验证码是否正确
#         return jsonify(errno=RET.PARAMERR, errmsg="验证码错误")
#
#     # 将用户数据保存到数据库
#     user = User()
#     user.mobile = mobile
#     # 使用计算性属性password对密码加密过程进行封装
#     user.password = password
#     user.nick_name = mobile
#     # 记录用户最后的登录时间
#     user.last_login = datetime.now()
#
#     try:
#         db.session.add(user)
#         db.session.commit()
#     except BaseException as e:
#         current_app.logger.error(e)
#         db.session.rollback()  # 设置回滚
#         return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
#
#     # 状态保持  免密码登录
#     session["user_id"] = user.id
#     print('注册成功')
#     return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])
#
#
# # 用户登录
# @passport_blu.route('/login',methods=['POST'])
# def login():
#     # 获取参数　校验参数　校验手机号　根据手机号取出用户模型　校验密码　将校验结果返回
#     # 校验参数
#     mobile = request.json.get('mobile')
#     password = request.json.get('password')
#     # 校验参数
#     if not all([mobile, password]):
#         return jsonify(errno.RET.PARAMERR,errmsg=error_map[RET.PARAMERR])
#     # 校验手机号
#     if not re.match(r"1[345678]\d{9}$", mobile):
#         return jsonify(errno=RET.PARAMERR,errmsg=error_map[RET.PARAMERR])
#     # 根据手机号取出用户模型
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except BaseException as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR,errmsg=error_map[RET.DBERR])
#     # 判断用户是否存在
#     if not user:
#         return jsonify(errno=RET.USERERR,errmsg=error_map[RET.USERERR])
#     # 校验密码是否正确
#     if not user.check_password(password):
#         return jsonify(errno=RET.PWDERR,errmsg=error_map[RET.PWDERR])
#     # 记录用户最后的登录时间
#     user.last_login = datetime.now()
#
#     # 状态保持
#     session['user_id'] = user.id
#     # 将结果已Json 返回
#     return jsonify(errno=RET.OK,errmsg=error_map[RET.OK])
#
#
# # 退出登录
# @passport_blu.route('/logout')
# def logout():
#     # 将用户信息从session中删除　pop 可以设置默认值　当键值不存在时，不会报错并返回默认值
#     session.pop('user_id',None)
#     # 将结果返回
#     return jsonify(errno=RET.OK,errmsg=error_map[RET.OK])


# 获取图片验证码
@passport_blu.route('/get_img_code')
def get_img_code():
    # 获取参数
    img_code_id = request.args.get('img_code_id')
    # 校验参数
    if not img_code_id:
        return abort(403)
    # 生成图片验证码
    img_name, img_code_text, img_code_bytes = captcha.generate_captcha()
    # 将图片key 和图片文字保存到数据中
    try:
        sr.set('img_code_id_'+img_code_id,img_code_text,ex=180)
    except BaseException as e:
        current_app.logger.error(e)
        return abort(500)
    # 返回验证码图片
    # 创建响应头 设置响应头
    response = make_response(img_code_bytes)
    # 设置响应头
    response.content_type='image/jpeg'
    return response


# 获取短信验证码
@passport_blu.route('/get_sms_code',methods=['POST'])
def get_sms_code():
    # 获取参数 （手机号 图片key 图片验证码）
    mobile = request.json.get('mobile')
    img_code_id = request.json.get('img_code_id')
    img_code = request.json.get('img_code')
    # 校验参数
    if not all([mobile, img_code_id, img_code]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
    if not re.match(r"1[345678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
    # 根据图片key 取出验证码文字
    try:
        real_img_code = sr.get('img_code_id_'+img_code_id)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    # 检验验证码是否过期 是否正确
    if not real_img_code:
        return jsonify(errno=RET.PARAMERR,errmsg='验证码已过期')
    if img_code.upper() != real_img_code:
        return jsonify(errno=RET.PARAMERR,errmsg="验证码错误")
    # 校验成功 发送短信
    sms_code = "%04d"%random.randint(0,9999)
    current_app.logger.info('短信验证码为%s'%sms_code)
    res_code = CCP().send_template_sms(18715221675,[sms_code, 5], 1)
    print(res_code)
    if res_code == -1:
        return jsonify(errno=RET.THIRDERR, errmsg=error_map[REI.RET.THIRDERR])
    # 将短信验证码保存到数据库中
    try:
        sr.set('sms_code_id_'+mobile,sms_code,ex=60)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg= error_map[RET.DBERR])
    # 根据短信结果使用json 返回
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])


# 用户注册
@passport_blu.route('/register',methods=['POST'])
def register():
    # 获取参数
    mobile = request.json.get('mobile')
    password = request.json.get('password')
    sms_code = request.json.get('sms_code')
    # 校验参数
    if not all([mobile, password, sms_code]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
    # 手机号校验
    if not re.match(r"1[345678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
    # 根据手机号取出短信验证码
    try:
        real_sms_code = sr.get('sms_code_id_'+mobile)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    # 检验短信验证码
    if not real_sms_code:
        return jsonify(errno=RET.PARAMERR,errmsg='验证码已过期')
    if sms_code != real_sms_code:
        return jsonify(errno=RET.PARAMERR,errmsg="验证码错误")
    # 将用户数据保存到数据库
    user = User()
    user.mobile = mobile
    user.password = password
    user.nick_name = mobile
    user.last_login = datetime.now()
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    # 状态保持 免密码登录
    session['user_id'] = user.id
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])


# 用户登录
@passport_blu.route('/login',methods=['POST'])
def login():
    # 获取参数
    mobile = request.json.get('mobile')
    password = request.json.get('password')
    # 校验参数
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
    if not re.match(r"1[345678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])
    # 根据手机号从数据库中取出模型
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    if not user:
        return jsonify(errno=RET.USERERR,errmsg=error_map[RET.USERERR])
    # 校验密码
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR,errmsg=error_map[RET.PWDERR])
    # 记录用户最后的登录时间
    user.last_login = datetime.now()

    # 状态保持
    session['user_id'] = user.id
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])


# 退出登录
@passport_blu.route('/logout')
def logout():
    # 将用户信息从session 中删除 pop可以设置默认值 当键值对不存在时，不会报错，返回默认值
    session.pop('user_id', None)
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])