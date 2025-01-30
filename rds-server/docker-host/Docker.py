# SystemInfo.py
import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
import docker
import os
router = APIRouter()