# Render部署教程 - LovePetty好友服务器

## 📋 部署前准备

### 1. 注册Render账户
- 访问 https://render.com
- 点击 "Get Started" 注册账户
- 可以使用GitHub账户直接登录

### 2. 准备代码仓库
确保你的项目包含以下文件：
- `friend_server.py` - 服务器代码
- `requirements_server.txt` - 服务器依赖
- `render.yaml` - Render配置文件

## 🚀 部署步骤

### 第一步：创建新的Web Service

1. **登录Render Dashboard**
   - 进入 https://dashboard.render.com
   - 点击 "New +" 按钮

2. **选择服务类型**
   - 选择 "Web Service"
   - 点击 "Connect" 连接你的GitHub仓库

3. **配置仓库**
   - 选择包含LovePetty代码的仓库
   - 选择要部署的分支（通常是main或master）

### 第二步：配置服务设置

1. **基本信息**
   - **Name**: `lovepetty-friend-server`
   - **Environment**: `Python 3`
   - **Region**: 选择离你最近的区域（如US East）

2. **构建配置**
   - **Build Command**: `pip install -r requirements_server.txt`
   - **Start Command**: `gunicorn friend_server:app --bind 0.0.0.0:$PORT`

3. **环境变量**
   - 点击 "Advanced" 展开高级选项
   - 添加环境变量：
     - `PYTHON_VERSION`: `3.9.16`

### 第三步：部署服务

1. **创建服务**
   - 点击 "Create Web Service"
   - Render会自动开始构建和部署

2. **等待部署完成**
   - 构建过程通常需要2-5分钟
   - 可以在日志中查看构建进度

3. **获取服务URL**
   - 部署成功后，你会得到一个URL
   - 格式类似：`https://lovepetty-friend-server.onrender.com`

## 🔧 配置客户端

### 更新客户端服务器URL

部署成功后，需要更新客户端代码中的服务器地址：

```python
# 在 friend_network_manager.py 中修改
self.server_url = "https://your-app-name.onrender.com"
```

将 `your-app-name` 替换为你的实际服务名称。

## 📊 监控和管理

### 查看服务状态
- 在Render Dashboard中可以看到服务状态
- 绿色表示运行正常，红色表示有错误

### 查看日志
- 点击服务名称进入详情页
- 在 "Logs" 标签页查看运行日志
- 可以实时监控API请求和错误信息

### 重启服务
- 在服务详情页点击 "Manual Deploy"
- 选择 "Clear build cache & deploy" 完全重新部署

## 🧪 测试部署

### 测试API接口

部署完成后，可以使用以下命令测试：

```bash
# 测试首页
curl https://your-app-name.onrender.com/

# 测试用户注册
curl -X POST https://your-app-name.onrender.com/register_user \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U12345678", "user_name": "测试用户"}'

# 测试搜索用户
curl https://your-app-name.onrender.com/search_user?user_id=U12345678
```

### 在客户端测试
1. 更新客户端代码中的服务器URL
2. 运行 `python main.py`
3. 尝试注册用户和搜索功能

## ⚠️ 注意事项

### 免费计划限制
- Render免费计划有每月使用时间限制
- 服务在15分钟无请求后会自动休眠
- 首次请求可能需要等待服务启动（约30秒）

### 数据持久化
- 当前版本使用内存存储，重启后数据会丢失
- 生产环境建议使用数据库（如PostgreSQL）

### 安全考虑
- 免费计划使用HTTPS
- 建议添加身份验证和速率限制
- 定期备份重要数据

## 🔄 更新部署

### 代码更新
1. 将修改后的代码推送到GitHub
2. Render会自动检测到代码变更
3. 自动开始新的部署流程

### 手动重新部署
1. 在服务详情页点击 "Manual Deploy"
2. 选择部署类型：
   - "Deploy latest commit" - 部署最新代码
   - "Clear build cache & deploy" - 清除缓存并重新部署

## 📞 故障排除

### 常见问题

#### 1. 构建失败
**问题**: 构建过程中出现错误
**解决**:
- 检查 `requirements_server.txt` 文件是否正确
- 确认Python版本兼容性
- 查看构建日志中的具体错误信息

#### 2. 服务无法启动
**问题**: 服务启动失败
**解决**:
- 检查 `startCommand` 是否正确
- 确认 `friend_server.py` 中的 `app` 对象存在
- 查看启动日志

#### 3. API请求失败
**问题**: 客户端无法连接到服务器
**解决**:
- 确认服务器URL正确
- 检查网络连接
- 验证API接口路径

### 获取帮助
- 查看Render官方文档：https://render.com/docs
- 在Render社区寻求帮助
- 检查服务日志获取详细错误信息

## 🎉 部署完成

部署成功后，你的LovePetty好友服务器就可以为客户端提供服务了！

### 验证部署
1. 访问你的服务URL
2. 应该看到欢迎页面
3. 测试API接口功能
4. 更新客户端配置

---

**恭喜！** 你的LovePetty好友服务器已经成功部署到Render！🎉 