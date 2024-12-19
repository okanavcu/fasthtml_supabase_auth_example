from fasthtml import common as fh
from dotenv import load_dotenv
import os

load_dotenv()


from components import auth

hdrs = [
    fh.Html({"data-theme":"cupcake"}, lang='en'),
    fh.Link(href='https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css', rel='stylesheet'),
    fh.Script(src='https://cdn.tailwindcss.com')
]

app, rt = fh.fast_app(before=auth.bware,pico=False,hdrs=hdrs)

async def info(req):
    return await auth.users_info(req=req)



@rt("/login")
async def get():
    return await auth.login_get()


@rt("/login")
async def post(login: auth.Login, sess, req):
    return await auth.login_post(login, sess, req)


@rt("/logout")
async def logout(sess,req):
    return await auth.logout(sess,req=req)


@rt("/protected")
async def protected(req):
    return fh.Titled(
        "Protected Page",
        fh.A("Back", href="/"),
        fh.P(),
        fh.A("Logout", href="/logout"),
        fh.Div(await info(req=req)),
    )


@rt("/")
async def home(sess, req):
    if await auth.is_authenticated(sess):
        return fh.Titled(
            "Dashboard",
            fh.P("You are logged in. View a protected page below."),
            fh.A("Protected Page", href="/protected"),
            fh.P(),
            fh.P("Logout here:"),
            fh.A("Logout", href="/logout"),
            fh.Div(await auth.veri(sess,req))
        )   

    else:
        return fh.Titled(
            "Home", fh.H1("Welcome to the App"), fh.A("Login", href="/login")
        )


if __name__ == "__main__":
    print("Starting server")
    fh.serve(port=8080)
