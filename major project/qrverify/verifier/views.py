import os
import json
import numpy as np
import tensorflow as tf
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.urls import reverse

# Import blockchain helpers
from .blockchain import verify_product, register_product, generate_qr, abi, CONTRACT_ADDR


# ------------------- LOAD CNN MODEL (UPDATED) -------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "logo_counterfeit_cnn.h5")

cnn_model = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Counterfeit", "Genuine"]


# ------------------- LOGIN SYSTEM -------------------

def login_selection(request):
    """Main page with two options: Client or Manufacturer."""
    return render(request, 'verifier/login_selection.html')


def client_login(request):
    """Client logs in with just a name."""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            request.session['client_name'] = name
            return redirect('client_dashboard')
    return render(request, 'verifier/client_login.html')


def manufacturer_login(request):
    """Manufacturer logs in with name and password."""
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name == 'admin' and password == '12345':
            request.session['manufacturer_name'] = name
            return redirect('manufacturer_dashboard')
        else:
            return render(request, 'verifier/manufacturer_login.html', {'error': 'Invalid credentials'})
    return render(request, 'verifier/manufacturer_login.html')


def client_dashboard(request):
    """Dashboard for client."""
    name = request.session.get('client_name', 'Guest')
    return render(request, 'verifier/client_dashboard.html', {'name': name})


def manufacturer_dashboard(request):
    """Dashboard for manufacturer."""
    name = request.session.get('manufacturer_name', 'Manufacturer')
    return render(request, 'verifier/manufacturer_dashboard.html', {'name': name})


# ------------------- Dashboard -------------------

def dashboard(request):
    return render(request, 'verifier/dashboard.html')


# ------------------- Product Registration -------------------

def register_product_view(request):
    """
    Register product on blockchain.
    Handles both server-side registration fallback and MetaMask frontend registration.
    """
    message = ""
    qr_path = ""

    if request.method == "POST":
        product_id = request.POST.get("product_id", "").strip().upper()
        cid = request.POST.get("cid", "").strip()
        issuer = request.POST.get("issuer", "").strip()

        if product_id and cid and issuer:
            result = register_product(product_id, cid, issuer)
            if result["status"] == "success":
                qr_path = generate_qr(product_id)
                message = (
                    f"✅ Product registered successfully!<br>"
                    f"TxHash: {result['txHash']}<br>"
                    f"QR Generated: {qr_path}"
                )
            else:
                message = f"❌ Registration failed: {result['error']}"

    if request.session.get('manufacturer_name'):
        dashboard_url = reverse('manufacturer_dashboard')
    elif request.session.get('client_name'):
        dashboard_url = reverse('client_dashboard')
    else:
        dashboard_url = reverse('login_selection')

    return render(request, "verifier/register_product.html", {
        "message": message,
        "qr_path": qr_path,
        "contract_abi": json.dumps(abi),
        "contract_address": CONTRACT_ADDR,
        "dashboard_url": dashboard_url
    })


# ------------------- QR Verification -------------------

def qr_scan(request):
    if request.session.get('client_name'):
        dashboard_url = 'client_dashboard'
    elif request.session.get('manufacturer_name'):
        dashboard_url = 'manufacturer_dashboard'
    else:
        dashboard_url = 'login_selection'

    return render(request, 'verifier/qr_scan.html', {'dashboard_url': dashboard_url})


def verify_qr(request):
    """Reads uploaded QR image, extracts product_id, verifies on blockchain."""
    if request.method == 'POST':
        try:
            image_file = request.FILES['qr_image']
            image = Image.open(image_file)
            decoded_objs = decode(image)

            if not decoded_objs:
                return HttpResponse("⚠️ No QR code found in the image.")

            product_id = decoded_objs[0].data.decode('utf-8').strip().upper()
            product = verify_product(product_id)

            if product and product.get("exists"):
                return HttpResponse(
                    f"✅ Product Verified on Blockchain<br>"
                    f"Product ID: {product_id}<br>"
                    f"CID: {product['cid']}<br>"
                    f"Issuer: {product['issuer']}<br>"
                    f"Timestamp: {product['timestamp']}"
                )
            else:
                return HttpResponse(f"❌ Product ID '{product_id}' not found in Blockchain.")
        except Exception as e:
            return HttpResponse(f"⚠️ Error verifying QR: {str(e)}")


# ------------------- Image Verification -------------------

def image_scan(request):
    return render(request, 'verifier/image_scan.html')


def verify_image(request):
    """Verifies uploaded product image using CNN model."""
    if request.method == 'POST':
        try:
            image_file = request.FILES['product_image']
            img = Image.open(BytesIO(image_file.read())).convert('RGB')
            img = img.resize((128, 128))

            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = cnn_model.predict(img_array)[0][0]
            confidence = prediction

            if prediction >= 0.5:
                result = f"Genuine ({confidence*100:.2f}%)"
            else:
                result = f"Counterfeit ({(1-confidence)*100:.2f}%)"

            return HttpResponse(f"🧠 Image Verification Result: {result}")

        except Exception as e:
            return HttpResponse(f"⚠️ Error processing image: {str(e)}")

    return render(request, 'verifier/image_scan.html')


# ------------------- Combined QR + Image Verification -------------------

def verify_combined(request):
    """
    Verifies both QR and product image for maximum accuracy.
    """
    context = {}

    if request.method == "POST":
        qr_result, cnn_result, final_status, blockchain_status = None, None, None, None

        # --- QR Verification (Blockchain) ---
        try:
            qr_file = request.FILES.get("qr_image")
            if qr_file:
                qr_img = Image.open(qr_file)
                decoded_data = decode(qr_img)

                if decoded_data:
                    product_id = decoded_data[0].data.decode("utf-8").strip().upper()
                    qr_result = product_id
                    product = verify_product(product_id)

                    if product and product.get("exists"):
                        blockchain_status = (
                            f"✅ Verified | CID: {product['cid']} | Issuer: {product['issuer']}"
                        )
                    else:
                        blockchain_status = "❌ Not Found in Blockchain"

                else:
                    qr_result = "No QR code detected"
        except Exception as e:
            qr_result = f"Error: {str(e)}"

        # --- CNN Image Verification ---
        try:
            product_file = request.FILES.get("product_image")
            if product_file:
                img = Image.open(product_file).convert("RGB")
                img = img.resize((128, 128))

                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                prediction = cnn_model.predict(img_array)[0][0]
                confidence = prediction

                if prediction >= 0.5:
                    cnn_result = f"Genuine ({confidence*100:.2f}%)"
                else:
                    cnn_result = f"Counterfeit ({(1-confidence)*100:.2f}%)"

        except Exception as e:
            cnn_result = f"Error: {str(e)}"

        # --- Final Decision ---
        if qr_result and cnn_result:
            if blockchain_status and blockchain_status.startswith("✅") and "Genuine" in cnn_result:
                final_status = "✅ Product Verified (Blockchain + AI agree)"
            else:
                final_status = "⚠️ Suspicious Product (Mismatch or Missing Data)"
        else:
            final_status = "⚠️ Incomplete Verification"

        context = {
            "qr_result": qr_result,
            "blockchain_status": blockchain_status,
            "cnn_result": cnn_result,
            "final_status": final_status,
        }

    return render(request, "verifier/verify_product.html", context)
