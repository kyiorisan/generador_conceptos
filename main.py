import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QLabel, QFileDialog, QLineEdit

import configurador
from generador_ss import generar_archivos_ss


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Inicializar Configuración
        if not Path('settings.ini').is_file():
            configurador.generate_config()

        config = configurador.read_config()

        # Cargar el archivo UI..
        uic.loadUi("main.ui", self)

        # Define nuestros widgets.
        self.button: QPushButton = self.findChild(QPushButton, "botonArchivo")
        self.boton_gener_archivos: QPushButton = self.findChild(QPushButton, "generarSS")
        self.label: QLabel = self.findChild(QLabel, "etiqueta")
        self.qna_proc_text: QLineEdit = self.findChild(QLineEdit, "qna_proc_edit")
        self.fname = ''
        self.button.clicked.connect(self.clicker)
        self.boton_gener_archivos.clicked.connect(self.clicker2)

        # Muestra la app.
        self.show()

    def clicker(self):
        self.fname = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "All Files(*);;Archivos Excel (*.xlsx)")

    def clicker2(self):
        try:
            generar_archivos_ss(int(self.qna_proc_text.text()), self.fname[0])
        except ValueError:
            print('seleccione el archivo primero')


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
