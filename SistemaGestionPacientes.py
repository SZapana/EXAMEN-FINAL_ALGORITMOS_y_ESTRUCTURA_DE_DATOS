"""
SISTEMA DE GESTIÓN DE PACIENTES 
"""

import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QFileDialog,
    QMessageBox, QFrame, QScrollArea, QGridLayout, QSplitter  
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon


# === ESTRUCTURA: LISTA ENLAZADA ===
class Paciente:
    def __init__(self, nombre, edad, prioridad):
        self.nombre = nombre
        self.edad = edad
        self.prioridad = prioridad  # "urgente" o "normal"

    def __str__(self):
        return f"{self.nombre} ({self.edad} años) - {self.prioridad.upper()}"


class Nodo:
    def __init__(self, paciente):
        self.paciente = paciente
        self.siguiente = None


class ColaPacientes:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.total = 0

    def agregar(self, paciente):
        nuevo = Nodo(paciente)
        if paciente.prioridad == "urgente":
            if not self.cabeza:
                self.cabeza = self.cola = nuevo
            else:
                nuevo.siguiente = self.cabeza
                self.cabeza = nuevo
        else:
            if not self.cola:
                self.cabeza = self.cola = nuevo
            else:
                self.cola.siguiente = nuevo
                self.cola = nuevo
        self.total += 1

    def atender(self):
        if not self.cabeza:
            return None
        paciente = self.cabeza.paciente
        self.cabeza = self.cabeza.siguiente
        if not self.cabeza:
            self.cola = None
        self.total -= 1
        return paciente

    def mostrar_lista(self):
        if not self.cabeza:
            return ["(No hay pacientes esperando)"]
        lista = []
        actual = self.cabeza
        idx = 1
        while actual:
            lista.append(f"{idx}. {actual.paciente}")
            actual = actual.siguiente
            idx += 1
        return lista

    def esta_vacia(self):
        return self.cabeza is None

    def contar_por_prioridad(self):
        urgentes = normales = 0
        actual = self.cabeza
        while actual:
            if actual.paciente.prioridad == "urgente":
                urgentes += 1
            else:
                normales += 1
            actual = actual.siguiente
        return urgentes, normales


