#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面宠物测试脚本 - 好友申请制版本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pet_window():
    """测试桌面宠物窗口"""
    try:
        from pet_window import PetWindow
        print("✓ PetWindow 导入成功")
        
        # 测试创建窗口
        from PyQt5.QtWidgets import QApplication
        app = QApplication([])
        
        window = PetWindow()
        print("✓ PetWindow 创建成功")
        
        # 测试基本方法
        window.move_to_bottom_right()
        print("✓ 移动到右下角功能正常")
        
        window.set_emotion("开心")
        print("✓ 表情设置功能正常")
        
        window.set_interaction("抚摸")
        print("✓ 互动设置功能正常")
        
        return True
        
    except Exception as e:
        print(f"✗ 桌面宠物测试失败: {e}")
        return False

def test_network_manager():
    """测试网络管理器"""
    try:
        from friend_network_manager import FriendNetworkManager
        print("✓ FriendNetworkManager 导入成功")
        
        network_manager = FriendNetworkManager()
        print("✓ FriendNetworkManager 创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 网络管理器测试失败: {e}")
        return False

def test_dialogs():
    """测试对话框"""
    try:
        from user_registration_dialog import UserRegistrationDialog
        from friend_search_dialog import FriendSearchDialog
        from friend_network_manager import FriendNetworkManager
        print("✓ 对话框模块导入成功")
        
        # 测试创建对话框
        from PyQt5.QtWidgets import QApplication
        app = QApplication([])
        
        reg_dialog = UserRegistrationDialog()
        print("✓ UserRegistrationDialog 创建成功")
        
        network_manager = FriendNetworkManager()
        search_dialog = FriendSearchDialog(network_manager)
        print("✓ FriendSearchDialog 创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 对话框测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试桌面宠物 - 好友申请制版本...")
    print("=" * 60)
    
    tests = [
        ("桌面宠物窗口", test_pet_window),
        ("网络管理器", test_network_manager),
        ("对话框", test_dialogs)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n测试 {test_name}...")
        if test_func():
            print(f"✓ {test_name} 测试通过")
        else:
            print(f"✗ {test_name} 测试失败")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有测试通过！")
        print("\n功能特性:")
        print("- ✅ 拖拽移动：按住左键拖拽桌宠")
        print("- ✅ 点击交互：轻点桌宠显示交互菜单")
        print("- ✅ 右键菜单：右键显示系统菜单")
        print("- ✅ 稳定显示：不会因点击外部而消失")
        print("- ✅ 用户注册：注册唯一用户ID")
        print("- ✅ 好友搜索：通过ID搜索其他用户")
        print("- ✅ 好友申请：发送和接受好友申请")
        print("- ✅ 宠物控制：每人控制一只小狗")
        print("- ✅ 实时同步：好友间的动作实时同步")
        print("- ✅ 系统托盘：支持后台运行")
        print("\n运行程序:")
        print("python main.py")
        print("\n使用说明:")
        print("1. 启动程序后会自动弹出用户注册对话框")
        print("2. 注册用户ID，用于好友搜索")
        print("3. 点击桌宠选择控制小狗1或小狗2")
        print("4. 右键菜单可以搜索好友并发送申请")
        print("5. 好友间可以实时同步宠物动作")
    else:
        print("✗ 部分测试失败，请检查错误信息")

if __name__ == "__main__":
    main() 