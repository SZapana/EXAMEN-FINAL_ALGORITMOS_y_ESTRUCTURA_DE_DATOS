"""
SISTEMA DE PRIORIDADES CON HEAP - INTERFAZ PROFESIONAL

Funcionalidad:
- Gestión de tareas con prioridad (1-10)
- Heap para extracción de máxima prioridad
- Interfaz gráfica moderna con PyQt5
"""

import sys
import heapq
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem, QSpinBox, QFrame, QScrollArea, QMessageBox,
    QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QPainter


# === FONDO SUAVE CON DEGRADADO ===
class FondoSuave(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QBrush(QColor(248, 249, 250), Qt.SolidPattern)
        painter.fillRect(event.rect(), gradient)


# === CLASE PRINCIPAL: SISTEMA DE PRIORIDADES ===
class SistemaPrioridades:
    def __init__(self):
        self.heap = []
        self.contador = 0  # Para romper empates en prioridad

    def agregar_tarea(self, nombre, prioridad):
        """Agrega tarea con prioridad. Usa -prioridad para simular max-heap."""
        heapq.heappush(self.heap, (-prioridad, self.contador, nombre))
        self.contador += 1

    def extraer_tarea(self):
        """Extrae la tarea con mayor prioridad."""
        if not self.heap:
            return None
        neg_prioridad, _, nombre = heapq.heappop(self.heap)
        return nombre, -neg_prioridad

    def mostrar_heap(self):
        """Devuelve una lista ordenada por prioridad (descendente)."""
        return sorted(self.heap, key=lambda x: (x[0], x[1]))

    def esta_vacia(self):
        return len(self.heap) == 0

    def eliminar_tarea(self, nombre):
        """Elimina una tarea por nombre (búsqueda lineal)."""
        for i, (_, _, nombre_tarea) in enumerate(self.heap):
            if nombre_tarea == nombre:
                # Eliminar y reconstruir heap
                del self.heap[i]
                heapq.heapify(self.heap)
                return True
        return False

    def editar_tarea(self, nombre_viejo, nombre_nuevo, nueva_prioridad):
        """Edita una tarea existente."""
        if self.eliminar_tarea(nombre_viejo):
            self.agregar_tarea(nombre_nuevo, nueva_prioridad)
            return True
        return False


# === VENTANA PRINCIPAL ===
class VentanaPrioridades(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Sistema de Prioridades con Heap")
        self.setGeometry(100, 100, 1100, 750)
        self.setFixedSize(1100, 750)

        # Fondo
        self.fondo = FondoSuave()
        self.setCentralWidget(self.fondo)

        # Layout principal
        layout_principal = QVBoxLayout(self.fondo)

        # Título
        titulo = QLabel("GESTIÓN DE TAREAS CON HEAP")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color: #2c3e50;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #2ecc71);
            color: white;
            border-radius: 15px;
            margin-bottom: 10px;
        """)
        layout_principal.addWidget(titulo)

        # Descripción
        desc = QLabel("Sistema basado en montículo (heap) para gestión de tareas por prioridad.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout_principal.addWidget(desc)

        # Panel dividido
        splitter_panel = QFrame()
        splitter_layout = QHBoxLayout(splitter_panel)
        layout_principal.addWidget(splitter_panel)

        # === PANEL IZQUIERDO: CONTROLES ===
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")
        layout_izq = QVBoxLayout(panel_izq)

        # Título
        lbl_form = QLabel("➕ Gestión de Tareas")
        lbl_form.setFont(QFont("Arial", 14, QFont.Bold))
        lbl_form.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout_izq.addWidget(lbl_form)

        # Formulario
        form_layout = QVBoxLayout()

        # Nombre
        form_layout.addWidget(QLabel("Nombre de la tarea:"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Finalizar informe")
        form_layout.addWidget(self.input_nombre)

        # Prioridad
        form_layout.addWidget(QLabel("Prioridad (1-10):"))
        self.spinbox_prioridad = QSpinBox()
        self.spinbox_prioridad.setRange(1, 10)
        self.spinbox_prioridad.setValue(5)
        form_layout.addWidget(self.spinbox_prioridad)

        layout_izq.addLayout(form_layout)

        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("➕ Agregar Tarea")
        btn_agregar.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_agregar.clicked.connect(self.agregar_tarea)

        btn_extraer = QPushButton("✅ Extraer Prioritaria")
        btn_extraer.setStyleSheet("""
            background-color: #e67e22;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_extraer.clicked.connect(self.extraer_tarea)

        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_extraer)
        layout_izq.addLayout(btn_layout)

        # Información
        self.label_info = QLabel("Tareas: 0")
        self.label_info.setStyleSheet("color: #7f8c8d; font-weight: bold; margin-top: 10px;")
        layout_izq.addWidget(self.label_info)

        # Botones adicionales
        btns_extra = QHBoxLayout()
        btn_editar = QPushButton("✏️ Editar")
        btn_editar.setStyleSheet("background: #3498db; color: white; padding: 8px;")
        btn_editar.clicked.connect(self.editar_tarea)

        btn_eliminar = QPushButton("🗑️ Eliminar")
        btn_eliminar.setStyleSheet("background: #e74c3c; color: white; padding: 8px;")
        btn_eliminar.clicked.connect(self.eliminar_tarea)

        btns_extra.addWidget(btn_editar)
        btns_extra.addWidget(btn_eliminar)
        layout_izq.addLayout(btns_extra)

        # === PANEL DERECHO: LISTA DE TAREAS ===
        panel_der = QWidget()
        panel_der.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")
        layout_der = QVBoxLayout(panel_der)

        layout_der.addWidget(QLabel("📋 Lista de Tareas (Ordenadas por Prioridad)"))
        self.tabla_tareas = QTableWidget()
        self.tabla_tareas.setColumnCount(3)
        self.tabla_tareas.setHorizontalHeaderLabels(["Tarea", "Prioridad", "Acción"])
        self.tabla_tareas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_tareas.verticalHeader().setVisible(False)
        layout_der.addWidget(self.tabla_tareas)

        # Añadir paneles
        splitter_layout.addWidget(panel_izq)
        splitter_layout.addWidget(panel_der)
        splitter_layout.setStretch(0, 1)
        splitter_layout.setStretch(1, 2)

        # Inicializar sistema
        self.sistema = SistemaPrioridades()
        self.mostrar_tareas()

    def validar_datos(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre de la tarea no puede estar vacío.")
            return None, None
        prioridad = self.spinbox_prioridad.value()
        return nombre, prioridad

    def agregar_tarea(self):
        nombre, prioridad = self.validar_datos()
        if nombre and prioridad:
            self.sistema.agregar_tarea(nombre, prioridad)
            QMessageBox.information(self, "Éxito", f"Tarea '{nombre}' agregada con prioridad {prioridad}.")
            self.input_nombre.clear()
            self.mostrar_tareas()

    def extraer_tarea(self):
        if self.sistema.esta_vacia():
            QMessageBox.information(self, "Sin tareas", "No hay tareas para extraer.")
            return
        nombre, prioridad = self.sistema.extraer_tarea()
        QMessageBox.information(
            self, "Tarea Extraída",
            f"✅ Tarea más urgente: '{nombre}' (Prioridad: {prioridad})"
        )
        self.mostrar_tareas()

    def mostrar_tareas(self):
        self.tabla_tareas.setRowCount(0)
        tareas = self.sistema.mostrar_heap()
        for neg_prioridad, _, nombre in tareas:
            prioridad = -neg_prioridad
            row = self.tabla_tareas.rowCount()
            self.tabla_tareas.insertRow(row)
            self.tabla_tareas.setItem(row, 0, QTableWidgetItem(nombre))
            self.tabla_tareas.setItem(row, 1, QTableWidgetItem(str(prioridad)))

            # Botón de selección para editar/eliminar
            btn = QPushButton("Seleccionar")
            btn.setStyleSheet("background: #9b59b6; color: white; padding: 5px;")
            btn.clicked.connect(lambda _, n=nombre: self.seleccionar_tarea(n))
            self.tabla_tareas.setCellWidget(row, 2, btn)

            # Color por prioridad
            color = self.get_color_por_prioridad(prioridad)
            for col in [0, 1]:
                self.tabla_tareas.item(row, col).setBackground(QColor(color))

        self.actualizar_info()

    def get_color_por_prioridad(self, prioridad):
        """Devuelve un color suave basado en la prioridad."""
        if prioridad >= 8:
            return "#ffebee"  # Rojo claro
        elif prioridad >= 6:
            return "#fff3e0"  # Naranja claro
        elif prioridad >= 4:
            return "#e8f5e8"  # Verde claro
        else:
            return "#e3f2fd"  # Azul claro

    def actualizar_info(self):
        total = len(self.sistema.heap)
        self.label_info.setText(f"Tareas: {total}")

    def seleccionar_tarea(self, nombre):
        tarea_seleccionada = None
        for neg_prioridad, _, nombre_tarea in self.sistema.heap:
            if nombre_tarea == nombre:
                tarea_seleccionada = (nombre_tarea, -neg_prioridad)
                break
        if tarea_seleccionada:
            self.input_nombre.setText(tarea_seleccionada[0])
            self.spinbox_prioridad.setValue(tarea_seleccionada[1])

    def editar_tarea(self):
        nombre_viejo = self.input_nombre.text().strip()
        if not nombre_viejo:
            QMessageBox.warning(self, "Error", "Primero selecciona una tarea para editar.")
            return
        nombre_nuevo, prioridad = self.validar_datos()
        if nombre_nuevo and prioridad:
            if self.sistema.editar_tarea(nombre_viejo, nombre_nuevo, prioridad):
                QMessageBox.information(self, "Éxito", f"Tarea '{nombre_viejo}' actualizada.")
                self.input_nombre.clear()
                self.mostrar_tareas()
            else:
                QMessageBox.warning(self, "Error", "No se pudo editar la tarea.")

    def eliminar_tarea(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "Primero selecciona una tarea para eliminar.")
            return
        if self.sistema.eliminar_tarea(nombre):
            QMessageBox.information(self, "Éxito", f"Tarea '{nombre}' eliminada.")
            self.input_nombre.clear()
            self.mostrar_tareas()
        else:
            QMessageBox.warning(self, "Error", "Tarea no encontrada.")


# === EJECUCIÓN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrioridades()
    ventana.show()
    sys.exit(app.exec_())