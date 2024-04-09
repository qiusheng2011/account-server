"""send_mail_worker程序入口文件

程序启动文件,任意位置使用即可启动

示例
`python3  */src/main_sewmain.py`
"""

import os
import sys
import asyncio


sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")

if __name__ == "__main__":
    from src.workers import send_email_worker
    asyncio.run(main=send_email_worker.main())
