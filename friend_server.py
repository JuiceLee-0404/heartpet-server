#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好友系统服务器 - 最终完整修复版本
包含好友申请、情侣配对等所有功能
"""

from flask import Flask, request, jsonify
import json
import time
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# 存储用户数据
users = {}  # user_id -> user_data
friends = defaultdict(set)  # user_id -> set of friend_ids
friend_requests = defaultdict(list)  # user_id -> list of pending friend requests
couple_requests = defaultdict(list)  # user_id -> list of pending couple requests
couples = {}  # user_id -> couple_partner_id (双向关系)
messages = defaultdict(list)  # user_id -> list of messages

@app.route('/register_user', methods=['POST'])
def register_user():
    """注册用户"""
    data = request.json
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    
    if not user_id or not user_name:
        return jsonify({'error': '缺少必要参数'}), 400
        
    if user_id in users:
        return jsonify({'error': '用户ID已存在'}), 400
        
    # 存储用户信息
    users[user_id] = {
        'user_id': user_id,
        'user_name': user_name,
        'online': True,
        'last_seen': time.time()
    }
    
    return jsonify({
        'message': '注册成功',
        'user_id': user_id
    })

@app.route('/login_user', methods=['POST'])
def login_user():
    """用户登录"""
    data = request.json
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    
    if not user_id or not user_name:
        return jsonify({'error': '缺少必要参数'}), 400
        
    # 如果用户不存在，自动注册
    if user_id not in users:
        users[user_id] = {
            'user_id': user_id,
            'user_name': user_name,
            'online': True,
            'last_seen': time.time()
        }
        
    # 更新用户状态
    users[user_id]['online'] = True
    users[user_id]['last_seen'] = time.time()
    users[user_id]['user_name'] = user_name  # 允许更新昵称
    
    return jsonify({
        'message': '登录成功',
        'user_id': user_id
    })

@app.route('/search_user', methods=['GET'])
def search_user():
    """搜索用户"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id in users:
        user_data = users[user_id].copy()
        # 不返回敏感信息
        user_data.pop('last_seen', None)
        return jsonify({'user': user_data})
    else:
        return jsonify({'error': '用户不存在'}), 404

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    """发送好友申请"""
    data = request.json
    from_user_id = data.get('from_user_id')
    from_user_name = data.get('from_user_name')
    to_user_id = data.get('to_user_id')
    message = data.get('message', '我想和你成为好友')
    
    if not all([from_user_id, from_user_name, to_user_id]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    if to_user_id not in users:
        return jsonify({'error': '目标用户不存在'}), 404
        
    if from_user_id == to_user_id:
        return jsonify({'error': '不能向自己发送好友申请'}), 400
        
    # 检查是否已经是好友
    if to_user_id in friends[from_user_id]:
        return jsonify({'error': '已经是好友了'}), 400
        
    # 检查是否已经发送过申请
    for request_data in friend_requests[to_user_id]:
        if request_data['from_user_id'] == from_user_id:
            return jsonify({'error': '已经发送过好友申请'}), 400
    
    # 创建好友申请
    friend_request = {
        'from_user_id': from_user_id,
        'from_user_name': from_user_name,
        'to_user_id': to_user_id,
        'message': message,
        'timestamp': time.time()
    }
    
    friend_requests[to_user_id].append(friend_request)
    
    # 发送消息通知
    message_data = {
        'type': 'friend_request',
        'from_user_id': from_user_id,
        'from_user_name': from_user_name,
        'message': message,
        'timestamp': time.time()
    }
    
    messages[to_user_id].append(message_data)
    
    return jsonify({'message': '好友申请发送成功'})

@app.route('/send_couple_request', methods=['POST'])
def send_couple_request():
    """发送情侣申请"""
    data = request.json
    from_user_id = data.get('from_user_id')
    from_user_name = data.get('from_user_name')
    to_user_id = data.get('to_user_id')
    message = data.get('message', '我想和你成为情侣')
    
    if not all([from_user_id, from_user_name, to_user_id]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    if to_user_id not in users:
        return jsonify({'error': '目标用户不存在'}), 404
        
    if from_user_id == to_user_id:
        return jsonify({'error': '不能向自己发送情侣申请'}), 400
        
    # 检查是否已经是情侣
    if from_user_id in couples and couples[from_user_id] == to_user_id:
        return jsonify({'error': '已经是情侣了'}), 400
        
    # 检查是否已经发送过申请
    for request_data in couple_requests[to_user_id]:
        if request_data['from_user_id'] == from_user_id:
            return jsonify({'error': '已经发送过情侣申请'}), 400
    
    # 创建情侣申请
    couple_request = {
        'from_user_id': from_user_id,
        'from_user_name': from_user_name,
        'to_user_id': to_user_id,
        'message': message,
        'timestamp': time.time()
    }
    
    couple_requests[to_user_id].append(couple_request)
    
    # 发送消息通知
    message_data = {
        'type': 'couple_request',
        'from_user_id': from_user_id,
        'from_user_name': from_user_name,
        'message': message,
        'timestamp': time.time()
    }
    
    messages[to_user_id].append(message_data)
    
    return jsonify({'message': '情侣申请发送成功'})

@app.route('/accept_friend_request', methods=['POST'])
def accept_friend_request():
    """接受好友申请 - 最终修复版本"""
    data = request.json
    print(f"DEBUG: 接收到的数据: {data}")
    
    # 检查数据是否为None
    if data is None:
        print("DEBUG: 请求数据为空")
        return jsonify({'error': '请求数据为空'}), 400
    
    user_id = data.get('user_id')
    from_user_id = data.get('from_user_id')
    
    print(f"DEBUG: user_id = {user_id}, from_user_id = {from_user_id}")
    
    # 修复参数验证 - 使用更宽松的验证
    if not user_id or not from_user_id:
        print(f"DEBUG: 参数验证失败 - user_id: '{user_id}', from_user_id: '{from_user_id}'")
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 检查用户是否存在
    if user_id not in users:
        print(f"DEBUG: 用户不存在 - {user_id}")
        return jsonify({'error': '用户不存在'}), 404
        
    if from_user_id not in users:
        print(f"DEBUG: 申请者不存在 - {from_user_id}")
        return jsonify({'error': '申请者不存在'}), 404
        
    # 查找并移除好友申请
    request_found = False
    if user_id in friend_requests:
        for i, request_data in enumerate(friend_requests[user_id]):
            if request_data['from_user_id'] == from_user_id:
                friend_requests[user_id].pop(i)
                request_found = True
                print(f"DEBUG: 找到并移除好友申请")
                break
                
    if not request_found:
        print(f"DEBUG: 未找到好友申请 - user_id: {user_id}, from_user_id: {from_user_id}")
        print(f"DEBUG: 当前好友申请列表: {friend_requests}")
        return jsonify({'error': '未找到好友申请'}), 404
        
    # 建立好友关系
    friends[user_id].add(from_user_id)
    friends[from_user_id].add(user_id)
    print(f"DEBUG: 建立好友关系成功")
    
    # 发送接受通知
    message_data = {
        'type': 'friend_accepted',
        'from_user_id': user_id,
        'from_user_name': users[user_id]['user_name'],
        'message': '已接受你的好友申请',
        'timestamp': time.time()
    }
    
    messages[from_user_id].append(message_data)
    print(f"DEBUG: 发送接受通知成功")
    
    return jsonify({'message': '好友申请接受成功'})

@app.route('/accept_couple_request', methods=['POST'])
def accept_couple_request():
    """接受情侣申请 - 最终修复版本"""
    data = request.json
    print(f"DEBUG: 接收到的情侣申请数据: {data}")
    
    # 检查数据是否为None
    if data is None:
        print("DEBUG: 请求数据为空")
        return jsonify({'error': '请求数据为空'}), 400
    
    user_id = data.get('user_id')
    from_user_id = data.get('from_user_id')
    
    print(f"DEBUG: user_id = {user_id}, from_user_id = {from_user_id}")
    
    # 修复参数验证 - 使用更宽松的验证
    if not user_id or not from_user_id:
        print(f"DEBUG: 参数验证失败 - user_id: '{user_id}', from_user_id: '{from_user_id}'")
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 检查用户是否存在
    if user_id not in users:
        print(f"DEBUG: 用户不存在 - {user_id}")
        return jsonify({'error': '用户不存在'}), 404
        
    if from_user_id not in users:
        print(f"DEBUG: 申请者不存在 - {from_user_id}")
        return jsonify({'error': '申请者不存在'}), 404
        
    # 查找并移除情侣申请
    request_found = False
    if user_id in couple_requests:
        for i, request_data in enumerate(couple_requests[user_id]):
            if request_data['from_user_id'] == from_user_id:
                couple_requests[user_id].pop(i)
                request_found = True
                print(f"DEBUG: 找到并移除情侣申请")
                break
                
    if not request_found:
        print(f"DEBUG: 未找到情侣申请 - user_id: {user_id}, from_user_id: {from_user_id}")
        print(f"DEBUG: 当前情侣申请列表: {couple_requests}")
        return jsonify({'error': '未找到情侣申请'}), 404
        
    # 建立情侣关系
    couples[user_id] = from_user_id
    couples[from_user_id] = user_id
    print(f"DEBUG: 建立情侣关系成功")
    
    # 发送接受通知
    message_data = {
        'type': 'couple_accepted',
        'from_user_id': user_id,
        'from_user_name': users[user_id]['user_name'],
        'message': '已接受你的情侣申请',
        'timestamp': time.time()
    }
    
    messages[from_user_id].append(message_data)
    print(f"DEBUG: 发送情侣接受通知成功")
    
    return jsonify({'message': '情侣申请接受成功'})

@app.route('/reject_couple_request', methods=['POST'])
def reject_couple_request():
    """拒绝情侣申请 - 最终修复版本"""
    data = request.json
    print(f"DEBUG: 接收到的拒绝情侣申请数据: {data}")
    
    # 检查数据是否为None
    if data is None:
        print("DEBUG: 请求数据为空")
        return jsonify({'error': '请求数据为空'}), 400
    
    user_id = data.get('user_id')
    from_user_id = data.get('from_user_id')
    
    print(f"DEBUG: user_id = {user_id}, from_user_id = {from_user_id}")
    
    # 修复参数验证 - 使用更宽松的验证
    if not user_id or not from_user_id:
        print(f"DEBUG: 参数验证失败 - user_id: '{user_id}', from_user_id: '{from_user_id}'")
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 检查用户是否存在
    if user_id not in users:
        print(f"DEBUG: 用户不存在 - {user_id}")
        return jsonify({'error': '用户不存在'}), 404
        
    if from_user_id not in users:
        print(f"DEBUG: 申请者不存在 - {from_user_id}")
        return jsonify({'error': '申请者不存在'}), 404
        
    # 查找并移除情侣申请
    request_found = False
    if user_id in couple_requests:
        for i, request_data in enumerate(couple_requests[user_id]):
            if request_data['from_user_id'] == from_user_id:
                couple_requests[user_id].pop(i)
                request_found = True
                print(f"DEBUG: 找到并移除情侣申请")
                break
                
    if not request_found:
        print(f"DEBUG: 未找到情侣申请 - user_id: {user_id}, from_user_id: {from_user_id}")
        return jsonify({'error': '未找到情侣申请'}), 404
        
    # 发送拒绝通知
    message_data = {
        'type': 'couple_rejected',
        'from_user_id': user_id,
        'from_user_name': users[user_id]['user_name'],
        'message': '已拒绝你的情侣申请',
        'timestamp': time.time()
    }
    
    messages[from_user_id].append(message_data)
    print(f"DEBUG: 发送情侣拒绝通知成功")
    
    return jsonify({'message': '情侣申请拒绝成功'})

@app.route('/friends', methods=['GET'])
def get_friends():
    """获取好友列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    friend_list = []
    for friend_id in friends[user_id]:
        if friend_id in users:
            friend_list.append({
                'user_id': friend_id,
                'user_name': users[friend_id]['user_name'],
                'online': users[friend_id]['online']
            })
            
    return jsonify({'friends': friend_list})

@app.route('/couple_status', methods=['GET'])
def get_couple_status():
    """获取情侣状态"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    if user_id in couples:
        partner_id = couples[user_id]
        if partner_id in users:
            return jsonify({
                'has_couple': True,
                'partner': {
                    'user_id': partner_id,
                    'user_name': users[partner_id]['user_name'],
                    'online': users[partner_id]['online']
                }
            })
    
    return jsonify({'has_couple': False})

@app.route('/couple_requests', methods=['GET'])
def get_couple_requests():
    """获取情侣申请列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    return jsonify({'requests': couple_requests[user_id]})

@app.route('/friend_requests', methods=['GET'])
def get_friend_requests():
    """获取好友申请列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    return jsonify({'requests': friend_requests[user_id]})

@app.route('/friends_status', methods=['GET'])
def get_friends_status():
    """获取好友在线状态"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    status_list = []
    for friend_id in friends[user_id]:
        if friend_id in users:
            status_list.append({
                'user_id': friend_id,
                'user_name': users[friend_id]['user_name'],
                'online': users[friend_id]['online']
            })
            
    return jsonify({'friends': status_list})

@app.route('/send', methods=['POST'])
def send_message():
    """发送消息"""
    data = request.json
    user_id = data.get('user_id')
    message_type = data.get('type')
    target_user_id = data.get('target_user_id')
    message_content = data.get('message', '')
    
    if not all([user_id, message_type]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    # 创建消息
    message_data = {
        'type': message_type,
        'from_user_id': user_id,
        'from_user_name': users[user_id]['user_name'],
        'message': message_content,
        'timestamp': time.time()
    }
    
    # 如果有目标用户，发送给目标用户
    if target_user_id and target_user_id in users:
        messages[target_user_id].append(message_data)
    else:
        # 否则发送给所有好友
        for friend_id in friends[user_id]:
            if friend_id in users:
                messages[friend_id].append(message_data)
    
    return jsonify({'message': '消息发送成功'})

@app.route('/messages', methods=['GET'])
def get_messages():
    """获取消息"""
    user_id = request.args.get('user_id')
    timestamp = request.args.get('timestamp', 0)
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    # 过滤新消息
    new_messages = []
    for message in messages[user_id]:
        if message['timestamp'] > float(timestamp):
            new_messages.append(message)
            
    return jsonify({'messages': new_messages})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    """心跳包"""
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id in users:
        users[user_id]['last_seen'] = time.time()
        users[user_id]['online'] = True
        return jsonify({'message': '心跳成功'})
    else:
        return jsonify({'error': '用户不存在'}), 404

@app.route('/')
def home():
    """首页"""
    return jsonify({
        'message': 'LovePetty Friend Server',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'users_count': len(users),
        'version': '2.1.0',
        'features': [
            'user_registration',
            'friend_requests',
            'couple_pairing',
            'messaging',
            'real_time_status'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
