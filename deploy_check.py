#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署检查脚本 - 验证Render部署所需文件
"""

import os
import sys

def check_deployment_files():
    """检查部署所需文件"""
    print("🔍 检查Render部署文件...")
    print("=" * 50)
    
    required_files = [
        'friend_server.py',
        'requirements_server.txt', 
        'render.yaml'
    ]
    
    all_files_exist = True
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - 文件不存在")
            all_files_exist = False
    
    print("\n" + "=" * 50)
    if all_files_exist:
        print("🎉 所有部署文件已准备就绪！")
        return True
    else:
        print("⚠️  请确保所有必需文件都存在")
        return False

def check_server_code():
    """检查服务器代码"""
    print("\n🔍 检查服务器代码...")
    print("=" * 50)
    
    try:
        with open('friend_server.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ('Flask应用', 'app = Flask(__name__)' in content),
            ('端口配置', 'os.environ.get(\'PORT\'' in content),
            ('导入os模块', 'import os' in content),
            ('gunicorn兼容', 'app.run' in content)
        ]
        
        all_checks_passed = True
        for check_name, passed in checks:
            if passed:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
                all_checks_passed = False
        
        return all_checks_passed
        
    except Exception as e:
        print(f"❌ 无法读取服务器代码: {e}")
        return False

def check_requirements():
    """检查依赖文件"""
    print("\n🔍 检查依赖文件...")
    print("=" * 50)
    
    try:
        with open('requirements_server.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_packages = ['Flask', 'gunicorn']
        all_packages_found = True
        
        for package in required_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - 未找到")
                all_packages_found = False
        
        return all_packages_found
        
    except Exception as e:
        print(f"❌ 无法读取依赖文件: {e}")
        return False

def generate_deployment_guide():
    """生成部署指南"""
    print("\n📋 Render部署步骤:")
    print("=" * 50)
    print("1. 访问 https://render.com 注册账户")
    print("2. 点击 'New +' 创建新的Web Service")
    print("3. 连接你的GitHub仓库")
    print("4. 配置服务设置:")
    print("   - Name: lovepetty-friend-server")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements_server.txt")
    print("   - Start Command: gunicorn friend_server:app --bind 0.0.0.0:$PORT")
    print("5. 点击 'Create Web Service' 开始部署")
    print("6. 等待部署完成，获取服务URL")
    print("7. 更新客户端代码中的服务器URL")

def main():
    """主函数"""
    print("🚀 LovePetty Render部署检查")
    print("=" * 50)
    
    # 检查文件
    files_ok = check_deployment_files()
    
    if files_ok:
        # 检查代码
        code_ok = check_server_code()
        req_ok = check_requirements()
        
        if code_ok and req_ok:
            print("\n🎉 所有检查通过！可以开始部署了。")
            generate_deployment_guide()
        else:
            print("\n⚠️  代码检查未通过，请修复问题后重试。")
    else:
        print("\n❌ 文件检查未通过，请确保所有必需文件都存在。")

if __name__ == "__main__":
    main() 