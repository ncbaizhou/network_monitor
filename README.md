1️⃣ README.md（直接复制到GitHub仓库）
Markdown
编辑
# 🌐 网络健康监测仪 | Network Health Monitor

一个**超实用**的Python脚本，用于监控多台主机的网络状态，用**友好名称**代替难记的IP，**状态一目了然**！

![运行效果](https://raw.githubusercontent.com/ncbaizhou/network_monitor/refs/heads/main/%E6%88%AA%E5%9B%BE.png)

## 🔥 核心亮点
- ✅ **名称代替IP**：用“服务器71”代替 `172.17.2.1`
- ✅ **状态emoji**：🟢=快 / 🟠=慢 / 🔴=丢包
- ✅ **两行对齐显示**：主机名+状态在上，IP在下（再也不用对齐分隔符！）
- ✅ **完全兼容**：支持旧XML/文本文件配置（无需修改旧配置）

## 🛠️ 快速上手

### 1️⃣ 安装依赖
```bash
# 确保已安装Python 3.x（推荐3.7+）
python --version
2️⃣ 配置主机列表
复制示例文件：
Bash
编辑
copy hosts.example.xml hosts.xml  # Windows
cp hosts.example.xml hosts.xml    # macOS/Linux
编辑hosts.xml（用VS Code或记事本都可以，我自己用notepad--）：
Xml
编辑
<?xml version="1.0" encoding="UTF-8"?>
<hosts>
    <!-- 用你的名称替换IP（如：服务器71） -->
    <host name="百度">www.baidu.com</host>
    <host name="服务器71">172.17.2.1</host>
    <host name="阿里DNS">223.5.5.5</host>
</hosts>
3️⃣ 运行监控
Bash
编辑
python ping_monitor.py hosts.xml
💡 提示：按 Ctrl + C 停止监控

4️⃣ 查看历史日志
日志自动保存在 ping_log_YYYYMMDD.txt
示例内容：
Text
编辑
12:30:05 | 百度 | www.baidu.com | 🟢 23ms
12:30:05 | 服务器71 | 172.17.2.1 | 🟢 15ms
🌐 为什么推荐这个项目？
中文友好：所有提示语、日志都用中文
零配置：直接运行，无需安装额外库
企业级设计：支持公司内网设备监控（如财务系统、数据库）
📜 开源许可
本项目采用 MIT License，允许任何人自由使用、修改和分享（详见 LICENSE 文件）。
