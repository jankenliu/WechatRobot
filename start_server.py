# -*- coding: utf-8 -*-
"""
快速启动脚本 - 启动微信 Hook HTTP 服务器
"""

import sys

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
    print(f"🔍 测试接口：GET /test")
    print(f"📍 发送微信文字消息接口：POST /wxSend {{\"target\": \"聊天对象名\", \"content\": \"消息内容\"}}")
    print(f"📍 发送微信文件消息接口：POST /wxSend {{\"target\": \"聊天对象名\", \"file\": \"文件路径(本地路径C:\\\\图片\\\\xxx.png 或 URL https://example.com/xxx.png)\"}}")
    print()
    print(f"🔔！！！请务必首先手动的在PC微信当中 ctrl+f 输入每一个需要自动化的完整的 [聊天对象名：如文件传输助手]，并点击进入该对话框，先将搜索进行缓存，以便于程序执行 ctrl+f 搜索 [聊天对象名] 时，搜索结果第一个就是目标聊天对象")
    print("=" * 60)
    print()
    
    # 导入并运行服务器
    from wechat_hook_server import run_server
    run_server(host, port)


if __name__ == "__main__":
    main()
