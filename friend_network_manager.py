#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好友网络管理器 - 最终修复版本
包含好友申请、情侣配对等所有功能
"""

import requests
import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal

class FriendNetworkManager(QObject):
    """好友网络管理器 - 最终修复版本"""
    
    # 信号定义
    registration_status_changed = pyqtSignal(bool)  # 注册状态改变
    login_status_changed = pyqtSignal(bool)  # 登录状态改变
    friend_request_received = pyqtSignal(str, str, str)  # 好友申请 (from_user_id, from_user_name, message)
    couple_request_received = pyqtSignal(str, str, str)  # 情侣申请 (from_user_id, from_user_name, message)
    friend_status_changed = pyqtSignal(str, bool)  # 好友状态改变 (friend_id, online)
    couple_status_changed = pyqtSignal(str, bool)  # 情侣状态改变 (partner_id, online)
    pet_action_received = pyqtSignal(int, str, str)  # 宠物动作 (pet_id, action_type, action_data)
    
    def __init__(self, server_url="https://lovepetty-friend-server.onrender.com"):
        super().__init__()
        self.server_url = server_url
        self.user_id = None
        self.user_name = None
        self.registered = False
        self.logged_in = False
        self.last_message_timestamp = 0
        self.polling_thread = None
        self.running = False
        
    def register_user(self, user_id: str, user_name: str) -> bool:
        """注册用户"""
        try:
            response = requests.post(f"{self.server_url}/register_user", 
                                   json={
                                       'user_id': user_id,
                                       'user_name': user_name
                                   }, timeout=10)
            
            if response.status_code == 200:
                self.user_id = user_id
                self.user_name = user_name
                self.registered = True
                self.logged_in = True
                self.start_polling()
                self.registration_status_changed.emit(True)
                return True
            else:
                print(f"注册失败: {response.text}")
                self.registration_status_changed.emit(False)
                return False
                
        except Exception as e:
            print(f"注册异常: {e}")
            self.registration_status_changed.emit(False)
            return False
            
    def login_user(self, user_id: str, user_name: str) -> bool:
        """用户登录"""
        try:
            response = requests.post(f"{self.server_url}/login_user", 
                                   json={
                                       'user_id': user_id,
                                       'user_name': user_name
                                   }, timeout=10)
            
            if response.status_code == 200:
                self.user_id = user_id
                self.user_name = user_name
                self.logged_in = True
                self.start_polling()
                self.login_status_changed.emit(True)
                return True
            else:
                print(f"登录失败: {response.text}")
                self.login_status_changed.emit(False)
                return False
                
        except Exception as e:
            print(f"登录异常: {e}")
            self.login_status_changed.emit(False)
            return False
    
    def search_user(self, user_id: str) -> dict:
        """搜索用户"""
        try:
            response = requests.get(f"{self.server_url}/search_user", 
                                  params={'user_id': user_id}, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"搜索用户失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"搜索用户异常: {e}")
            return None
    
    def send_friend_request(self, target_user_id: str, message: str = "我想和你成为好友") -> bool:
        """发送好友申请"""
        if not self.user_id or not self.user_name:
            return False
            
        try:
            response = requests.post(f"{self.server_url}/send_friend_request", 
                                   json={
                                       'from_user_id': self.user_id,
                                       'from_user_name': self.user_name,
                                       'to_user_id': target_user_id,
                                       'message': message
                                   }, timeout=10)
            
            if response.status_code == 200:
                print(f"好友申请发送成功: {target_user_id}")
                return True
            else:
                print(f"发送好友申请失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"发送好友申请异常: {e}")
            return False
    
    def send_couple_request(self, target_user_id: str, message: str = "我想和你成为情侣") -> bool:
        """发送情侣申请"""
        if not self.user_id or not self.user_name:
            return False
            
        try:
            response = requests.post(f"{self.server_url}/send_couple_request", 
                                   json={
                                       'from_user_id': self.user_id,
                                       'from_user_name': self.user_name,
                                       'to_user_id': target_user_id,
                                       'message': message
                                   }, timeout=10)
            
            if response.status_code == 200:
                print(f"情侣申请发送成功: {target_user_id}")
                return True
            else:
                print(f"发送情侣申请失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"发送情侣申请异常: {e}")
            return False
    
    def accept_friend_request(self, from_user_id: str) -> bool:
        """接受好友申请 - 最终修复版本"""
        if not self.user_id:
            print("❌ 用户ID为空，无法接受好友申请")
            return False
            
        try:
            # 尝试多种数据格式
            request_formats = [
                # 格式1: 标准格式
                {
                    'user_id': self.user_id,
                    'from_user_id': from_user_id
                },
                # 格式2: 字符串格式
                {
                    'user_id': str(self.user_id),
                    'from_user_id': str(from_user_id)
                },
                # 格式3: 添加额外字段
                {
                    'user_id': self.user_id,
                    'from_user_id': from_user_id,
                    'timestamp': time.time()
                }
            ]
            
            for i, request_data in enumerate(request_formats):
                print(f"🔍 尝试格式 {i+1}: {request_data}")
                
                response = requests.post(f"{self.server_url}/accept_friend_request", 
                                       json=request_data, timeout=10)
                
                print(f"📡 格式 {i+1} 响应:")
                print(f"   状态码: {response.status_code}")
                print(f"   响应内容: {response.text}")
                
                if response.status_code == 200:
                    print(f"✅ 好友申请接受成功: {from_user_id}")
                    return True
                elif response.status_code == 404 and "未找到好友申请" in response.text:
                    print(f"⚠️ 未找到好友申请，可能申请已被处理")
                    return False
                else:
                    print(f"❌ 格式 {i+1} 失败: {response.text}")
                    continue
            
            print(f"❌ 所有格式都失败了")
            return False
                
        except Exception as e:
            print(f"❌ 接受好友申请异常: {e}")
            return False
    
    def accept_couple_request(self, from_user_id: str) -> bool:
        """接受情侣申请 - 最终修复版本"""
        if not self.user_id:
            print("❌ 用户ID为空，无法接受情侣申请")
            return False
            
        try:
            # 尝试多种数据格式
            request_formats = [
                # 格式1: 标准格式
                {
                    'user_id': self.user_id,
                    'from_user_id': from_user_id
                },
                # 格式2: 字符串格式
                {
                    'user_id': str(self.user_id),
                    'from_user_id': str(from_user_id)
                },
                # 格式3: 添加额外字段
                {
                    'user_id': self.user_id,
                    'from_user_id': from_user_id,
                    'timestamp': time.time()
                }
            ]
            
            for i, request_data in enumerate(request_formats):
                print(f"🔍 尝试情侣申请格式 {i+1}: {request_data}")
                
                response = requests.post(f"{self.server_url}/accept_couple_request", 
                                       json=request_data, timeout=10)
                
                print(f"📡 情侣申请格式 {i+1} 响应:")
                print(f"   状态码: {response.status_code}")
                print(f"   响应内容: {response.text}")
                
                if response.status_code == 200:
                    print(f"✅ 情侣申请接受成功: {from_user_id}")
                    return True
                elif response.status_code == 404 and "未找到情侣申请" in response.text:
                    print(f"⚠️ 未找到情侣申请，可能申请已被处理")
                    return False
                else:
                    print(f"❌ 情侣申请格式 {i+1} 失败: {response.text}")
                    continue
            
            print(f"❌ 所有情侣申请格式都失败了")
            return False
                
        except Exception as e:
            print(f"❌ 接受情侣申请异常: {e}")
            return False
    
    def reject_couple_request(self, from_user_id: str) -> bool:
        """拒绝情侣申请 - 最终修复版本"""
        if not self.user_id:
            print("❌ 用户ID为空，无法拒绝情侣申请")
            return False
            
        try:
            # 尝试多种数据格式
            request_formats = [
                # 格式1: 标准格式
                {
                    'user_id': self.user_id,
                    'from_user_id': from_user_id
                },
                # 格式2: 字符串格式
                {
                    'user_id': str(self.user_id),
                    'from_user_id': str(from_user_id)
                },
                # 格式3: 添加额外字段
                {
                    'user_id': self.user_id,
                    'from_user_id': from_user_id,
                    'timestamp': time.time()
                }
            ]
            
            for i, request_data in enumerate(request_formats):
                print(f"🔍 尝试拒绝情侣申请格式 {i+1}: {request_data}")
                
                response = requests.post(f"{self.server_url}/reject_couple_request", 
                                       json=request_data, timeout=10)
                
                print(f"📡 拒绝情侣申请格式 {i+1} 响应:")
                print(f"   状态码: {response.status_code}")
                print(f"   响应内容: {response.text}")
                
                if response.status_code == 200:
                    print(f"✅ 情侣申请拒绝成功: {from_user_id}")
                    return True
                elif response.status_code == 404 and "未找到情侣申请" in response.text:
                    print(f"⚠️ 未找到情侣申请，可能申请已被处理")
                    return False
                else:
                    print(f"❌ 拒绝情侣申请格式 {i+1} 失败: {response.text}")
                    continue
            
            print(f"❌ 所有拒绝情侣申请格式都失败了")
            return False
                
        except Exception as e:
            print(f"❌ 拒绝情侣申请异常: {e}")
            return False
    
    def get_friends_list(self) -> list:
        """获取好友列表"""
        if not self.user_id:
            return []
            
        try:
            response = requests.get(f"{self.server_url}/friends", 
                                  params={'user_id': self.user_id}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('friends', [])
            else:
                print(f"获取好友列表失败: {response.text}")
                return []
                
        except Exception as e:
            print(f"获取好友列表异常: {e}")
            return []
    
    def get_couple_status(self) -> dict:
        """获取情侣状态"""
        if not self.user_id:
            return {'has_couple': False}
            
        try:
            response = requests.get(f"{self.server_url}/couple_status", 
                                  params={'user_id': self.user_id}, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取情侣状态失败: {response.text}")
                return {'has_couple': False}
                
        except Exception as e:
            print(f"获取情侣状态异常: {e}")
            return {'has_couple': False}
    
    def get_couple_requests(self) -> list:
        """获取情侣申请列表"""
        if not self.user_id:
            return []
            
        try:
            response = requests.get(f"{self.server_url}/couple_requests", 
                                  params={'user_id': self.user_id}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('requests', [])
            else:
                print(f"获取情侣申请失败: {response.text}")
                return []
                
        except Exception as e:
            print(f"获取情侣申请异常: {e}")
            return []
    
    def get_friend_requests(self) -> list:
        """获取好友申请列表"""
        if not self.user_id:
            return []
            
        try:
            response = requests.get(f"{self.server_url}/friend_requests", 
                                  params={'user_id': self.user_id}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('requests', [])
            else:
                print(f"获取好友申请失败: {response.text}")
                return []
                
        except Exception as e:
            print(f"获取好友申请异常: {e}")
            return []
    
    def get_user_id(self) -> str:
        """获取用户ID"""
        return self.user_id
    
    def get_user_name(self) -> str:
        """获取用户名称"""
        return self.user_name
    
    def send_pet_action(self, pet_id: int, action_type: str, action_data: str):
        """发送宠物动作"""
        if not self.user_id:
            return
            
        try:
            response = requests.post(f"{self.server_url}/send", 
                                   json={
                                       'user_id': self.user_id,
                                       'type': 'pet_action',
                                       'message': f"{pet_id}:{action_type}:{action_data}"
                                   }, timeout=10)
            
            if response.status_code != 200:
                print(f"发送宠物动作失败: {response.text}")
                
        except Exception as e:
            print(f"发送宠物动作异常: {e}")
    
    def start_polling(self):
        """开始轮询"""
        if self.polling_thread is None or not self.polling_thread.is_alive():
            self.running = True
            self.polling_thread = threading.Thread(target=self._polling_loop)
            self.polling_thread.daemon = True
            self.polling_thread.start()
    
    def _polling_loop(self):
        """轮询循环"""
        while self.running and self.user_id:
            try:
                # 获取新消息
                response = requests.get(f"{self.server_url}/messages", 
                                      params={
                                          'user_id': self.user_id,
                                          'timestamp': self.last_message_timestamp
                                      }, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    messages = data.get('messages', [])
                    
                    for message in messages:
                        self.last_message_timestamp = max(self.last_message_timestamp, message['timestamp'])
                        
                        if message['type'] == 'friend_request':
                            self.friend_request_received.emit(
                                message['from_user_id'],
                                message['from_user_name'],
                                message['message']
                            )
                        elif message['type'] == 'couple_request':
                            self.couple_request_received.emit(
                                message['from_user_id'],
                                message['from_user_name'],
                                message['message']
                            )
                        elif message['type'] == 'friend_accepted':
                            print(f"✅ 收到好友申请接受通知: {message['from_user_name']}")
                        elif message['type'] == 'couple_accepted':
                            print(f"💕 收到情侣申请接受通知: {message['from_user_name']}")
                        elif message['type'] == 'couple_rejected':
                            print(f"💔 收到情侣申请拒绝通知: {message['from_user_name']}")
                
                # 心跳包
                requests.post(f"{self.server_url}/heartbeat", 
                             json={'user_id': self.user_id}, timeout=5)
                
            except Exception as e:
                print(f"轮询异常: {e}")
            
            time.sleep(5)  # 5秒轮询一次
    
    def disconnect(self):
        """断开连接"""
        self.running = False
        if self.polling_thread and self.polling_thread.is_alive():
            self.polling_thread.join(timeout=1) 
