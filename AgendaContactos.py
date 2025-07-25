"""
AGENDA DE CONTACTOS - HASHING CON CHAINING + INTERFAZ PYQT5
Autor: [Tu Nombre]
Docente: Mg. Aldo Hernán Zanabria Gálvez
Curso: Estructuras de Datos y Algoritmos

Funcionalidad:
- Diccionario con hashing y chaining
- Interfaz profesional con PyQt5
- Agregar, buscar, eliminar, mostrar estado del hash
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QFrame, QScrollArea,
    QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QPainter


# === ESTRUCTURA HASH CON CHAINING ===
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # Chaining con listas

    def _hash(self, key):
        """Función hash simple: suma de valores ASCII módulo tamaño"""
        return sum(ord(char) for char in key) % self.size

    def insert(self, nombre, telefono):
        index = self._hash(nombre)
        bucket = self.table[index]
        for i, (n, t) in enumerate(bucket):
            if n == nombre:
                bucket[i] = (nombre, telefono)  # Actualizar
                return "actualizado"
        bucket.append((nombre, telefono))
        return "agregado"

    def search(self, nombre):
        index = self._hash(nombre)
        bucket = self.table[index]
        for n, t in bucket:
            if n == nombre:
                return t
        return None

    def delete(self, nombre):
        index = self._hash(nombre)
        bucket = self.table[index]
        for i, (n, t) in enumerate(bucket):
            if n == nombre:
                del bucket[i]
                return True
        return False

    def get_state(self):
        """Devuelve una representación del estado del hash table"""
        state = []
        for i, bucket in enumerate(self.table):
            if bucket:
                entries = " → ".join(f"{n}({t})" for n, t in bucket)
                state.append(f"Bucket {i}: [{entries}]")
            else:
                state.append(f"Bucket {i}: [vacío]")
        return state

    def get_all_contacts(self):
        """Devuelve todos los contactos como lista"""
        contacts = []
        for bucket in self.table:
            contacts.extend(bucket)
        return contacts


# === FONDO SUAVE CON DEGRADADO ===
class FondoSuave(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QBrush(QColor(240, 248, 255), Qt.SolidPattern)  # Azul cielo claro
        painter.fillRect(event.rect(), gradient)


# === VENTANA PRINCIPAL ===
class VentanaAgenda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📱 Agenda de Contactos - Hashing con Chaining")
        self.setGeometry(100, 100, 1000, 700)
        self.setFixedSize(1000, 700)

        # Fondo
        self.fondo = FondoSuave()
        self.setCentralWidget(self.fondo)

        # Layout principal
        layout_principal = QVBoxLayout(self.fondo)

        # Título
        titulo = QLabel("AGENDA DE CONTACTOS")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color: #2c3e50;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            color: white;
            border-radius: 15px;
            margin-bottom: 10px;
        """)
        layout_principal.addWidget(titulo)

        # Descripción
        desc = QLabel("Sistema de hashing con chaining para gestión de contactos.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout_principal.addWidget(desc)

        # Panel dividido
        splitter = QFrame()
        splitter.setFrameShape(QFrame.HLine)
        splitter.setStyleSheet("color: #bdc3c7;")
        layout_principal.addWidget(splitter)

        splitter_panel = QFrame()
        splitter_layout = QHBoxLayout(splitter_panel)
        layout_principal.addWidget(splitter_panel)

        # === PANEL IZQUIERDO: CONTROLES ===
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")
        layout_izq = QVBoxLayout(panel_izq)

        # Título
        lbl_form = QLabel("➕ Gestión de Contactos")
        lbl_form.setFont(QFont("Arial", 14, QFont.Bold))
        lbl_form.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout_izq.addWidget(lbl_form)

        # Formulario
        form_layout = QVBoxLayout()

        # Nombre
        form_layout.addWidget(QLabel("Nombre:"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Juan Pérez")
        form_layout.addWidget(self.input_nombre)

        # Teléfono
        form_layout.addWidget(QLabel("Teléfono:"))
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Ej: 987654321")
        form_layout.addWidget(self.input_telefono)

        layout_izq.addLayout(form_layout)

        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("➕ Agregar")
        btn_agregar.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_agregar.clicked.connect(self.agregar_contacto)

        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_buscar.clicked.connect(self.buscar_contacto)

        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_eliminar.clicked.connect(self.eliminar_contacto)

        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_buscar)
        btn_layout.addWidget(btn_eliminar)
        layout_izq.addLayout(btn_layout)

        # Información
        self.label_info = QLabel("Contactos: 0")
        self.label_info.setStyleSheet("color: #7f8c8d; font-weight: bold; margin-top: 10px;")
        layout_izq.addWidget(self.label_info)

        # === PANEL DERECHO: LISTA Y HASH ===
        panel_der = QWidget()
        panel_der.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")
        layout_der = QVBoxLayout(panel_der)

        # Pestañas
        tabs_layout = QHBoxLayout()
        btn_contactos = QPushButton("📋 Contactos")
        btn_contactos.setStyleSheet("background: #1e3a8a; color: white; padding: 8px;")
        btn_contactos.clicked.connect(self.mostrar_contactos)

        btn_hash = QPushButton("🔧 Estado del Hash")
        btn_hash.setStyleSheet("background: #7c3aed; color: white; padding: 8px;")
        btn_hash.clicked.connect(self.mostrar_hash)

        tabs_layout.addWidget(btn_contactos)
        tabs_layout.addWidget(btn_hash)
        layout_der.addLayout(tabs_layout)

        # Área de texto
        self.area_texto = QTextEdit()
        self.area_texto.setReadOnly(True)
        self.area_texto.setStyleSheet("""
            background: #f8f9fa;
            border: 1px solid #dfe4ea;
            border-radius: 8px;
            font-family: 'Courier New';
            color: #2c3e50;
            padding: 10px;
        """)
        layout_der.addWidget(self.area_texto)

        # Añadir paneles
        splitter_layout.addWidget(panel_izq)
        splitter_layout.addWidget(panel_der)
        splitter_layout.setStretch(0, 1)
        splitter_layout.setStretch(1, 2)

        # Inicializar hash table
        self.hash_table = HashTable(size=10)
        self.mostrar_contactos()

    def validar_datos(self):
        nombre = self.input_nombre.text().strip()
        telefono = self.input_telefono.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío.")
            return None, None
        if not telefono.isdigit() or len(telefono) < 6:
            QMessageBox.warning(self, "Error", "El teléfono debe tener al menos 6 dígitos.")
            return None, None
        return nombre, telefono

    def agregar_contacto(self):
        nombre, telefono = self.validar_datos()
        if nombre and telefono:
            resultado = self.hash_table.insert(nombre, telefono)
            accion = "actualizado" if resultado == "actualizado" else "agregado"
            QMessageBox.information(self, "Éxito", f"Contacto {accion} correctamente.")
            self.input_nombre.clear()
            self.input_telefono.clear()
            self.mostrar_contactos()

    def buscar_contacto(self):
        nombre, _ = self.validar_datos()
        if nombre:
            telefono = self.hash_table.search(nombre)
            if telefono:
                QMessageBox.information(self, "Encontrado", f"{nombre}: {telefono}")
                self.input_telefono.setText(telefono)
            else:
                QMessageBox.information(self, "No encontrado", f"El contacto '{nombre}' no existe.")
            self.mostrar_contactos()

    def eliminar_contacto(self):
        nombre, _ = self.validar_datos()
        if nombre:
            if self.hash_table.delete(nombre):
                QMessageBox.information(self, "Eliminado", f"Contacto '{nombre}' eliminado.")
            else:
                QMessageBox.information(self, "No encontrado", f"El contacto '{nombre}' no existe.")
            self.input_nombre.clear()
            self.input_telefono.clear()
            self.mostrar_contactos()

    def mostrar_contactos(self):
        self.area_texto.clear()
        self.area_texto.append("<h3>📋 LISTA DE CONTACTOS</h3><hr>")
        contacts = self.hash_table.get_all_contacts()
        if not contacts:
            self.area_texto.append("<i>No hay contactos registrados.</i>")
        else:
            for nombre, telefono in contacts:
                self.area_texto.append(f"📞 <b>{nombre}</b>: {telefono}")
        self.actualizar_info()

    def mostrar_hash(self):
        self.area_texto.clear()
        self.area_texto.append("<h3>🔧 ESTADO DEL HASH TABLE</h3><hr>")
        state = self.hash_table.get_state()
        for line in state:
            if "vacío" in line:
                self.area_texto.append(f'<font color="#95a5a6">{line}</font>')
            else:
                self.area_texto.append(f'<font color="#2c3e50"><b>{line}</b></font>')
        self.actualizar_info()

    def actualizar_info(self):
        contacts = self.hash_table.get_all_contacts()
        self.label_info.setText(f"Contactos: {len(contacts)}")


# === EJECUCIÓN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaAgenda()
    ventana.show()
    sys.exit(app.exec_())