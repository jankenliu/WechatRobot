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
    default_host = "localhost"
    
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
    print(f"📍 API 端点：POST /wxSend")
    print(f"📋 请求体：{{\"target\": \"聊天对象名\", \"content\": \"消息内容\"}}")
    print("=" * 60)
    print()
    print("使用示例:")
    print(f"  curl -X POST http://{host}:{port}/wxSend \\")
    print(f"    -H \"Content-Type: application/json\" \\")
    print(f"    -d '{{\"target\":\"文件传输助手\",\"content\":\"你好\"}}'")
    print()
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    print()
    
    # 导入并运行服务器
    from wechat_hook_server import run_server
    run_server(host, port)


if __name__ == "__main__":
    main()
