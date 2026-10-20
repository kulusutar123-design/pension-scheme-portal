from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Pension Scheme Portal</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                h1 { color: #2E86C1; }
            </style>
        </head>
        <body>
            <h1>Social Security Pension Portal</h1>
            <p>Gariba o asahaya mananka sahayata pain.</p>
            <p>Registration Form khub shighra asuchi...</p>
        </body>
    </html>
    """
