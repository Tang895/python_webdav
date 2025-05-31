from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
from cheroot.wsgi import Server
import os
movies_path = os.path.join(os.path.expanduser("~"), "movies", "影片")
# 配置 WebDAV 服务
config = {
    "host": "0.0.0.0",                # 监听的地址
    "port": 8080,                      # 监听的端口
    "provider_mapping": {"/": FilesystemProvider(movies_path)},  # 文件存储路径
    "simple_dc": {                     # 简单的用户名和密码认证
        "user_mapping": {
            "*": {"admin": {"password": "tang"}},  # 用户名: admin, 密码: admin
        },
    },
    "verbose": 1,                      # 日志详细级别
    "http_authenticator": {
        "accept_basic": True,          # 允许 HTTP 基本认证
        "accept_digest": False,        # 不允许摘要认证
        "default_to_digest": False,
    },
    # "enable_loggers": ["wsgidav"],     # 启用日志
}

# 创建 WebDAV 应用程序
app = WsgiDAVApp(config)

if __name__ == "__main__":
    # 使用 cheroot.wsgi.Server 启动服务
    server = Server((config["host"], config["port"]), app)
    try:
        print(f"Starting WebDAV server at http://{config['host']}:{config['port']}")
        server.start()
    except KeyboardInterrupt:
        print("Stopping WebDAV server.")
        server.stop()
