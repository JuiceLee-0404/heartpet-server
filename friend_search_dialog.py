#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好友搜索和申请对话框
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QGroupBox,
                             QMessageBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class FriendSearchDialog(QDialog):
    """好友搜索和申请对话框"""
    
    # 信号定义
    friend_request_sent = pyqtSignal(str, str)  # 好友申请 (target_user_id, message)
    
    def __init__(self, network_manager, parent=None):
        super().__init__(parent)
        self.network_manager = network_manager
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("好友搜索")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        # 搜索组
        search_group = QGroupBox("搜索用户")
        search_layout = QVBoxLayout()
        
        # 搜索输入
        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(QLabel("用户ID:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入要搜索的用户ID")
        search_input_layout.addWidget(self.search_edit)
        
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.search_user)
        search_input_layout.addWidget(self.search_button)
        
        search_layout.addLayout(search_input_layout)
        
        # 搜索结果
        self.result_label = QLabel("输入用户ID进行搜索")
        search_layout.addWidget(self.result_label)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # 好友申请组
        friend_request_group = QGroupBox("好友申请")
        friend_request_layout = QVBoxLayout()
        
        # 申请消息
        message_layout = QHBoxLayout()
        message_layout.addWidget(QLabel("申请消息:"))
        self.message_edit = QLineEdit()
        self.message_edit.setPlaceholderText("输入申请消息（可选）")
        message_layout.addWidget(self.message_edit)
        
        friend_request_layout.addLayout(message_layout)
        
        # 发送申请按钮
        self.send_request_button = QPushButton("发送好友申请")
        self.send_request_button.clicked.connect(self.send_friend_request)
        self.send_request_button.setEnabled(False)
        friend_request_layout.addWidget(self.send_request_button)
        
        friend_request_group.setLayout(friend_request_layout)
        layout.addWidget(friend_request_group)
        
        # 我的好友列表
        friends_group = QGroupBox("我的好友")
        friends_layout = QVBoxLayout()
        
        self.friends_list = QListWidget()
        self.friends_list.setMaximumHeight(150)
        friends_layout.addWidget(self.friends_list)
        
        # 刷新好友列表按钮
        self.refresh_button = QPushButton("刷新好友列表")
        self.refresh_button.clicked.connect(self.refresh_friends_list)
        friends_layout.addWidget(self.refresh_button)
        
        friends_group.setLayout(friends_layout)
        layout.addWidget(friends_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 初始化数据
        self.current_user = None
        self.refresh_friends_list()
        
    def search_user(self):
        """搜索用户"""
        user_id = self.search_edit.text().strip()
        
        if not user_id:
            QMessageBox.warning(self, "提示", "请输入用户ID")
            return
            
        try:
            # 这里应该调用网络管理器搜索用户
            # 暂时模拟搜索结果
            if user_id.startswith("U"):
                self.current_user = {
                    'user_id': user_id,
                    'user_name': f"用户{user_id[-4:]}"
                }
                self.result_label.setText(f"找到用户: {self.current_user['user_name']} ({user_id})")
                self.send_request_button.setEnabled(True)
            else:
                self.result_label.setText("未找到用户")
                self.send_request_button.setEnabled(False)
                self.current_user = None
                
        except Exception as e:
            QMessageBox.warning(self, "搜索失败", f"搜索用户时出错: {e}")
            
    def send_friend_request(self):
        """发送好友申请"""
        if not self.current_user:
            QMessageBox.warning(self, "提示", "请先搜索用户")
            return
            
        message = self.message_edit.text().strip()
        if not message:
            message = "我想和你成为好友"
            
        try:
            # 发送好友申请信号，不在这里显示成功提示
            self.friend_request_sent.emit(self.current_user['user_id'], message)
            
            # 清空搜索
            self.search_edit.clear()
            self.result_label.setText("输入用户ID进行搜索")
            self.send_request_button.setEnabled(False)
            self.current_user = None
            
            # 关闭对话框
            self.accept()
            
        except Exception as e:
            QMessageBox.warning(self, "发送失败", f"发送好友申请时出错: {e}")
            
    def refresh_friends_list(self):
        """刷新好友列表"""
        try:
            # 这里应该从网络管理器获取好友列表
            # 暂时显示模拟数据
            self.friends_list.clear()
            
            # 模拟好友列表
            friends = [
                {"user_id": "U12345678", "user_name": "小明"},
                {"user_id": "U87654321", "user_name": "小红"}
            ]
            
            for friend in friends:
                item = QListWidgetItem(f"{friend['user_name']} ({friend['user_id']})")
                self.friends_list.addItem(item)
                
        except Exception as e:
            QMessageBox.warning(self, "刷新失败", f"刷新好友列表时出错: {e}")
            
    def get_current_user(self):
        """获取当前搜索的用户"""
        return self.current_user 
