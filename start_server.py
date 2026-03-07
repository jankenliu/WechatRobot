# -*- coding: utf-8 -*-
"""
快速启动脚本 - 启动微信 Hook HTTP 服务器
"""

import sys
import os

def main():
    """主函数"""
    print("=" * 60)
    print("微信 Hook HTTP 服务器")
    print("=" * 60)
    
    # 默认配置
    default_port = 9999
    default_host = "0.0.0.0"  # 绑定所有网络接口，支持本地和局域网访问
    
    # 解析命令行参数
    port = default_port
    host = default_host
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"❌ 无效的端口号：{sys.argv[1]}")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    print(f"📡 监听地址：http://{host}:{port}")
    print(f"🌐 可访问地址:")
    print(f"   - 本地访问：http://localhost:{port}")
    print(f"   - 局域网访问：http://<本机 IP>:{port} (如：http://192.168.1.111:{port})")
    print(f"🔍 测试接口：GET /test")
    print(f"📍 发送微信消息接口：POST /wxSend {{\"target\": \"聊天对象名\", \"content\": \"消息内容\"}}")
    print("=" * 60)
    print()
    
    # 导入并运行服务器
    from wechat_hook_server import run_server
    run_server(host, port)


if __name__ == "__main__":
    main()