# === VENTANA PRINCIPAL – DISEÑO HOSPITALARIO ===
class VentanaPacientes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏥 Sistema Clínico - Sala de Emergencias")
        self.setGeometry(100, 100, 1200, 800)

        # Paleta de colores hospitalaria
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f8f9fa;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid #bdc3c7;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 8px;
                font-family: 'Courier New';
                color: #2c3e50;
            }
        """)

        # Layout principal
        layout_principal = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)

        # Cabecera del hospital
        cabecera = QFrame()
        cabecera.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
        """)
        cabecera_layout = QHBoxLayout(cabecera)

        logo = QLabel("🏥")
        logo.setFont(QFont("Arial", 40))
        cabecera_layout.addWidget(logo)

        titulo = QLabel("HOSPITAL UNIVERSITARIO\nSistema de Gestión de Pacientes")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: white; margin-left: 10px;")
        cabecera_layout.addWidget(titulo)
        cabecera_layout.addStretch()

        layout_principal.addWidget(cabecera)

        # Panel dividido
        splitter = QFrame()
        splitter.setFrameShape(QFrame.HLine)
        splitter.setStyleSheet("color: #bdc3c7;")
        layout_principal.addWidget(splitter)

        splitter_panel = QSplitter(Qt.Horizontal)
        layout_principal.addWidget(splitter_panel)

        # === PANEL IZQUIERDO: REGISTRO ===
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: #ffffff; border-radius: 10px; padding: 15px;")
        layout_izq = QVBoxLayout(panel_izq)

        # Título
        lbl_registro = QLabel("➕ Registrar Nuevo Paciente")
        lbl_registro.setFont(QFont("Arial", 14, QFont.Bold))
        lbl_registro.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout_izq.addWidget(lbl_registro)

        # Formulario
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Nombre:"), 0, 0)
        self.input_nombre = QLineEdit()
        form_layout.addWidget(self.input_nombre, 0, 1)

        form_layout.addWidget(QLabel("Edad:"), 1, 0)
        self.input_edad = QLineEdit()
        form_layout.addWidget(self.input_edad, 1, 1)

        form_layout.addWidget(QLabel("Prioridad:"), 2, 0)
        self.combo_prioridad = QComboBox()
        self.combo_prioridad.addItems(["normal", "urgente"])
        form_layout.addWidget(self.combo_prioridad, 2, 1)

        layout_izq.addLayout(form_layout)

        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("➕ Agregar Paciente")
        btn_agregar.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
        """)
        btn_agregar.clicked.connect(self.agregar_paciente)

        btn_atender = QPushButton("✅ Atender Siguiente")
        btn_atender.setStyleSheet("""
            background-color: #c0392b;
            color: white;
            border: none;
        """)
        btn_atender.clicked.connect(self.atender_paciente)

        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_atender)
        layout_izq.addLayout(btn_layout)

        # Información
        self.label_info = QLabel("📊 Pacientes en espera: 0 (Urgentes: 0)")
        self.label_info.setStyleSheet("color: #7f8c8d; font-weight: bold; font-size: 12px;")
        layout_izq.addWidget(self.label_info)

        # === PANEL DERECHO: LISTA Y ACCIONES ===
        panel_der = QWidget()
        panel_der.setStyleSheet("background: #ffffff; border-radius: 10px; padding: 15px;")
        layout_der = QVBoxLayout(panel_der)

        # Título
        lbl_lista = QLabel("📋 Lista de Pacientes en Espera")
        lbl_lista.setFont(QFont("Arial", 14, QFont.Bold))
        lbl_lista.setStyleSheet("color: #2c3e50;")
        layout_der.addWidget(lbl_lista)

        # Área de texto
        self.area_texto = QTextEdit()
        self.area_texto.setReadOnly(True)
        layout_der.addWidget(self.area_texto)

        # Botones de acción
        acciones_layout = QHBoxLayout()
        btn_lista = QPushButton("🔄 Actualizar")
        btn_lista.clicked.connect(self.mostrar_lista_actual)

        btn_historial = QPushButton("🗂️ Historial")
        btn_historial.clicked.connect(self.mostrar_historial)

        btn_exportar = QPushButton("📥 Exportar Lista")
        btn_exportar.clicked.connect(self.exportar_lista)

        acciones_layout.addWidget(btn_lista)
        acciones_layout.addWidget(btn_historial)
        acciones_layout.addWidget(btn_exportar)
        layout_der.addLayout(acciones_layout)

        # Añadir paneles
        splitter_panel.addWidget(panel_izq)
        splitter_panel.addWidget(panel_der)
        splitter_panel.setSizes([400, 800])
        splitter_panel.setStyleSheet("QSplitter::handle { background: #dfe4ea; }")

        # Variables
        self.cola = ColaPacientes()
        self.historial = []
        self.mostrar_lista_actual()

    def validar_datos(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingrese el nombre del paciente.")
            return None
        try:
            edad = int(self.input_edad.text().strip())
            if edad < 0 or edad > 120:
                raise ValueError
        except:
            QMessageBox.warning(self, "Edad inválida", "La edad debe ser un número entre 0 y 120.")
            return None
        prioridad = self.combo_prioridad.currentText()
        return Paciente(nombre, edad, prioridad)

    def agregar_paciente(self):
        paciente = self.validar_datos()
        if paciente:
            self.cola.agregar(paciente)
            self.actualizar_info()
            self.input_nombre.clear()
            self.input_edad.clear()
            QMessageBox.information(
                self, "Registrado",
                f"Paciente '{paciente.nombre}' registrado con prioridad '{paciente.prioridad}'."
            )
            self.mostrar_lista_actual()

    def atender_paciente(self):
        if self.cola.esta_vacia():
            QMessageBox.information(self, "Sin pacientes", "No hay pacientes para atender.")
            return
        paciente = self.cola.atender()
        self.historial.append(f"✅ {paciente} - Atendido a las {time.strftime('%H:%M')}")
        self.actualizar_info()
        # Animación suave
        self.area_texto.setStyleSheet("background-color: #fdedec; color: #c0392b;")
        self.area_texto.setText(f"🚨 ATENCIÓN: {paciente}\nHora: {time.strftime('%H:%M:%S')}")
        QTimer.singleShot(1500, self.restaurar_estilo)
        QTimer.singleShot(1800, self.mostrar_lista_actual)

    def restaurar_estilo(self):
        self.area_texto.setStyleSheet("""
            background-color: white;
            border: 1px solid #dfe4ea;
            border-radius: 8px;
            font-family: 'Courier New';
            color: #2c3e50;
        """)

    def actualizar_info(self):
        urgentes, normales = self.cola.contar_por_prioridad()
        total = self.cola.total
        self.label_info.setText(f"📊 Pacientes en espera: {total} (🔴 Urgentes: {urgentes})")

    def mostrar_lista_actual(self):
        self.area_texto.clear()
        self.area_texto.append("<h3>📋 LISTA DE ESPERA - SALA DE EMERGENCIAS</h3>")
        self.area_texto.append(f"<b>Fecha:</b> {time.strftime('%d/%m/%Y')} | <b>Hora:</b> {time.strftime('%H:%M:%S')}")
        self.area_texto.append("<hr>")
        lista = self.cola.mostrar_lista()
        for item in lista:
            if "URGENTE" in item:
                self.area_texto.append(f'<font color="#c0392b"><b>🚨 {item}</b></font>')
            else:
                self.area_texto.append(f'🔵 {item}')
        self.actualizar_info()

    def mostrar_historial(self):
        self.area_texto.clear()
        self.area_texto.append("<h3>🗂️ HISTORIAL DE ATENCIONES</h3><hr>")
        if not self.historial:
            self.area_texto.append("<i>Ningún paciente ha sido atendido aún.</i>")
        else:
            for registro in self.historial:
                self.area_texto.append(registro)

    def exportar_lista(self):
        nombre_archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Lista de Pacientes", "lista_pacientes.txt",
            "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        if nombre_archivo:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("========================================\n")
                f.write("      LISTA DE PACIENTES - HOSPITAL\n")
                f.write("========================================\n")
                f.write(f"Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Pacientes en espera: {self.cola.total}\n")
                f.write("Prioridades: Urgentes (🔴), Normales (🔵)\n")
                f.write("Lista:\n")
                actual = self.cola.cabeza
                idx = 1
                while actual:
                    f.write(f"{idx}. {actual.paciente}\n")
                    actual = actual.siguiente
                    idx += 1
            QMessageBox.information(self, "Exportado", f"Lista guardada en:\n{nombre_archivo}")


# === EJECUCIÓN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPacientes()
    ventana.show()
    sys.exit(app.exec_())