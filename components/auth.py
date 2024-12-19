from datetime import datetime
import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from fasthtml import common as fh
from starlette.responses import RedirectResponse
from supabase import AsyncClientOptions
from supabase._async.client import AsyncClient as Client, create_client
import json

@dataclass
class Login:
    email: str
    password: str

async def create_supabase(req) -> Client:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    # Çerezlerden kullanıcı bilgilerini al
    user_token = req.cookies.get("user_token")
    
    if user_token:
        options = AsyncClientOptions(
            headers={"Authorization": f"Bearer {user_token}"}
        )
    else:
        options = None
    
    return await create_client(
        supabase_url,
        supabase_key,
        options=options
    )

def before(req, sess):
    # JSON stringini Python sözlüğüne dönüştür
    session_data = json.loads(req.cookies["session_"])
    auth = req.scope["auth"] = session_data["user"]["email"]
    if not auth:
        return RedirectResponse("/login", status_code=303)
bware = fh.Beforeware(
    before, skip=[r"/favicon\\.ico", r"/static/.*", r".*\\.css", "/login", "/"]
)

async def login_get():
    print("Rendering login page")
    frm = fh.Form(
        fh.Input(type="email", name="email", placeholder="Email"),
        fh.Input(type="password", name="password", placeholder="Password"),
        fh.Button("Log in", type="submit"),
        action="/login",
        method="post",
    )
    return fh.Titled("Login", frm)

async def login_post(login: Login, sess, req):
    try:
        # create_client artık await edilmez
        supabase = await create_supabase(req=req)
        
        # Auth işlemi
        response = await supabase.auth.sign_in_with_password(
            {"email": login.email, "password": login.password}
        )
        data = response.model_dump_json()
        return RedirectResponse(
            "/",
            status_code=303,
            headers={
                'Set-Cookie': f"session_={data};",
            }
            )
    except Exception as e:
        print(f"Login failed with error: {str(e)}")
        return fh.Titled("Login Failed", fh.P(str(e)))

async def logout(sess, req):
    print(f"Logging out. Session before clear: {sess}")
    supabase = await create_supabase(req)
    await supabase.auth.sign_out()
    sess.clear()
    return RedirectResponse("/login", status_code=303)

async def users_info(req):
    supabase = await create_supabase(req)
    response = await supabase.auth.get_user()
    return response

async def set_user_session(sess, user_email):
    sess["user"] = user_email

async def clear_session(sess):
    sess.clear()

async def is_authenticated(sess):
    return "user" in sess

async def veri(req):
    supabase = await create_supabase(req)
    response = await supabase.table("deneme").select("*").execute()
    return response
