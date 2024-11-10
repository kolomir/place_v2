from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys


class ImageViewer(QWidget):
    def __init__(self, image_paths):
        super().__init__()

        # Lista ścieżek do obrazów
        self.image_paths = image_paths
        self.current_image_index = 0  # indeks aktualnego obrazu

        # Ustawienia okna
        self.setWindowTitle("Przeglądarka obrazów")
        self.setGeometry(100, 100, 800, 600)

        # Inicjalizacja QLabel do wyświetlania obrazu
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.update_image()

        # Przyciski do przewijania obrazów
        self.prev_button = QPushButton("<", self)
        self.prev_button.clicked.connect(self.show_previous_image)

        self.next_button = QPushButton(">", self)
        self.next_button.clicked.connect(self.show_next_image)

        # Układ poziomy z przyciskami po bokach QLabel
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.prev_button)
        h_layout.addWidget(self.image_label)
        h_layout.addWidget(self.next_button)

        # Układ główny widgetu
        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)

    def update_image(self):
        # Wczytuje obraz do QLabel na podstawie aktualnego indeksu
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def show_next_image(self):
        # Przechodzi do następnego obrazu
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.update_image()

    def show_previous_image(self):
        # Przechodzi do poprzedniego obrazu
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.update_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_paths = ["obraz1.jpg", "obraz2.jpg", "obraz3.jpg"]  # Lista ścieżek do obrazów
    viewer = ImageViewer(image_paths)
    viewer.show()
    sys.exit(app.exec_())