from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(code: int, msg: str = "success", data=None):
    content = {"code": code, "msg": msg, "data": data}
    return JSONResponse(content=jsonable_encoder(content))
