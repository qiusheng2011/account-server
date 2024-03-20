"""
程序入口文件
"""
import os
import sys

import uvicorn
import app

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    config = app.appserver.extra.get("config", None)
    uvicorn.run(
        "app:appserver",
        host=str(config.host),
        port=config.port,
        workers=config.workers
    )
