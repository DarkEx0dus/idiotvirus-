#!/usr/bin/env python3

import os
import subprocess
from flask import Flask, render_template_string, render_template
import qrcode
import base64
from io import BytesIO

def check_install(command, install_command):
    result = subprocess.run(f"which {command}", shell=True, stdout=subprocess.PIPE)
    if result.stdout.decode().strip() == "":
        print(f"[+] Installing {command}...")
        os.system(install_command)
    else:
        print(f"[✓] {command} already installed.")

def install_dependencies():
    os.system("pkg update -y")
    check_install("figlet", "pkg install figlet -y")
    check_install("ruby", "pkg install ruby -y")
    check_install("lolcat", "gem install lolcat")

def banner():
    os.system("clear")
    os.system("figlet IDIOT VIRUS | lolcat")
    print(r"""
╔══════════════════════════╗
║  CREATED BY: Dark Ex0dus ║
╚══════════════════════════╝
""")

app = Flask(__name__)

PUBLIC_URL = "https://suggestions-playstation-contracts-fence.trycloudflare.com"
QR_TARGET = f"{PUBLIC_URL}/dashboard"

@app.route("/")
def qr_page():
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(QR_TARGET)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scan QR</title>
        <style>
            body {{
                background: #111;
                color: white;
                text-align: center;
                font-family: Arial;
                padding-top: 50px;
            }}
            img {{
                width: 300px;
                height: 300px;
                background: white;
                padding: 15px;
                border-radius: 15px;
            }}
        </style>
    </head>
    <body>
        <h2>Scan This QR Code</h2>
        <img src="data:image/png;base64,{qr_base64}">
        <p>{QR_TARGET}</p>
    </body>
    </html>
    """)

@app.route("/dashboard")
def dashboard():
    return render_template("vbs.html")

def main():
    install_dependencies()
    banner()
    print("[+] Starting QR Flask App...")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
