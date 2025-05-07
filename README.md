# WeibanHelper (适用于2025春季课程)
安全微课自动化助手

## 项目简介
WeibanHelper 是一个用于自动化完成安全微课学习任务的Python脚本工具。本工具仅供学习交流使用，请勿用于其他用途。

## 功能特点
- 自动遍历所有课程分类
- 自动完成课程学习
- 自动处理验证码
- 进度条显示学习状态
- 支持断点续学

## 下载与安装
1. 克隆仓库
```bash
git clone https://github.com/Julian-hob/WeibanHelper.git
cd WeibanHelper
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法
1. 获取个人配置信息
   - 登录安全微课网站
   - 打开浏览器开发者工具(F12)
   - 在网络请求中找到以下信息：
     - User-Agent
     - user_id
     - user_project_id
     - cookie
     - x_token
     - tenant_code
     - user_name

2. 配置信息
   - 打开 `WeibanHelper.py`
   - 修改 `user_config` 中的配置信息

3. 运行脚本
```bash
python WeibanHelper.py
```

## 配置示例
```python
user_config = {
    'User-Agent': '你的User-Agent'
    'user_id': '你的user_id',
    'user_project_id': '你的user_project_id',
    'cookie': '你的cookie',
    'user_name': '你的user_name',
    'x_token': '你的x_token',
    'tenant_code': '你的tenant_code'
}
```

## 注意事项
- 本工具仅供学习交流使用
- 使用前请确保已完成实名认证
- 建议适度使用，避免频繁请求
- 请遵守相关规定和法律法规

## 依赖库
- requests
- tqdm
- json

## 更新日志
- 2025.05.07: 初始版本发布，支持2025春季课程

## 免责声明
本项目仅供学习交流使用，使用本工具产生的任何后果由使用者自行承担。

## 贡献
欢迎提交Issue和Pull Request来帮助改进这个项目。
