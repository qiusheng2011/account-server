import uvicorn
from app import appserver

if __name__ == "__main__":
    uvicorn.run(appserver, port=8700, workers=1,limit_concurrency=1)