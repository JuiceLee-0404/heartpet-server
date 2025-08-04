# 服务器部署说明

## 部署到Render

### 1. 准备文件

创建以下文件用于部署：

#### requirements.txt
```
Flask==2.3.3
gunicorn==21.2.0
```

#### render.yaml
```yaml
services:
  - type: web
    name: lovepetty-friend-server
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn friend_server:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
```

### 2. 部署步骤

1. 注册Render账户：https://render.com
2. 创建新的Web Service
3. 连接GitHub仓库
4. 上传服务器代码
5. 配置环境变量
6. 部署服务

### 3. 更新客户端配置

部署成功后，更新客户端中的服务器URL：

```python
# 在 friend_network_manager.py 中更新
self.server_url = "https://your-app-name.onrender.com"
```

## 本地测试服务器

### 1. 安装依赖
```bash
pip install flask gunicorn
```

### 2. 运行服务器
```bash
python friend_server.py
```

### 3. 测试API
```bash
# 测试首页
curl http://localhost:10000/

# 测试用户注册
curl -X POST http://localhost:10000/register_user \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U12345678", "user_name": "测试用户"}'

# 测试搜索用户
curl http://localhost:10000/search_user?user_id=U12345678
```

## API接口说明

### 1. 用户注册接口
- **URL**: `/register_user`
- **方法**: POST
- **参数**: 
  - `user_id`: 用户ID
  - `user_name`: 用户名
- **返回**: 注册结果

### 2. 搜索用户接口
- **URL**: `/search_user`
- **方法**: GET
- **参数**: 
  - `user_id`: 要搜索的用户ID
- **返回**: 用户信息

### 3. 发送好友申请
- **URL**: `/send_friend_request`
- **方法**: POST
- **参数**: 
  - `from_user_id`: 发送者用户ID
  - `from_user_name`: 发送者用户名
  - `to_user_id`: 接收者用户ID
  - `message`: 申请消息
- **返回**: 发送结果

### 4. 接受好友申请
- **URL**: `/accept_friend_request`
- **方法**: POST
- **参数**: 
  - `from_user_id`: 申请者用户ID
  - `to_user_id`: 接受者用户ID
- **返回**: 接受结果

### 5. 获取好友列表
- **URL**: `/friends`
- **方法**: GET
- **参数**: 
  - `user_id`: 用户ID
- **返回**: 好友列表

### 6. 获取好友状态
- **URL**: `/friends_status`
- **方法**: GET
- **参数**: 
  - `user_id`: 用户ID
- **返回**: 好友在线状态

### 7. 发送消息
- **URL**: `/send`
- **方法**: POST
- **参数**: 
  - `user_id`: 发送者用户ID
  - `type`: 消息类型
  - `target_user_id`: 目标用户ID（可选）
  - 其他消息数据
- **返回**: 发送结果

### 8. 获取消息
- **URL**: `/messages`
- **方法**: GET
- **参数**: 
  - `user_id`: 用户ID
  - `timestamp`: 时间戳
- **返回**: 新消息列表

### 9. 心跳包
- **URL**: `/heartbeat`
- **方法**: POST
- **参数**: 
  - `user_id`: 用户ID
- **返回**: 心跳结果

## 安全考虑

1. **数据加密**: 建议在生产环境中使用HTTPS
2. **身份验证**: 可以添加JWT token验证
3. **数据持久化**: 使用数据库存储用户和消息数据
4. **速率限制**: 防止API滥用
5. **日志记录**: 记录访问和错误日志

## 扩展功能

1. **数据库集成**: 使用PostgreSQL或MongoDB
2. **实时通信**: 集成WebSocket支持
3. **文件上传**: 支持图片和文件分享
4. **消息加密**: 端到端加密
5. **多语言支持**: 国际化支持
6. **用户管理**: 用户资料、头像等
7. **群组功能**: 支持群组聊天
8. **消息历史**: 保存聊天记录 