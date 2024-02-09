import typing
import fastapi
import orjson
import uvicorn
import jwt
import json
import base64
from fastapi import FastAPI, Request
from config import settings
from routes.online_interview_rating import router as OnlineInterviewRatingRouter

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse


class ORJSONResponse(fastapi.responses.JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(default_response_class=ORJSONResponse)
"""
@app.middleware("http")
async def requestHeaderHandler(request: Request, call_next):

    headers = request.headers

    if "user_data" not in headers.keys():
        if "authorization" in headers.keys():
            authorization_token = headers["authorization"]
            access_token = authorization_token
            if authorization_token.startswith("Bearer"):
                access_token = authorization_token.split(" ")[1]
            try:
                decoded_token = jwt.decode(access_token, algorithms=["RS256"], options={"verify_signature": False})
                user_data = decoded_token
                json_str = json.dumps(user_data)
                base64_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
                if user_data:
                    request.headers.__dict__["_list"].append(
                        (
                            "user_data".encode(),
                            str(base64_data).encode(),
                        )
                    )
            except jwt.InvalidTokenError:
                return JSONResponse({"error": "Invalid access token"}, status_code=401)
        else:
            return JSONResponse({"error": "Token is missing"}, status_code=401)
                
    
    return await call_next(request)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
@app.get("/", tags=["Root"])
async def read_root(request: Request):
    return {"message": "Welcome to this fantastic app.", "headers": request.headers}


app.include_router(
    OnlineInterviewRatingRouter,
    tags=["OnlineInterviewRating"],
    prefix="/online-interview-rating",
)
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
         host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
    

@app.get("/healthz")
def health():
    return {"status": "healthy"}

