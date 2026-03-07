# 使用说明
建议使用uv来管理pyhon并执行，本项目基于 python3.14 测试的
```shell
# 测试个人微信进程及窗口状态
uv run wechat_sender_v3.py test
# 调试个人微信进程及窗口信息
uv run wechat_sender_v3.py debug
# 发送微信群消息
uv run wechat_sender_v3.py send [聊天对象名]
```

# 实现原理
1.激活微信聊天窗口
2.ctrl+f触发搜索操作，并将光标定位到搜索框
3.将待发送的文本存进剪切板，ctrl+a全选搜索框内容，ctrl+v粘贴[聊天对象名]
4.enter回车选择第一个聊天对象
5.激活微信聊天窗口
6.将待发送的文本存进剪切板，ctrl+a全选搜索框内容，ctrl+v粘贴[待发送内容]
7.enter回车发送消息
