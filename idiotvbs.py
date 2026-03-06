from flask import Flask, render_template_string, render_template
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

# 🔥 PALITAN MO ITO NG CURRENT CLOUDFARE LINK MO
PUBLIC_URL = "https://suggestions-playstation-contracts-fence.trycloudflare.com"

# QR should point to /dashboard
QR_TARGET = f"{PUBLIC_URL}/dashboard"


# 🔹 QR PAGE (Homepage)
@app.route("/")
def qr_page():

    # Generate clean QR
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


# 🔹 Dashboard Route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)