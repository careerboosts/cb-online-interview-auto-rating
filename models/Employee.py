from typing import List, Optional
from datetime import datetime, time, timedelta,date
from fastapi import HTTPException

def ResponseModel_post(data, message):
    return {
        "data": [
            data
        ],
        "code": 201,
        "message": message,
    }

def ResponseModel_get(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
        raise HTTPException(detail={
        "detail": error,
        "code": code,
        "message": message
    },status_code=code)

