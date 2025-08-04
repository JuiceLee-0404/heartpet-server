#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户注册对话框
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QGroupBox,
                             QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import uuid

class UserRegistrationDialog(QDialog):
    """用户注册对话框"""
    
    # 信号定义
    registration_requested = pyqtSignal(str, str)  # 注册请求 (user_id, user_name)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("用户注册")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # 说明组
        info_group = QGroupBox("注册说明")
        info_layout = QVBoxLayout()
        
        info_text = QTextEdit()
        info_text.setMaximumHeight(100)
        info_text.setPlainText(
            "用户注册说明：\n\n"
            "1. 注册一个唯一的用户ID，用于好友搜索\n"
            "2. 用户ID是你在系统中的唯一标识\n"
            "3. 注册后可以通过ID搜索其他用户并发送好友申请\n"
            "4. 用户ID请妥善保管，用于后续登录"
        )
        info_text.setReadOnly(True)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 注册信息组
        registration_group = QGroupBox("注册信息")
        registration_layout = QVBoxLayout()
        
        # 用户ID输入
        user_id_layout = QHBoxLayout()
        user_id_layout.addWidget(QLabel("用户ID:"))
        self.user_id_edit = QLineEdit()
        self.user_id_edit.setPlaceholderText("输入用户ID")
        user_id_layout.addWidget(self.user_id_edit)
        
        self.generate_button = QPushButton("生成ID")
        self.generate_button.clicked.connect(self.generate_user_id)
        user_id_layout.addWidget(self.generate_button)
        
        registration_layout.addLayout(user_id_layout)
        
        # 用户名输入
        user_name_layout = QHBoxLayout()
        user_name_layout.addWidget(QLabel("昵称:"))
        self.user_name_edit = QLineEdit()
        self.user_name_edit.setPlaceholderText("输入你的昵称")
        user_name_layout.addWidget(self.user_name_edit)
        
        registration_layout.addLayout(user_name_layout)
        
        registration_group.setLayout(registration_layout)
        layout.addWidget(registration_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.register_button = QPushButton("注册")
        self.register_button.clicked.connect(self.confirm_registration)
        button_layout.addWidget(self.register_button)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def generate_user_id(self):
        """生成用户ID"""
        user_id = f"U{uuid.uuid4().hex[:8].upper()}"
        self.user_id_edit.setText(user_id)
        
    def confirm_registration(self):
        """确认注册"""
        user_id = self.user_id_edit.text().strip()
        user_name = self.user_name_edit.text().strip()
        
        if not user_id:
            QMessageBox.warning(self, "提示", "请输入用户ID")
            return
            
        if not user_name:
            QMessageBox.warning(self, "提示", "请输入昵称")
            return
            
        message = f"即将注册用户：\n\n用户ID: {user_id}\n昵称: {user_name}\n\n确认注册吗？"
        
        reply = QMessageBox.question(self, "确认注册", message, 
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 发送注册信号
            self.registration_requested.emit(user_id, user_name)
            self.accept()
            
    def get_user_id(self) -> str:
        """获取用户ID"""
        return self.user_id_edit.text().strip()
        
    def get_user_name(self) -> str:
        """获取用户名"""
        return self.user_name_edit.text().strip() 