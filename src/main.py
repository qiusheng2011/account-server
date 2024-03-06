import uvicorn
from app import appserver

if __name__ == "__main__":
    config = appserver.extra.get("config", None)
    uvicorn.run(
        appserver,
        host=str(config.host),
        port=config.port,
        workers=config.workers
    )
