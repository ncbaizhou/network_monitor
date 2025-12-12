# -*- coding: utf-8 -*-
import os
import re
import time
from datetime import datetime
import socket
import subprocess
import sys
import xml.etree.ElementTree as ET

def resource_path(relative_path):
    """获取资源路径，兼容开发环境和打包后的 EXE"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def load_hosts():
    # 自动找当前目录下的 hosts.xml
    file_path = resource_path('hosts.xml')
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 找不到 hosts.xml！")
        sys.exit(1)
    
    try:
        root = ET.parse(file_path).getroot()
        hosts = []
        for host in root.findall('host'):
            ip = host.text.strip()
            name = host.get('name', ip)
            if ip:
                hosts.append((name, ip))
        print(f"✅ 自动加载 hosts.xml (路径: {file_path})")
        return hosts
    except Exception as e:
        print(f"❌ 解析 hosts.xml 失败: {e}")
        sys.exit(1)

def ping_host(host_ip):
    """执行单次ping，返回延迟(ms)或错误类型字符串"""
    # ✅ 1. DNS解析失败（独立处理）
    try:
        socket.gethostbyname(host_ip)
    except socket.gaierror:
        return "dns_error"  # 仅返回错误类型，不打印

    # ✅ 2. 执行ping命令
    cmd = ['ping', '-n', '1', '-w', '1000', host_ip] if os.name == 'nt' else ['ping', '-c', '1', '-i', '0.5', host_ip]
    try:
        if os.name == 'nt':
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=1.5).decode('gbk', errors='ignore')
        else:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=1.5).decode('utf-8')
        
        # ✅ 3. 解析延迟（成功）
        if os.name == 'nt':
            match = re.search(r'时间\s*=?<?\s*(\d+)', output)
            if match: return int(match.group(1))
            match = re.search(r'time\s*=\s*(\d+)', output, re.IGNORECASE)
            if match: return int(match.group(1))
        else:
            match = re.search(r'time\s*=\s*(\d+)', output, re.IGNORECASE)
            if match: return int(match.group(1))
        
        # ✅ 4. 解析成功但ping不通（主机不可达）
        return "host_unreachable"
    
    # ✅ 5. 其他错误（如超时、命令不存在）
    except Exception:
        return "unknown_error"

def main():
    hosts = load_hosts() 

    # 创建日志目录（如果不存在）
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 创建主日志文件和错误日志文件
    log_file = os.path.join(log_dir, f"ping_log_{datetime.now().strftime('%Y%m%d')}.txt")
    error_log_file = os.path.join(log_dir, f"error_log_{datetime.now().strftime('%Y%m%d')}.txt")
    
    # 初始化缓存（内存存储未写入的日志）
    log_cache = []      # 主日志缓存
    error_cache = []     # 错误日志缓存
    MAX_CACHE_SIZE = 100  # 最大缓存100条（约100秒数据）
    
    print(f"\n🚀 开始监控！日志将保存到: {log_file}\n")
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"{'='*60}")
            print(f"  网络健康监测仪 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")
            
            for name, ip in hosts:
                delay = ping_host(ip)
                result = ping_host(ip)
                
                # 状态判断
                if result == "dns_error":
                    status_line = "⚠️ 域名解析失败"
                    emoji = "⚠️"
                    # 存入错误日志缓存
                    error_cache.append(f"{datetime.now().strftime('%H:%M:%S')} | {name} | {ip} | {status_line}\n")
                elif result == "host_unreachable":
                    status_line = "🔴 主机不可达"
                    emoji = "🔴"
                    # 存入错误日志缓存
                    error_cache.append(f"{datetime.now().strftime('%H:%M:%S')} | {name} | {ip} | {status_line}\n")
                elif result == "unknown_error":
                    status_line = "❌ 丢包"
                    emoji = "❌"
                    # 存入错误日志缓存
                    error_cache.append(f"{datetime.now().strftime('%H:%M:%S')} | {name} | {ip} | {status_line}\n")
                else:  # 成功
                    delay = result
                    if delay < 50:
                        status_line = f"🟢 {delay}ms"
                    else:
                        status_line = f"🟠 {delay}ms"
                
                # ✅ 将所有信息合并为一行显示
                print(f"{name.ljust(15)} | {ip.ljust(15)} | {status_line}")
                
                # ✅ 生成日志字符串并缓存（不立即写入文件）
                log_entry = f"{datetime.now().strftime('%H:%M:%S')} | {name} | {ip} | {status_line}\n"
                log_cache.append(log_entry)
                
                # 保持缓存大小不超过MAX_CACHE_SIZE
                if len(log_cache) > MAX_CACHE_SIZE:
                    log_cache.pop(0)  # 丢弃最旧记录
    
            # ✅ 每秒尝试写入缓存（关键逻辑）
            try:
                # 主日志保存
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.writelines(log_cache)  # 批量写入所有缓存
                log_cache = []  # 写入成功后清空缓存
                # 错误日志保存
                if error_cache:  # 仅当有错误时才写入
                    with open(error_log_file, 'a', encoding='utf-8') as f:
                        f.writelines(error_cache)
                    error_cache = []
                print("✅ 日志已成功保存到文件")
            except PermissionError:
                # 文件被占用，继续缓存（不中断监控）
                print("⚠️ 日志文件被占用，已缓存当前数据（等待可用）")
            except Exception as e:
                print(f"⚠️ 日志写入错误: {e}")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 监控已停止，感谢使用！")
        
        # 退出前尝试写入剩余缓存
        if log_cache:
            try:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.writelines(log_cache)
                print(f"✅ 退出时已保存 {len(log_cache)} 条缓存日志")
            except:
                print("⚠️ 退出时无法保存缓存日志")

if __name__ == "__main__":
    main()
