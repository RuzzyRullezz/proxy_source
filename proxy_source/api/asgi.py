import uvicorn

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8001
    uvicorn.run("proxy_source.api:app", host=host, port=port, reload=True)
