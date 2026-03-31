import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

# Import giao diện từ file RSAForm.py bạn vừa tạo
from RSAForm import Ui_MainWindow 

class RSAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Các biến để lưu trữ khóa RSA
        self.e = None
        self.d = None
        self.n = None

        # Gắn sự kiện click cho các nút bấm
        self.ui.btnGenerate.clicked.connect(self.generate_keys)
        self.ui.btnEncrypt.clicked.connect(self.encrypt_rsa)
        self.ui.btnDecrypt.clicked.connect(self.decrypt_rsa)

    # --- HÀM KIỂM TRA SỐ NGUYÊN TỐ ---
    def is_prime(self, num):
        if num < 2: return False
        for i in range(2, int(math.isqrt(num)) + 1):
            if num % i == 0: return False
        return True

    def get_random_prime(self, min_val=10, max_val=100):
        prime = random.randint(min_val, max_val)
        while not self.is_prime(prime):
            prime = random.randint(min_val, max_val)
        return prime

    # --- HÀM TẠO KHÓA ---
    def generate_keys(self):
        # 1. Chọn 2 số nguyên tố p, q khác nhau
        p = self.get_random_prime(10, 100)
        q = self.get_random_prime(10, 100)
        while p == q: 
            q = self.get_random_prime(10, 100)

        # 2. Tính n và phi(n)
        self.n = p * q
        phi = (p - 1) * (q - 1)

        # 3. Chọn e (Khóa công khai)
        self.e = random.randrange(2, phi)
        while math.gcd(self.e, phi) != 1:
            self.e = random.randrange(2, phi)

        # 4. Tính d (Khóa bí mật)
        self.d = pow(self.e, -1, phi)

        # Hiển thị lên giao diện
        self.ui.txtPublicKey.setText(f"e = {self.e}, n = {self.n}")
        self.ui.txtPrivateKey.setText(f"d = {self.d}, n = {self.n}")
        
        QMessageBox.information(self, "Thành công", "Đã tạo cặp khóa RSA ngẫu nhiên mới!")

    # --- HÀM MÃ HOÁ ---
    def encrypt_rsa(self):
        text = self.ui.txtInput.toPlainText()
        
        if not text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập văn bản cần mã hoá!")
            return
        if self.e is None or self.n is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng bấm 'Tạo khóa ngẫu nhiên' trước!")
            return

        # Quá trình mã hoá: C = M^e mod n
        cipher_blocks = []
        for char in text:
            m = ord(char) # Chuyển ký tự thành số ASCII
            c = pow(m, self.e, self.n)
            cipher_blocks.append(str(c))
        
        # Nối các số lại bằng khoảng trắng
        result = " ".join(cipher_blocks)
        self.ui.txtOutput.setPlainText(result)

    # --- HÀM GIẢI MÃ ---
    def decrypt_rsa(self):
        cipher_text = self.ui.txtInput.toPlainText().strip()
        
        if not cipher_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập bản mã cần giải!")
            return
        if self.d is None or self.n is None:
            QMessageBox.warning(self, "Cảnh báo", "Khóa bí mật chưa sẵn sàng!")
            return

        try:
            # Quá trình giải mã: M = C^d mod n
            plain_text = ""
            cipher_blocks = cipher_text.split(" ") 
            
            for block in cipher_blocks:
                if block: # Bỏ qua khoảng trắng thừa
                    c = int(block)
                    m = pow(c, self.d, self.n)
                    plain_text += chr(m) # Chuyển ngược từ ASCII sang ký tự
            
            self.ui.txtOutput.setPlainText(plain_text)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi giải mã", "Dữ liệu bản mã không hợp lệ! Hãy chắc chắn bạn nhập các số cách nhau bởi khoảng trắng.")

# --- KHỞI CHẠY APP ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())