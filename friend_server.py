#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好友系统服务器 - 支持用户注册和好友申请
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
friend_requests = defaultdict(list)  # user_id -> list of pending requests
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
    
    # 添加到消息列表
    messages[to_user_id].append({
        'type': 'friend_request',
        'from_user_id': from_user_id,
        'from_user_name': from_user_name,
        'message': message,
        'timestamp': time.time()
    })
    
    return jsonify({'message': '好友申请发送成功'})

@app.route('/accept_friend_request', methods=['POST'])
def accept_friend_request():
    """接受好友申请"""
    data = request.json
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    
    if not from_user_id or not to_user_id:
        return jsonify({'error': '缺少必要参数'}), 400
        
    # 查找并移除好友申请
    request_found = False
    for i, request_data in enumerate(friend_requests[to_user_id]):
        if request_data['from_user_id'] == from_user_id:
            friend_requests[to_user_id].pop(i)
            request_found = True
            break
            
    if not request_found:
        return jsonify({'error': '好友申请不存在'}), 404
        
    # 添加好友关系
    friends[from_user_id].add(to_user_id)
    friends[to_user_id].add(from_user_id)
    
    # 发送通知消息
    messages[from_user_id].append({
        'type': 'friend_accepted',
        'from_user_id': to_user_id,
        'message': f'用户 {to_user_id} 接受了你的好友申请',
        'timestamp': time.time()
    })
    
    return jsonify({'message': '好友申请接受成功'})

@app.route('/friends', methods=['GET'])
def get_friends():
    """获取好友列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    if user_id not in users:
        return jsonify({'error': '用户不存在'}), 404
        
    friends_list = []
    for friend_id in friends[user_id]:
        if friend_id in users:
            friend_data = users[friend_id].copy()
            friend_data.pop('last_seen', None)
            friends_list.append(friend_data)
            
    return jsonify({'friends': friends_list})

@app.route('/friends_status', methods=['GET'])
def get_friends_status():
    """获取好友在线状态"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    friends_status = {}
    for friend_id in friends[user_id]:
        if friend_id in users:
            # 30秒内活跃视为在线
            online = time.time() - users[friend_id]['last_seen'] < 30
            friends_status[friend_id] = online
            
    return jsonify({'friends_status': friends_status})

@app.route('/send', methods=['POST'])
def send_message():
    """发送消息"""
    data = request.json
    user_id = data.get('user_id')
    message_type = data.get('type')
    target_user_id = data.get('target_user_id')
    
    if not all([user_id, message_type]):
        return jsonify({'error': '缺少必要参数'}), 400
        
    # 创建消息
    message = {
        'type': message_type,
        'user_id': user_id,
        'timestamp': time.time(),
        **data
    }
    
    if target_user_id:
        # 发送给特定用户
        if target_user_id in friends[user_id]:
            messages[target_user_id].append(message)
    else:
        # 发送给所有好友
        for friend_id in friends[user_id]:
            messages[friend_id].append(message)
    
    return jsonify({'message': '发送成功'})

@app.route('/messages', methods=['GET'])
def get_messages():
    """获取消息"""
    user_id = request.args.get('user_id')
    timestamp = float(request.args.get('timestamp', 0))
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
        
    # 过滤新消息
    new_messages = [
        msg for msg in messages[user_id]
        if msg['timestamp'] > timestamp
    ]
    
    # 清理旧消息（保留最近50条）
    if len(messages[user_id]) > 50:
        messages[user_id] = messages[user_id][-50:]
    
    return jsonify({'messages': new_messages})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    """心跳包"""
    data = request.json
    user_id = data.get('user_id')
    
    if user_id and user_id in users:
        users[user_id]['last_seen'] = time.time()
        users[user_id]['online'] = True
    
    return jsonify({'message': '心跳成功'})

@app.route('/')
def home():
    """首页"""
    return jsonify({
        'message': 'LovePetty Friend Server',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'users_count': len(users),
        'version': '2.0.0'
    })

if __name__ == '__main__':
    # 获取环境变量中的端口，如果没有则使用10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False) 