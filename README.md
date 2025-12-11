# 🌐 网络健康监测仪 | Network Health Monitor

这个脚本主要是借助阿里千问完成。
This script is mainly completed with the help of Alibaba Qianwen.

一个**超实用**的Python脚本，用于监控多台主机的网络状态，用**友好名称**代替难记的IP，**状态一目了然**！
A **super useful** Python script for monitoring the network status of multiple hosts, replacing hard-to-remember IPs with **friendly names**, **status at a glance**!

![运行效果Running Effect](https://raw.githubusercontent.com/ncbaizhou/network_monitor/refs/heads/main/%E6%88%AA%E5%9B%BE.png)

## 🔥 核心亮点 Core Highlights
- ✅ **名称代替IP**：用“主机名称”代替 “主机地址”
**Name instead of IP**: Use "Host Name" instead of "Host Address"
- ✅ **状态emoji**：🟢=快 / 🟠=慢 / 🔴=丢包
Status emoji: 🟢 = fast / 🟠 = slow / 🔴 = packet loss
- ✅ **完全兼容**：支持旧XML/文本文件配置（无需修改旧配置）
 **Fully Compatible**: Support for legacy XML/text file configurations (no need to modify old configurations)

## 🛠️ 快速上手 Get started quickly

### 1️⃣ 安装依赖 Install dependencies
# 确保已安装Python Make sure Python is installed
我电脑上的版本为Python 3.13.9，大家可以通过命令查看自己的Python版本
The version on my computer is Python 3.13.9, and you can check your Python version through the command
python --version
### 2️⃣ 配置主机列表 Configure the host list
编辑hosts.xml（用VS Code或记事本都可以，我自己用notepad--）
Edit hosts.xml (using VS Code or Notepad is fine, I use notepad myself--)
<?xml version="1.0" encoding="UTF-8"?>
<hosts>
    <!-- 用你的名称替换IP（如：服务器71） -->
    <host name="百度">www.baidu.com</host>
    <host name="服务器71">172.17.2.1</host>
    <host name="阿里DNS">223.5.5.5</host>
</hosts>
### 3️⃣ 运行监控 Run monitoring
python ping_monitor.py hosts.xml
或者直接运行其中的“一键运行.bat”即可，因此也可以添加到计划任务当中
Or just run the "One-click Run .bat" in it, so it can also be added to the scheduled task
💡 提示：按 Ctrl + C 停止监控
Tip: Press Ctrl C to stop monitoring

### 4️⃣ 查看历史日志 View the history log
日志自动保存在 ping_log_YYYYMMDD.txt
Logs are automatically saved in ping_log_YYYYMMDD.txt
示例内容 Example content：
12:30:05 | 百度 | www.baidu.com | 🟢 23ms
12:30:05 | Server 71 | 172.17.2.1 | 🟢 15ms

# 🌐 为什么推荐这个项目？ Why is this project recommended?
中文友好：所有提示语、日志都用中文
  Chinese friendly: All prompts and logs are in Chinese
零配置：直接运行，无需安装额外库
  Zero configuration: Runs directly without installing additional libraries
企业级设计：支持公司内网设备监控（如财务系统、数据库）
  Enterprise-level design: support the monitoring of intranet devices (such as financial systems, databases)

# 📜 开源许可 Open source license
本项目采用 MIT License，允许任何人自由使用、修改和分享（详见 LICENSE 文件）。
This project is licensed under the MIT License, which allows anyone to freely use, modify, and share it (see LICENSE document for details).

# 如果你觉得这个脚本有用，欢迎(If you find this script useful, feel free to)：
Star仓库 ⭐ Star the repository ️
提交Issue（发现bug或建议） Submit an Issue (if you find a bug or have suggestions)  
PR贡献（优化代码） Contribute via PR (to optimize the code)

