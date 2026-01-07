# Detection of Counterfeit Products Using Blockchain and CNN

## 📌 Project Overview
Counterfeit products cause major financial loss and pose serious risks to consumers.
This project proposes a secure and intelligent system to **detect counterfeit products**
using **Blockchain technology**, **QR code verification**, and **Convolutional Neural Networks (CNN)**.

The system ensures product authenticity by combining immutable blockchain records
with AI-based image/logo verification.

---

## 🎯 Objectives
- Prevent counterfeit products in the supply chain
- Provide tamper-proof product verification using blockchain
- Enable QR-code based product authentication
- Detect counterfeit products using CNN-based image classification

---

## 🧠 System Modules
1. **Product Registration**
   - Manufacturer registers product details
   - Unique QR code is generated for each product

2. **Blockchain-Based Verification**
   - Product details stored securely using blockchain hashing
   - Ensures immutability and transparency

3. **QR Code Authentication**
   - Users scan/upload QR codes
   - System verifies authenticity from blockchain records

4. **CNN-Based Image Detection**
   - Logo/image-based classification
   - Detects genuine vs counterfeit products

5. **User Interface**
   - Django-based web dashboard
   - Separate manufacturer and client views

---

## ⚙️ Technologies Used
- **Backend:** Python, Django
- **Blockchain:** Solidity, Truffle, Web3
- **AI/ML:** CNN (TensorFlow / Keras)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Tools:** Git, GitHub

---

## 📁 Project Structure
counterfeit-product-detection/
│
├── Logo_CNN_Training/
│ ├── train_cnn.py
│ ├── accuracy_graph.png
│ └── loss_graph.png
│
├── major project/
│ └── qrverify/
│ ├── manage.py
│ ├── verifier/
│ └── templates/
│
├── .gitignore
└── README.md

---

## 📊 Dataset Information
Due to GitHub size limitations, image datasets are **not included** in this repository.

To run CNN training:
Logo_CNN_Training/dataset/


Place genuine and counterfeit images inside the dataset folder.

---

## ▶️ How to Run the Project
1. Clone the repository
```bash
git clone https://github.com/Soujanya315/counterfeit-product-detection.git
Navigate to project directory

cd counterfeit-product-detection


Create virtual environment and install dependencies

pip install -r requirements.txt


Run Django server

python manage.py runserver
🔐 Security Features

Blockchain-based immutability

QR-code validation

AI-powered counterfeit detection

🎓 Academic Details

Project Type: Final Year Engineering Major Project

Domain: Blockchain, Artificial Intelligence, Cyber Security

Use Case: Anti-counterfeit product verification system

📌 Future Enhancements

OTP-based verification

Mobile application support

Real-time blockchain network deployment

Advanced CNN model optimization

👩‍💻 Author

Soujanya HS
Final Year Engineering Student


---

## ✅ STEP 3: Add README to Git & Push
Run these commands in terminal:

```powershell
git add README.md
git commit -m "Add detailed project README"
git push