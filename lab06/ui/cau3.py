import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Import class Ui_MainWindow từ file RailFenceForm.py của bạn
from RailFenceForm import Ui_MainWindow 

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối nút bấm với các hàm xử lý bên dưới
        self.ui.btnEncrypt.clicked.connect(self.encrypt_rail_fence)
        self.ui.btnDecrypt.clicked.connect(self.decrypt_rail_fence)

    # --- HÀM MÃ HOÁ ---
    def encrypt_rail_fence(self):
        text = self.ui.txtInput.toPlainText()
        key = self.ui.spinKey.value()
        
        if not text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản!")
            return

        # Thuật toán Rail Fence Mã hoá
        rails = [''] * key
        row = 0
        step = 1

        for char in text:
            rails[row] += char
            if row == 0:
                step = 1
            elif row == key - 1:
                step = -1
            row += step

        result = ''.join(rails)
        
        # Hiển thị kết quả ra màn hình
        self.ui.txtOutput.setPlainText(result)

    # --- HÀM GIẢI MÃ ---
    def decrypt_rail_fence(self):
        cipher = self.ui.txtInput.toPlainText()
        key = self.ui.spinKey.value()
        
        if not cipher:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản!")
            return

        # Thuật toán Rail Fence Giải mã
        rail_matrix = [['\n' for i in range(len(cipher))] for j in range(key)]
        
        # Đánh dấu các vị trí
        row, step = 0, 1
        for i in range(len(cipher)):
            rail_matrix[row][i] = '*'
            if row == 0:
                step = 1
            elif row == key - 1:
                step = -1
            row += step
            
        # Điền ciphertext
        index = 0
        for i in range(key):
            for j in range(len(cipher)):
                if rail_matrix[i][j] == '*' and index < len(cipher):
                    rail_matrix[i][j] = cipher[index]
                    index += 1
                    
        # Đọc theo zigzag
        result = []
        row, step = 0, 1
        for i in range(len(cipher)):
            result.append(rail_matrix[row][i])
            if row == 0:
                step = 1
            elif row == key - 1:
                step = -1
            row += step
            
        # Hiển thị kết quả ra màn hình
        self.ui.txtOutput.setPlainText("".join(result))

# --- ĐOẠN CODE ĐỂ CHẠY CHƯƠNG TRÌNH ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())