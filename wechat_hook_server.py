# -*- coding: utf-8 -*-
"""
微信消息 HTTP Hook 接口
版本：v1.0.0
创建日期：2026-03-08
功能：提供 HTTP 接口接收 POST 请求来发送微信消息
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any
import threading

from wechat_sender_v3 import WeChatSenderV3

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeChatHookHandler(BaseHTTPRequestHandler):
    """微信 Hook HTTP 请求处理器"""
    
    # 类级别的发送器实例（延迟初始化）
    _sender = None
    _sender_lock = threading.Lock()
    
    def log_message(self, format, *args):
        """重写日志方法，使用我们的日志系统"""
        logger.info(f"HTTP 请求：{args[0]}")
    
    def _get_sender(self) -> WeChatSenderV3:
        """获取或创建微信发送器实例"""
        if WeChatHookHandler._sender is None:
            with WeChatHookHandler._sender_lock:
                if WeChatHookHandler._sender is None:
                    WeChatHookHandler._sender = WeChatSenderV3()
        return WeChatHookHandler._sender
    
    def _send_cors_headers(self):
        """发送 CORS 跨域头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """处理 OPTIONS 预检请求"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_POST(self):
        """处理 POST 请求"""
        try:
            # 解析 URL 路径
            parsed_path = urlparse(self.path)
            
            # 验证路径格式：/wxSend
            if parsed_path.path.strip('/') != 'wxSend':
                self._send_error_response("无效的路径格式", "路径应为：/wxSend")
                return
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response("缺少请求体", "请求体不能为空")
                return
            
            request_body = self.rfile.read(content_length).decode('utf-8')
            
            # 解析 JSON
            try:
                data = json.loads(request_body)
            except json.JSONDecodeError as e:
                self._send_error_response(f"JSON 解析失败", str(e))
                return
            
            # 验证必需的字段
            if 'target' not in data:
                self._send_error_response("缺少必需字段", "请求体必须包含'target'字段（聊天对象名）")
                return
            
            if 'content' not in data:
                self._send_error_response("缺少必需字段", "请求体必须包含'content'字段（消息内容）")
                return
            
            chat_target = data['target']
            message_content = data['content']
            
            # 验证参数
            if not chat_target or not isinstance(chat_target, str):
                self._send_error_response("无效的聊天对象名", "target 必须是非空字符串")
                return
            
            if not message_content or not isinstance(message_content, str):
                self._send_error_response("无效的消息内容", "content 必须是非空字符串")
                return
            
            logger.info(f"收到发送请求：目标={chat_target}, 消息长度={len(message_content)}")
            
            # 发送微信消息
            sender = self._get_sender()
            success = sender.send_text(message_content, chat_target)
            
            if success:
                logger.info(f"消息发送成功：{chat_target}")
                self._send_success_response({
                    "status": "success",
                    "message": "消息发送成功",
                    "target": chat_target,
                    "content_length": len(message_content)
                })
            else:
                logger.error(f"消息发送失败：{chat_target}")
                self._send_error_response(
                    "消息发送失败",
                    "微信消息发送失败，请检查微信是否正常运行",
                    status_code=500
                )
        
        except Exception as e:
            logger.error(f"处理请求失败：{e}", exc_info=True)
            self._send_error_response("服务器内部错误", str(e), status_code=500)
    
    def do_GET(self):
        """处理 GET 请求（用于健康检查）"""
        try:
            parsed_path = urlparse(self.path)
            
            # 只保留根路径的健康检查
            if parsed_path.path == '/':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                
                response = {
                    "service": "WeChat Hook API",
                    "version": "1.0.0",
                    "endpoint": "POST /wxSend",
                    "example": {
                        "url": "http://localhost:9999/wxSend",
                        "body": {
                            "target": "文件传输助手",
                            "content": "Hello, World!"
                        }
                    }
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # 其他路径返回 404
            self._send_error_response("未找到请求的资源", f"未知路径：{parsed_path.path}")
        
        except Exception as e:
            logger.error(f"处理 GET 请求失败：{e}", exc_info=True)
            self._send_error_response("服务器内部错误", str(e), status_code=500)
    
    def _send_success_response(self, data: Dict[str, Any]):
        """发送成功的 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._send_cors_headers()
        self.end_headers()
        
        response = {
            "code": 0,
            **data
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def _send_error_response(self, error: str, details: str = None, status_code: int = 400):
        """发送错误的 JSON 响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._send_cors_headers()
        self.end_headers()
        
        response = {
            "code": 1,
            "error": error
        }
        if details:
            response["details"] = details
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))


def run_server(host: str = 'localhost', port: int = 9999):
    """运行 HTTP 服务器"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, WeChatHookHandler)
    
    logger.info(f"正在启动微信 Hook HTTP 服务器...")
    logger.info(f"监听地址：http://{host}:{port}")
    logger.info(f"API 端点：POST /wxSend")
    logger.info(f"请求体：{{\"target\": \"聊天对象名\", \"content\": \"消息内容\"}}")
    logger.info(f"按 Ctrl+C 停止服务")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭服务器...")
        httpd.shutdown()
        logger.info("服务器已关闭")


def main():
    """主程序入口"""
    import sys
    
    # 默认配置
    default_host = 'localhost'
    default_port = 9999
    
    # 解析命令行参数
    host = default_host
    port = default_port
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"无效的端口号：{sys.argv[1]}")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    # 启动服务器
    run_server(host, port)


if __name__ == "__main__":
    main()
