#!/usr/local/bin/python3
# coding: utf-8

import os, httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# URLs where your Flask services are running
RDBES_API_URL = os.getenv('RDBES_API_URL')
CHANNEL_API_URL = os.getenv('CHANNEL_API_URL')
TAXON_API_URL = os.getenv('TAXON_API_URL')
GEAR_API_URL = os.getenv('GEAR_API_URL')
VESSEL_API_URL = os.getenv('VESSEL_API_URL')
AGF_API_URL = os.getenv('AGF_API_URL')
ADB_API_URL = os.getenv('ADB_API_URL')

app = FastAPI(title="Rdbes API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

timeout = httpx.Timeout(
    connect=10.0,   # connect timeout
    read=120.0,     # how long to wait for response data
    write=10.0,     # sending data timeout
    pool=120.0      # total connection pool timeout
)

@app.get("/")
def root():
    return {"message": "API Gateway is running"}

# -------- Acoustic service endpoints --------
@app.api_route("/rdbes/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_acoustic(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{RDBES_API_URL}/{path}"
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()

# -------- Channel service endpoints --------
@app.api_route("/channel/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_channel(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{CHANNEL_API_URL}/{path}"
        print(url)
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()

@app.api_route("/taxon/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_taxon(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{TAXON_API_URL}/{path}"
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()

@app.api_route("/gear/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_gear(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{GEAR_API_URL}/{path}"
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()

@app.api_route("/vessel/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_vessel(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{VESSEL_API_URL}/{path}"
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()

@app.api_route("/agf/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_agf(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{AGF_API_URL}/{path}"
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()

@app.api_route("/adb/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_adb(path: str, request: Request):
    print(path)
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{ADB_API_URL}/{path}"
        method = request.method
        data = await request.body()
        headers = dict(request.headers)
        params = dict(request.query_params)  # <-- forward query parameters
        r = await client.request(method, url, params=params, content=data, headers=headers)
        return r.json()
