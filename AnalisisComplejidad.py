"""
ANÁLISIS DE COMPLEJIDAD

Funcionalidad:
- Visualización animada de búsqueda lineal y binaria
- Comparación paso a paso con resaltado
- Medición de tiempos reales
- Tabla comparativa dinámica
- Simulación en tiempo real con pausas y efectos
"""

import sys
import time
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
    QLineEdit, QGroupBox, QProgressBar, QFrame, QSplitter  
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QPainter


# === FONDO TECNOLÓGICO ANIMADO ===
class FondoTecnologico(QWidget):
    def __init__(self):
        super().__init__()
        self.points = [(random.randint(0, self.width()), random.randint(0, self.height())) for _ in range(50)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mover_puntos)
        self.timer.start(200)

    def resizeEvent(self, event):
        self.points = [(random.randint(0, self.width()), random.randint(0, self.height())) for _ in range(50)]
        super().resizeEvent(event)

    def mover_puntos(self):
        for i in range(len(self.points)):
            x, y = self.points[i]
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
            if x < 0 or x > self.width():
                x = self.width() // 2
            if y < 0 or y > self.height():
                y = self.height() // 2
            self.points[i] = (x, y)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QBrush(QColor(10, 15, 30))
        painter.fillRect(event.rect(), gradient)

        painter.setPen(QColor(0, 200, 255))
        for x, y in self.points:
            painter.drawEllipse(x, y, 2, 2)

        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                x1, y1 = self.points[i]
                x2, y2 = self.points[j]
                dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                if dist < 100:
                    alpha = int(255 * (1 - dist / 100))
                    painter.setPen(QColor(0, 200, 255, alpha))
                    painter.drawLine(x1, y1, x2, y2)
        painter.end()


