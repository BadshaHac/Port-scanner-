import sys
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout

class PortScanner(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Port Scanner")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Target IP Address:")
        layout.addWidget(self.label)

        self.ip_input = QLineEdit(self)
        layout.addWidget(self.ip_input)

        self.scan_button = QPushButton("Scan Ports", self)
        self.scan_button.clicked.connect(self.scan_ports)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    # 🔹 Replace the old scan_ports function with this improved one
    def scan_ports(self):
        target = self.ip_input.text().strip()  # Remove spaces
        self.result_area.clear()
        
        if not target:
            self.result_area.setText("Please enter a valid IP address.")
            return
        
        try:
            # Validate IP or hostname
            socket.gethostbyname(target)
        except socket.gaierror:
            self.result_area.setText("Invalid IP Address or Hostname.")
            return
        
        self.result_area.append(f"Scanning {target}...\n")

        for port in range(20, 1025):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                result = s.connect_ex((target, port))
                if result == 0:
                    self.result_area.append(f"Port {port} is OPEN")
                s.close()
            except Exception as e:
                self.result_area.append(f"Error scanning port {port}: {e}")

        self.result_area.append("\nScan Complete!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = PortScanner()
    scanner.show()
    sys.exit(app.exec())
