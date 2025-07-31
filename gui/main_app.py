import os
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from api.openai_api import get_player_info_from_image

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("선수 정보 추출기")
        self.setGeometry(100, 100, 500, 600)
        self.image_label = QLabel("유니폼 이미지를 불러오세요")
        self.image_label.setFixedSize(400, 400)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_button = QPushButton("유니폼 이미지 불러오기")
        self.load_button.clicked.connect(self.load_image)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.result_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_label.setPixmap(QPixmap(file_name))
            
            self.result_output.setPlainText("정보 추출 중입니다. 잠시만 기다려주세요...")
            player_info = get_player_info_from_image(file_name)
            
            if player_info:
                text = (
                    f"이름: {player_info['name']}\n"
                    f"팀: {player_info['team']}\n"
                    f"번호: {player_info['number']}\n\n"
                    f"DB에 저장되었습니다."
                )
            else:
                text = "선수 정보를 추출하지 못했습니다. 다시 시도해주세요."

            self.result_output.setPlainText(text)