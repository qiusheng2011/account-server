import uvicorn
from app import appserver


if __name__ == "__main__":
    uvicorn.run(appserver,host=str(appserver.config.host), port=appserver.config.port, workers=appserver.config.workers)
