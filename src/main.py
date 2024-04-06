"""程序入口文件

程序启动文件,任意位置使用即可启动

示例
`python3  */src/main.py`
"""

import os
import sys

import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")


if __name__ == "__main__":
    import app
    config = app.appserver.extra.get("config", None)
    uvicorn.run(
        "app:appserver",
        host=str(config.host),
        port=config.port,
        workers=config.workers
    )
