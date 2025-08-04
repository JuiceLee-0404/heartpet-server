#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面宠物主程序 - 支持好友申请制
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from pet_window import PetWindow

def main():
    """主程序入口"""
    # 创建Qt应用
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("LovePetty")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("LovePetty")
    
    # 创建桌面宠物窗口
    pet_window = PetWindow()
    pet_window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 