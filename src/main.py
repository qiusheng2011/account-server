"""程序入口文件

程序启动文件,任意位置使用即可启动

示例
`python3  */src/main.py`
"""

import os
import sys
import logging

import uvicorn
import pydantic_settings

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")

logger = logging.getLogger(__file__)

if __name__ == "__main__":
    import app
    config: pydantic_settings.BaseSettings = app.appserver.extra.get(
        "config", None)
    logger.info(f"config={config.model_dump_json()}")
    uvicorn.run(
        "app:appserver",
        host=str(config.host) or "localhost",
        port=config.port or 8000,
        workers=config.workers or 1
    )
