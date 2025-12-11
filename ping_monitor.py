# -*- coding: utf-8 -*-
import os
import re
import time
from datetime import datetime
import subprocess
import sys
import xml.etree.ElementTree as ET

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
    if len(sys.argv) < 2:
        print("用法：python ping_monitor.py <hosts.txt或hosts.xml>")
        print("示例：python ping_monitor.py network_hosts.xml")
        return
    
    hosts = load_hosts(sys.argv[1])
    log_file = f"ping_log_{datetime.now().strftime('%Y%m%d')}.txt"
    
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
                
                # ✅ 两行对齐显示（关键优化！）
                print(f"主机: {name.ljust(15)}{status_line}")
                print(f"IP:   {ip.ljust(15)}")
                
                # 日志记录（保持原有格式）
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"{datetime.now().strftime('%H:%M:%S')} | {name} | {ip} | {status_line}\n")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 监控已停止，感谢使用！")

if __name__ == "__main__":
    main()