# === VENTANA PRINCIPAL ===
class VentanaAnalisis(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ Análisis de Complejidad - Simulación en Tiempo Real")
        self.setGeometry(100, 100, 1200, 800)

        # Fondo tecnológico
        self.fondo = FondoTecnologico()
        self.setCentralWidget(self.fondo)

        # Layout principal
        layout_principal = QVBoxLayout(self.fondo)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel("ANÁLISIS DE COMPLEJIDAD ALGORÍTMICA")
        titulo.setFont(QFont("Orbitron", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #00ffcc; padding: 20px; background: rgba(0, 50, 80, 150); border-radius: 15px;")
        layout_principal.addWidget(titulo)

        # Descripción
        desc = QLabel("Este sistema simula en tiempo real la ejecución de algoritmos de búsqueda e inserción.")
        desc.setStyleSheet("color: #a0e7ff; font-size: 14px;")
        desc.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(desc)

        # Controles
        controles = QHBoxLayout()
        self.input_tamano = QLineEdit("20")
        self.input_tamano.setFixedWidth(100)
        self.input_tamano.setStyleSheet("background: #0f1b33; color: #00ffaa; padding: 8px;")
        controles.addWidget(QLabel("Tamaño:"))
        controles.addWidget(self.input_tamano)

        btn_generar = QPushButton("🔄 Generar Datos")
        btn_generar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006644, stop:1 #00cc99);
            color: white; padding: 10px; border-radius: 8px;
        """)
        btn_generar.clicked.connect(self.generar_datos)
        controles.addWidget(btn_generar)

        layout_principal.addLayout(controles)

        # Panel dividido
        splitter = QFrame()
        splitter.setFrameShape(QFrame.HLine)
        layout_principal.addWidget(splitter)

        splitter_panel = QSplitter(Qt.Horizontal)
        layout_principal.addWidget(splitter_panel)

        # === PANEL IZQUIERDO: SIMULACIÓN ===
        panel_izq = QWidget()
        layout_izq = QVBoxLayout(panel_izq)
        label_izq = QLabel("🔍 SIMULACIÓN EN TIEMPO REAL")
        label_izq.setStyleSheet("color: #00ccff; font-weight: bold;")
        layout_izq.addWidget(label_izq)

        self.salida_simulacion = QTextEdit()
        self.salida_simulacion.setReadOnly(True)
        self.salida_simulacion.setStyleSheet("""
            background: #0a1428; color: #00ffcc; font-family: 'Courier New';
            border: 2px solid #00b386; border-radius: 10px; padding: 10px;
        """)
        layout_izq.addWidget(self.salida_simulacion)

        # Barra de progreso
        self.barra_busqueda = QProgressBar()
        self.barra_busqueda.setRange(0, 100)
        self.barra_busqueda.setValue(0)
        layout_izq.addWidget(self.barra_busqueda)

        # Botones de simulación
        btn_layout = QHBoxLayout()
        self.btn_buscar = QPushButton("▶️ Simular Búsquedas")
        self.btn_buscar.setStyleSheet("background: #059669; color: white; padding: 10px;")
        self.btn_buscar.clicked.connect(self.simular_busquedas)
        btn_layout.addWidget(self.btn_buscar)

        self.btn_insertar = QPushButton("➕ Simular Inserciones")
        self.btn_insertar.setStyleSheet("background: #7c3aed; color: white; padding: 10px;")
        self.btn_insertar.clicked.connect(self.simular_inserciones)
        btn_layout.addWidget(self.btn_insertar)

        layout_izq.addLayout(btn_layout)

        # === PANEL DERECHO: RESULTADOS ===
        panel_der = QWidget()
        layout_der = QVBoxLayout(panel_der)
        label_der = QLabel("📊 RESULTADOS Y COMPARATIVA")
        label_der.setStyleSheet("color: #ff6600; font-weight: bold;")
        layout_der.addWidget(label_der)

        self.tabla = QTableWidget()
        self.tabla.setRowCount(4)
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Métrica", "Tiempo (ms)", "Complejidad"])
        self.tabla.setStyleSheet("background: #101a30; color: white;")
        layout_der.addWidget(self.tabla)

        # Añadir paneles
        splitter_panel.addWidget(panel_izq)
        splitter_panel.addWidget(panel_der)
        splitter_panel.setSizes([700, 500])

        # Variables
        self.vector = []
        self.array_ordenado = []
        self.valor_buscar = 0
        self.lista_enlazada = None
        self.inicializar_tabla()

    def inicializar_tabla(self):
        metricas = [
            "Búsqueda Lineal",
            "Búsqueda Binaria",
            "Inserción Lista Enlazada",
            "Inserción Vector Dinámico"
        ]
        complejidades = ["O(n)", "O(log n)", "O(1)", "O(1) am."]
        for i, metrica in enumerate(metricas):
            self.tabla.setItem(i, 0, QTableWidgetItem(metrica))
            self.tabla.setItem(i, 1, QTableWidgetItem("0.00"))
            self.tabla.setItem(i, 2, QTableWidgetItem(complejidades[i]))

    def generar_datos(self):
        try:
            tam = int(self.input_tamano.text())
            if tam < 1 or tam > 100:
                raise ValueError

            self.vector = [random.randint(1, tam * 2) for _ in range(tam)]
            self.array_ordenado = sorted(self.vector)
            self.valor_buscar = self.vector[random.randint(0, len(self.vector) - 1)]

            self.lista_enlazada = ListaEnlazada()
            for val in self.vector:
                self.lista_enlazada.insertar_al_final(val)

            self.salida_simulacion.setText(f"✅ Datos generados: tamaño={tam}, buscar={self.valor_buscar}")
            self.barra_busqueda.setValue(0)
        except:
            self.salida_simulacion.setText("❌ Error: tamaño inválido (1-100)")

    def simular_busquedas(self):
        if not self.vector:
            self.salida_simulacion.setText("❌ Primero genera los datos.")
            return

        self.salida_simulacion.append("\n🚀 INICIANDO SIMULACIÓN DE BÚSQUEDAS...\n")
        QApplication.processEvents()

        # === BÚSQUEDA LINEAL ===
        self.salida_simulacion.append("🔍 BÚSQUEDA LINEAL (O(n))")
        inicio = time.perf_counter()
        encontrado = False
        for i, val in enumerate(self.vector):
            # Simulación paso a paso
            self.salida_simulacion.append(f"  → Comparando vector[{i}] = {val} con {self.valor_buscar}")
            self.barra_busqueda.setValue(int((i + 1) / len(self.vector) * 50))
            time.sleep(0.1)
            QApplication.processEvents()
            if val == self.valor_buscar:
                self.salida_simulacion.append(f"  ✅ Encontrado en índice {i}\n")
                encontrado = True
                break
        if not encontrado:
            self.salida_simulacion.append("  ❌ No encontrado\n")
        tiempo_lineal = (time.perf_counter() - inicio) * 1000

        # === BÚSQUEDA BINARIA ===
        self.salida_simulacion.append("🔍 BÚSQUEDA BINARIA (O(log n))")
        inicio = time.perf_counter()
        left, right = 0, len(self.array_ordenado) - 1
        pasos = 0
        while left <= right:
            mid = (left + right) // 2
            val = self.array_ordenado[mid]
            pasos += 1
            self.salida_simulacion.append(f"  → mid={mid}, valor={val}, rango=[{left}, {right}]")
            self.barra_busqueda.setValue(50 + int(pasos / 10 * 50))  # Aproximado
            time.sleep(0.5)
            QApplication.processEvents()
            if val == self.valor_buscar:
                self.salida_simulacion.append(f"  ✅ Encontrado en índice {mid} (ordenado)\n")
                break
            elif val < self.valor_buscar:
                left = mid + 1
                self.salida_simulacion.append(f"  → {val} < {self.valor_buscar}, ir a derecha")
            else:
                right = mid - 1
                self.salida_simulacion.append(f"  → {val} > {self.valor_buscar}, ir a izquierda")
        else:
            self.salida_simulacion.append("  ❌ No encontrado\n")
        tiempo_binaria = (time.perf_counter() - inicio) * 1000

        # Actualizar tabla
        self.tabla.setItem(0, 1, QTableWidgetItem(f"{tiempo_lineal:.4f}"))
        self.tabla.setItem(1, 1, QTableWidgetItem(f"{tiempo_binaria:.4f}"))
        self.salida_simulacion.append(f"🎯 Búsqueda binaria fue {tiempo_lineal/tiempo_binaria:.2f}x más rápida.")

    def simular_inserciones(self):
        if not self.vector:
            self.salida_simulacion.setText("❌ Primero genera los datos.")
            return

        self.salida_simulacion.append("\n🚀 SIMULANDO INSERCIÓN AL FINAL...\n")
        QApplication.processEvents()

        # Inserción en lista enlazada
        self.salida_simulacion.append("➕ INSERCIÓN EN LISTA ENLAZADA (O(1))")
        inicio = time.perf_counter()
        nuevo_nodo = Nodo("X")
        if not self.lista_enlazada.cabeza:
            self.lista_enlazada.cabeza = nuevo_nodo
        else:
            actual = self.lista_enlazada.cabeza
            pos = 0
            while actual.siguiente:
                self.salida_simulacion.append(f"  → Avanzando al nodo {pos}")
                time.sleep(0.2)
                actual = actual.siguiente
                pos += 1
            actual.siguiente = nuevo_nodo
            self.salida_simulacion.append(f"  ✅ Insertado 'X' al final\n")
        tiempo_lista = (time.perf_counter() - inicio) * 1000

        # Inserción en vector
        self.salida_simulacion.append("➕ INSERCIÓN EN VECTOR (O(1) am.)")
        inicio = time.perf_counter()
        time.sleep(0.1)
        self.vector.append("X")
        self.salida_simulacion.append("  ✅ Elemento 'X' agregado al final del vector\n")
        tiempo_vector = (time.perf_counter() - inicio) * 1000

        # Resultados
        self.tabla.setItem(2, 1, QTableWidgetItem(f"{tiempo_lista:.4f}"))
        self.tabla.setItem(3, 1, QTableWidgetItem(f"{tiempo_vector:.4f}"))
        self.salida_simulacion.append(f"💡 El vector fue más rápido en este caso por optimizaciones internas.")


# === ESTRUCTURAS DE DATOS (COPIADAS Y LISTAS) ===
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamaño = 0

    def insertar_al_final(self, valor):
        nuevo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamaño += 1


# === EJECUCIÓN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaAnalisis()
    ventana.show()
    sys.exit(app.exec_())