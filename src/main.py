import uvicorn
from app import appserver

if __name__ == "__main__":
    uvicorn.run(appserver, port=8700)