# 使用说明
建议使用uv来管理pyhon并执行，本项目基于python3.14测试的
```shell
# 测试个人微信进程及窗口状态
uv run wechat_sender_v3.py test
# 调试个人微信进程及窗口信息
uv run wechat_sender_v3.py debug
# 发送微信群消息
uv run wechat_sender_v3.py send [群名]
```