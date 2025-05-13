from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/webhook")
async def webhook_listener(request: Request):
    """
    Webhook 事件监听入口，支持 GitHub/GitLab PR/MR 相关事件。
    :param request: FastAPI Request 对象
    :return: JSONResponse
    """
    event_body = await request.json()
    # 打印收到的事件内容，后续可扩展为事件分发
    print("[Webhook] 收到事件:", event_body)
    return JSONResponse(content={"msg": "事件已接收"}, status_code=200) 