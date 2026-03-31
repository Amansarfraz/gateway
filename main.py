from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from routes import router  # your routes file


app = FastAPI()

# 🔥 Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# 🔥 Middleware
app.add_middleware(SlowAPIMiddleware)

# 🔥 Rate Limit Exception Handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests"}
    )

# 🔥 Home Route (FIXED)
@app.get("/")
@limiter.limit("5/minute")
def home(request: Request):   # ✅ IMPORTANT FIX
    return {"msg": "API Gateway Running 🚀"}

# 🔥 Include Routes
app.include_router(router)
from fastapi import FastAPI
from routes import auth_routes, student_routes, admin_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(admin_routes.router)