#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面宠物窗口 - 支持好友申请制
"""

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QMenu, QAction, 
                             QApplication, QMessageBox, QSystemTrayIcon, QMenu)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor, QIcon
from friend_network_manager import FriendNetworkManager
from user_registration_dialog import UserRegistrationDialog
from friend_search_dialog import FriendSearchDialog

class PetWindow(QWidget):
    """桌面宠物窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 拖拽相关变量
        self.dragging = False
        self.drag_position = QPoint()
        self.click_position = QPoint()
        
        # 网络管理器
        self.network_manager = FriendNetworkManager()
        self.network_manager.registration_status_changed.connect(self.on_registration_status_changed)
        self.network_manager.friend_request_received.connect(self.on_friend_request_received)
        self.network_manager.friend_status_changed.connect(self.on_friend_status_changed)
        self.network_manager.pet_action_received.connect(self.on_pet_action_received)
        
        # 宠物状态
        self.pet1_emotion = "正常"
        self.pet2_emotion = "正常"
        self.pet1_owner = None  # 控制者
        self.pet2_owner = None  # 控制者
        self.my_user_id = None
        self.my_user_name = None
        
        # 初始化界面
        self.init_ui()
        
        # 启动动画定时器
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(1000)  # 每秒更新一次
        
        # 启动检查窗口可见性的定时器
        self.visibility_timer = QTimer()
        self.visibility_timer.timeout.connect(self.ensure_visible)
        self.visibility_timer.start(500)  # 每500ms检查一次
        
        # 创建系统托盘
        self.create_system_tray()
        
        # 启动时显示用户注册对话框
        self.show_user_registration_dialog()
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性 - 使用更稳定的组合
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 始终置顶
            Qt.X11BypassWindowManagerHint  # 绕过窗口管理器（在macOS上也有效）
        )
        
        # 设置透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # 显示时不激活
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow, True)  # macOS专用：总是显示工具窗口
        
        # 设置窗口大小
        self.resize(200, 100)
        
        # 创建布局
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建两只小狗标签
        self.pet1_label = QLabel()
        self.pet2_label = QLabel()
        
        # 设置小狗大小
        self.pet1_label.setFixedSize(80, 80)
        self.pet2_label.setFixedSize(80, 80)
        
        # 创建占位符图片
        self.update_pets_display()
        
        # 添加到布局
        layout.addWidget(self.pet1_label)
        layout.addWidget(self.pet2_label)
        
        self.setLayout(layout)
        
        # 移动到屏幕右下角
        self.move_to_bottom_right()
        
        # 设置拖拽光标
        self.setCursor(Qt.SizeAllCursor)
        
    def ensure_visible(self):
        """确保窗口始终可见"""
        if not self.isVisible():
            self.show()
            self.raise_()
            
    def create_pet_pixmap(self, name, color, emotion="正常", owner=None):
        """创建宠物占位符图片"""
        pixmap = QPixmap(80, 80)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆形背景
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(10, 10, 60, 60)
        
        # 绘制表情
        painter.setPen(QColor(0, 0, 0))
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, f"{name}\n{emotion}")
        
        # 如果有控制者，显示控制者信息
        if owner:
            painter.setPen(QColor(255, 0, 0))
            painter.drawText(pixmap.rect(), Qt.AlignTop | Qt.AlignRight, "★")
        
        painter.end()
        return pixmap
        
    def update_pets_display(self):
        """更新宠物显示"""
        # 更新宠物1
        pet1_color = QColor(255, 182, 193)  # 粉色
        self.pet1_label.setPixmap(self.create_pet_pixmap("小狗1", pet1_color, self.pet1_emotion, self.pet1_owner))
        
        # 更新宠物2
        pet2_color = QColor(173, 216, 230)  # 蓝色
        self.pet2_label.setPixmap(self.create_pet_pixmap("小狗2", pet2_color, self.pet2_emotion, self.pet2_owner))
        
    def move_to_bottom_right(self):
        """移动到屏幕右下角"""
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 50
        y = screen.height() - self.height() - 100
        self.move(x, y)
        
    def update_animation(self):
        """更新动画 - 这里可以添加动画逻辑"""
        pass
        
    # 重写事件处理函数防止窗口消失
    def focusOutEvent(self, event):
        """焦点丢失事件 - 忽略以防止窗口消失"""
        event.ignore()
        
    def hideEvent(self, event):
        """隐藏事件 - 阻止意外隐藏"""
        if hasattr(self, '_closing') and self._closing:
            event.accept()
        else:
            event.ignore()
            self.show()
            self.raise_()
        
    # 鼠标事件处理 - 拖拽功能
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.click_position = event.globalPos()
            event.accept()
        elif event.button() == Qt.RightButton:
            # 右键显示菜单
            self.show_context_menu(event.globalPos())
            event.accept()
            
    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 拖拽"""
        if event.buttons() == Qt.LeftButton and self.dragging:
            # 拖拽窗口
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            
            # 判断是点击还是拖拽
            distance = (event.globalPos() - self.click_position).manhattanLength()
            if distance < 10:  # 移动距离小于10像素视为点击
                self.show_interaction_menu(event.globalPos())
            
            event.accept()
            
    def show_interaction_menu(self, pos):
        """显示交互菜单"""
        menu = QMenu(self)
        
        # 选择控制宠物（不需要好友配对）
        if not self.pet1_owner:
            action = menu.addAction("控制小狗1")
            action.triggered.connect(lambda: self.control_pet(1))
        elif not self.pet2_owner:
            action = menu.addAction("控制小狗2")
            action.triggered.connect(lambda: self.control_pet(2))
        else:
            menu.addAction("两只小狗都已被控制").setEnabled(False)
            
        menu.addSeparator()
        
        # 表情菜单
        emotions_menu = menu.addMenu("表情")
        emotions = ["开心", "难过", "愤怒", "骄傲", "害羞", "惊讶"]
        for emotion in emotions:
            action = emotions_menu.addAction(emotion)
            action.triggered.connect(lambda checked, e=emotion: self.set_emotion(e))
            
        # 互动菜单
        interactions_menu = menu.addMenu("互动")
        interactions = ["抚摸", "拥抱", "亲吻", "捏脸", "敲打"]
        for interaction in interactions:
            action = interactions_menu.addAction(interaction)
            action.triggered.connect(lambda checked, i=interaction: self.set_interaction(i))
            
        menu.exec_(pos)
        
    def show_context_menu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 用户注册状态
        if not self.network_manager.is_registered():
            register_action = menu.addAction("用户注册")
            register_action.triggered.connect(self.show_user_registration_dialog)
        else:
            status_action = menu.addAction(f"已注册: {self.network_manager.get_user_id()}")
            status_action.setEnabled(False)
            
        # 好友搜索
        if self.network_manager.is_registered():
            search_action = menu.addAction("好友搜索")
            search_action.triggered.connect(self.show_friend_search_dialog)
            
        menu.addSeparator()
        
        # 移动到右下角
        move_action = menu.addAction("移动到右下角")
        move_action.triggered.connect(self.move_to_bottom_right)
        
        menu.addSeparator()
        
        # 退出
        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(self.close_pet)
        
        menu.exec_(pos)
        
    def control_pet(self, pet_id):
        """控制宠物"""
        if self.my_user_name:
            if pet_id == 1 and not self.pet1_owner:
                self.pet1_owner = self.my_user_name
                QMessageBox.information(self, "控制成功", f"你现在控制小狗{pet_id}")
            elif pet_id == 2 and not self.pet2_owner:
                self.pet2_owner = self.my_user_name
                QMessageBox.information(self, "控制成功", f"你现在控制小狗{pet_id}")
            else:
                QMessageBox.warning(self, "控制失败", "这只小狗已经被控制了")
        else:
            QMessageBox.warning(self, "控制失败", "请先进行用户注册")
            
    def set_emotion(self, emotion):
        """设置表情"""
        if self.pet1_owner == self.my_user_name:
            self.pet1_emotion = emotion
            # 发送给所有好友
            self.network_manager.send_pet_action(1, "emotion", emotion)
        elif self.pet2_owner == self.my_user_name:
            self.pet2_emotion = emotion
            # 发送给所有好友
            self.network_manager.send_pet_action(2, "emotion", emotion)
        else:
            QMessageBox.warning(self, "设置失败", "请先控制一只小狗")
            
        self.update_pets_display()
        
    def set_interaction(self, interaction):
        """设置互动"""
        if self.pet1_owner == self.my_user_name:
            self.network_manager.send_pet_action(1, "interaction", interaction)
        elif self.pet2_owner == self.my_user_name:
            self.network_manager.send_pet_action(2, "interaction", interaction)
        else:
            QMessageBox.warning(self, "互动失败", "请先控制一只小狗")
            
    def show_user_registration_dialog(self):
        """显示用户注册对话框"""
        dialog = UserRegistrationDialog(self)
        dialog.registration_requested.connect(self.register_user)
        dialog.exec_()
        
    def register_user(self, user_id: str, user_name: str):
        """注册用户"""
        self.my_user_name = user_name
        
        # 尝试注册用户
        if self.network_manager.register_user(user_id, user_name):
            QMessageBox.information(self, "注册成功", f"用户注册成功: {user_id}")
        else:
            QMessageBox.warning(self, "注册失败", "无法注册用户，请检查网络连接")
            
    def show_friend_search_dialog(self):
        """显示好友搜索对话框"""
        dialog = FriendSearchDialog(self.network_manager, self)
        dialog.friend_request_sent.connect(self.send_friend_request)
        dialog.exec_()
        
    def send_friend_request(self, target_user_id: str, message: str):
        """发送好友申请"""
        if self.network_manager.send_friend_request(target_user_id, message):
            QMessageBox.information(self, "申请发送", f"已向用户 {target_user_id} 发送好友申请")
        else:
            QMessageBox.warning(self, "发送失败", "发送好友申请失败")
            
    def on_registration_status_changed(self, registered):
        """注册状态改变"""
        if registered:
            print("用户注册成功")
        else:
            print("用户注册失败")
            
    def on_friend_request_received(self, from_user_id, from_user_name, message):
        """收到好友申请"""
        reply = QMessageBox.question(self, "好友申请", 
                                   f"收到来自 {from_user_name} ({from_user_id}) 的好友申请：\n{message}\n\n是否接受？",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.network_manager.accept_friend_request(from_user_id):
                QMessageBox.information(self, "接受成功", f"已接受 {from_user_name} 的好友申请")
            else:
                QMessageBox.warning(self, "接受失败", "接受好友申请失败")
                
    def on_friend_status_changed(self, friend_id, online):
        """好友状态改变"""
        if online:
            print(f"好友 {friend_id} 上线了")
        else:
            print(f"好友 {friend_id} 下线了")
            
    def on_pet_action_received(self, pet_id, action_type, action_data):
        """接收到宠物动作"""
        if action_type == "control":
            if pet_id == 1:
                self.pet1_owner = action_data
            elif pet_id == 2:
                self.pet2_owner = action_data
        elif action_type == "emotion":
            if pet_id == 1:
                self.pet1_emotion = action_data
            elif pet_id == 2:
                self.pet2_emotion = action_data
                
        self.update_pets_display()
        
    def create_system_tray(self):
        """创建系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("pets"))  # 使用系统图标
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("显示桌宠")
        show_action.triggered.connect(self.show)
        
        hide_action = tray_menu.addAction("隐藏桌宠")
        hide_action.triggered.connect(self.hide)
        
        tray_menu.addSeparator()
        
        exit_action = tray_menu.addAction("退出")
        exit_action.triggered.connect(self.close_pet)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def close_pet(self):
        """关闭桌宠"""
        self._closing = True
        self.network_manager.disconnect()
        self.close()
        
    def closeEvent(self, event):
        """关闭事件"""
        self._closing = True
        self.network_manager.disconnect()
        QApplication.quit()
        event.accept() 