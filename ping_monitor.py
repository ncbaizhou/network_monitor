# -*- coding: utf-8 -*-
import os
import re
import time
from datetime import datetime
import subprocess
import sys
import xml.etree.ElementTree as ET
import socket
    
    # 原有ping逻辑...

def load_hosts(file_path):
    """加载主机列表，支持txt/xml格式（新增名称支持）"""
    if not os.path.exists(file_path):
        print(f"❌ 错误：文件 {file_path} 不存在！")
        sys.exit(1)
    
    if file_path.endswith('.txt'):
        hosts = []
        with open(file_path, 'r') as f:
            for line in f:
                ip = line.strip()
                if ip:
                    hosts.append((ip, ip))
        print(f"✅ 已加载 {len(hosts)} 个主机（TXT格式）")
        return hosts
    
    elif file_path.endswith('.xml'):
        try:
            tree = ET.parse(file_path)
            hosts = []
            for host in tree.findall('.//host'):
                ip = host.text.strip() if host.text else ""
                name = host.get('name', ip) if ip else ""
                if ip:
                    hosts.append((name, ip))
            print(f"✅ 已加载 {len(hosts)} 个主机（XML格式）")
            return hosts
        except Exception as e:
            print(f"❌ XML解析失败：{e}")
            sys.exit(1)
    
    else:
        print("❌ 错误：只支持 .txt 或 .xml 文件！")
        sys.exit(1)

def ping_host(host_ip):
    """执行单次ping，返回延迟(ms)或None（丢包）"""
    # 添加DNS解析检查
    try:
        socket.gethostbyname(host_ip)
    except socket.gaierror:
        print(f"⚠️ 域名解析失败: {host_ip}")
        return None
    
    """执行单次ping，返回延迟(ms)或None（丢包）"""
    cmd = ['ping', '-n', '1', '-w', '1000', host_ip] if os.name == 'nt' else ['ping', '-c', '1', '-i', '0.5', host_ip]
    
    try:
        if os.name == 'nt':
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=1.5).decode('gbk', errors='ignore')
        else:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=1.5).decode('utf-8')
    except Exception as e:
        print(f"⚠️ Ping命令执行失败: {e}")
        return None
    
    if os.name == 'nt':
        # 修复：同时匹配 "时间=1ms" 和 "时间<1ms"
        match = re.search(r'时间\s*=?<?\s*(\d+)', output)
        if match:
            return int(match.group(1))
        # 其他可能的匹配（保留）
        match = re.search(r'time\s*=\s*(\d+)', output, re.IGNORECASE)
        if match:
            return int(match.group(1))

def main():
    # 创建日志目录（如果不存在）
    log_dir = "network_logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"ping_log_{datetime.now().strftime('%Y%m%d')}.txt")
    
    if len(sys.argv) < 2:
        print("用法：python ping_monitor.py <hosts.txt或hosts.xml>")
        print("示例：python ping_monitor.py network_hosts.xml")
        return
    
    hosts = load_hosts(sys.argv[1])
    log_file = f"ping_log_{datetime.now().strftime('%Y%m%d')}.txt"
    
    # 初始化缓存（内存存储未写入的日志）
    log_cache = []
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
                
                # 状态判断
                if delay is None:
                    status_line = "❌ 丢包"
                    emoji = "🔴"
                elif delay < 50:
                    status_line = f"🟢 {delay}ms"
                else:
                    status_line = f"🟠 {delay}ms"
                
                # ✅ 修改：将所有信息合并为一行显示
                print(f"{name.ljust(15)} | {ip.ljust(15)} | {status_line}")
                
                # ✅ 生成日志字符串并缓存（不立即写入文件）
                log_entry = f"{datetime.now().strftime('%H:%M:%S')} | {name} | {ip} | {status_line}\n"
                log_cache.append(log_entry)
                
                # 保持缓存大小不超过MAX_CACHE_SIZE
                if len(log_cache) > MAX_CACHE_SIZE:
                    log_cache.pop(0)  # 丢弃最旧记录
    
            # ✅ 每秒尝试写入缓存（关键逻辑）
            try:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.writelines(log_cache)  # 批量写入所有缓存
                log_cache = []  # 写入成功后清空缓存
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
