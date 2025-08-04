#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好友网络管理器 - 支持用户注册和好友申请
"""

import json
import requests
import threading
import time
from typing import Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal

class FriendNetworkManager(QObject):
    """好友网络管理器"""
    
    # 信号定义
    registration_status_changed = pyqtSignal(bool)  # 注册状态改变
    friend_request_received = pyqtSignal(str, str, str)  # 收到好友申请 (from_user_id, from_user_name, message)
    friend_status_changed = pyqtSignal(str, bool)  # 好友状态改变 (friend_id, online)
    pet_action_received = pyqtSignal(int, str, str)  # 接收到宠物动作 (pet_id, action_type, action_data)
    
    def __init__(self):
        super().__init__()
        self.registered = False
        self.user_id = None
        self.user_name = None
        self.server_url = "https://lovepetty.onrender.com"  # 部署在Render的服务器
        self.polling_thread = None
        self.running = False
        self.friends = {}  # 好友列表
        
    def register_user(self, user_id: str, user_name: str) -> bool:
        """注册用户"""
        try:
            response = requests.post(f"{self.server_url}/register_user", json={
                'user_id': user_id,
                'user_name': user_name,
                'timestamp': time.time()
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.user_id = user_id
                self.user_name = user_name
                self.registered = True
                self.registration_status_changed.emit(True)
                
                # 启动轮询线程
                self.start_polling()
                
                print(f"用户注册成功: {user_id}")
                return True
            else:
                print(f"用户注册失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"注册错误: {e}")
            return False
            
    def search_user(self, target_user_id: str) -> Optional[dict]:
        """搜索用户"""
        try:
            response = requests.get(f"{self.server_url}/search_user", params={
                'user_id': target_user_id
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('user')
            else:
                print(f"搜索用户失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"搜索用户错误: {e}")
            return None
            
    def send_friend_request(self, target_user_id: str, message: str) -> bool:
        """发送好友申请"""
        try:
            response = requests.post(f"{self.server_url}/send_friend_request", json={
                'from_user_id': self.user_id,
                'from_user_name': self.user_name,
                'to_user_id': target_user_id,
                'message': message,
                'timestamp': time.time()
            }, timeout=10)
            
            if response.status_code == 200:
                print(f"好友申请发送成功: {target_user_id}")
                return True
            else:
                print(f"好友申请发送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"发送好友申请错误: {e}")
            return False
            
    def accept_friend_request(self, from_user_id: str) -> bool:
        """接受好友申请"""
        try:
            response = requests.post(f"{self.server_url}/accept_friend_request", json={
                'from_user_id': from_user_id,
                'to_user_id': self.user_id,
                'timestamp': time.time()
            }, timeout=10)
            
            if response.status_code == 200:
                print(f"接受好友申请成功: {from_user_id}")
                return True
            else:
                print(f"接受好友申请失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"接受好友申请错误: {e}")
            return False
            
    def get_friends_list(self) -> list:
        """获取好友列表"""
        try:
            response = requests.get(f"{self.server_url}/friends", params={
                'user_id': self.user_id
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                friends = data.get('friends', [])
                self.friends = {f['user_id']: f for f in friends}
                return friends
            else:
                print(f"获取好友列表失败: {response.text}")
                return []
                
        except Exception as e:
            print(f"获取好友列表错误: {e}")
            return []
            
    def start_polling(self):
        """启动轮询线程"""
        self.running = True
        self.polling_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self.polling_thread.start()
        
    def _polling_loop(self):
        """轮询循环"""
        while self.running and self.registered:
            try:
                # 获取新消息
                response = requests.get(f"{self.server_url}/messages", params={
                    'user_id': self.user_id,
                    'timestamp': time.time()
                }, timeout=5)
                
                if response.status_code == 200:
                    messages = response.json().get('messages', [])
                    for message in messages:
                        self._process_message(message)
                        
                # 检查好友在线状态
                self._check_friends_status()
                
                time.sleep(2)  # 每2秒轮询一次
                
            except Exception as e:
                if self.running:
                    print(f"轮询错误: {e}")
                    time.sleep(5)  # 出错时等待更长时间
                    
    def _process_message(self, message: dict):
        """处理接收到的消息"""
        message_type = message.get('type')
        
        if message_type == 'friend_request':
            from_user_id = message.get('from_user_id')
            from_user_name = message.get('from_user_name')
            request_message = message.get('message')
            
            if from_user_id and from_user_name:
                self.friend_request_received.emit(from_user_id, from_user_name, request_message)
                
        elif message_type == 'pet_action':
            pet_id = message.get('pet_id')
            action_type = message.get('action_type')
            action_data = message.get('action_data')
            
            if pet_id and action_type and action_data:
                self.pet_action_received.emit(pet_id, action_type, action_data)
                
        elif message_type == 'heartbeat':
            # 心跳包，保持连接
            pass
            
    def _check_friends_status(self):
        """检查好友在线状态"""
        try:
            response = requests.get(f"{self.server_url}/friends_status", params={
                'user_id': self.user_id
            }, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                friends_status = data.get('friends_status', {})
                
                for friend_id, online in friends_status.items():
                    self.friend_status_changed.emit(friend_id, online)
                    
        except Exception as e:
            print(f"检查好友状态错误: {e}")
            
    def send_pet_action(self, pet_id: int, action_type: str, action_data: str, target_user_id: str = None):
        """发送宠物动作"""
        if not self.registered:
            return
            
        try:
            payload = {
                'user_id': self.user_id,
                'user_name': self.user_name,
                'type': 'pet_action',
                'pet_id': pet_id,
                'action_type': action_type,
                'action_data': action_data,
                'timestamp': time.time()
            }
            
            if target_user_id:
                payload['target_user_id'] = target_user_id
                
            response = requests.post(f"{self.server_url}/send", json=payload, timeout=5)
            
            if response.status_code != 200:
                print(f"发送消息失败: {response.text}")
                
        except Exception as e:
            print(f"发送消息错误: {e}")
            
    def send_heartbeat(self):
        """发送心跳包"""
        if not self.registered:
            return
            
        try:
            requests.post(f"{self.server_url}/heartbeat", json={
                'user_id': self.user_id,
                'timestamp': time.time()
            }, timeout=5)
            
        except Exception as e:
            print(f"心跳包发送错误: {e}")
            
    def is_registered(self) -> bool:
        """检查是否已注册"""
        return self.registered
        
    def disconnect(self):
        """断开连接"""
        self.running = False
        self.registered = False
        
        if self.polling_thread:
            self.polling_thread.join(timeout=1)
            
        self.registration_status_changed.emit(False)
        print("已断开连接")
        
    def get_user_id(self) -> Optional[str]:
        """获取用户ID"""
        return self.user_id
        
    def get_user_name(self) -> Optional[str]:
        """获取用户名"""
        return self.user_name 