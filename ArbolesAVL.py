"""
SISTEMA AVL 
"""

import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QSplitter
)
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QLinearGradient
)


# === ESTRUCTURA AVL ===
class NodoAVL:
    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None
        self.altura = 1


def obtener_altura(nodo):
    return nodo.altura if nodo else 0


def actualizar_altura(nodo):
    if nodo:
        nodo.altura = 1 + max(obtener_altura(nodo.izq), obtener_altura(nodo.der))


def obtener_balance(nodo):
    return obtener_altura(nodo.izq) - obtener_altura(nodo.der) if nodo else 0


def rotar_derecha(y):
    x = y.izq
    T2 = x.der
    x.der = y
    y.izq = T2
    actualizar_altura(y)
    actualizar_altura(x)
    return x


def rotar_izquierda(x):
    y = x.der
    T2 = y.izq
    y.izq = x
    x.der = T2
    actualizar_altura(x)
    actualizar_altura(y)
    return y


def insertar_avl(raiz, clave, historial):
    if not raiz:
        historial.append(f"Insertando <b>{clave}</b> como nuevo nodo.")
        return NodoAVL(clave)

    if clave < raiz.clave:
        historial.append(f"➡️  {clave} < {raiz.clave} → a la izquierda")
        raiz.izq = insertar_avl(raiz.izq, clave, historial)
    elif clave > raiz.clave:
        historial.append(f"➡️  {clave} > {raiz.clave} → a la derecha")
        raiz.der = insertar_avl(raiz.der, clave, historial)
    else:
        historial.append(f"<b>Duplicado:</b> {clave} ya existe.")
        return raiz

    actualizar_altura(raiz)
    balance = obtener_balance(raiz)

    # Caso LL
    if balance > 1 and clave < raiz.izq.clave:
        historial.append(f"⚖️  <b>Rotación Derecha (LL)</b> en {raiz.clave}")
        return rotar_derecha(raiz)

    # Caso RR
    if balance < -1 and clave > raiz.der.clave:
        historial.append(f"⚖️  <b>Rotación Izquierda (RR)</b> en {raiz.clave}")
        return rotar_izquierda(raiz)

    # Caso LR
    if balance > 1 and clave > raiz.izq.clave:
        historial.append(f"⚖️  <b>Rotación Doble: LR</b> en {raiz.clave}")
        raiz.izq = rotar_izquierda(raiz.izq)
        return rotar_derecha(raiz)

    # Caso RL
    if balance < -1 and clave < raiz.der.clave:
        historial.append(f"⚖️  <b>Rotación Doble: RL</b> en {raiz.clave}")
        raiz.der = rotar_derecha(raiz.der)
        return rotar_izquierda(raiz)

    return raiz


# === WIDGET DE DIBUJO DEL ÁRBOL ===
class VisualizadorAVL(QWidget):
    def __init__(self):
        super().__init__()
        self.raiz = None
        self.radio = 20
        self.nivel_dist = 60
        self.hijo_dist = 80

    def set_arbol(self, raiz):
        self.raiz = raiz
        self.update()  # Redibuja

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QColor(10, 15, 30))  # Fondo oscuro

        if self.raiz:
            self._dibujar_nodo(painter, self.raiz, self.width() // 2, 60, self.width() // 4)

    def _dibujar_nodo(self, painter, nodo, x, y, offset):
        # Coordenadas hijo
        x_izq = x - offset
        x_der = x + offset
        y_siguiente = y + self.nivel_dist

        # Líneas a hijos
        pen = QPen(QColor("#00cc4e"))
        pen.setWidth(2)
        painter.setPen(pen)

        if nodo.izq:
            painter.drawLine(x, y + self.radio, x_izq, y_siguiente - self.radio)
            self._dibujar_nodo(painter, nodo.izq, x_izq, y_siguiente, max(30, offset // 2))

        if nodo.der:
            painter.drawLine(x, y + self.radio, x_der, y_siguiente - self.radio)
            self._dibujar_nodo(painter, nodo.der, x_der, y_siguiente, max(30, offset // 2))

        # Nodo actual
        color_fondo = QColor("#587cef") if obtener_balance(nodo) == 0 else \
                      QColor("#dd9d13") if obtener_balance(nodo) > 1 or obtener_balance(nodo) < -1 else \
                      QColor("#0891b2")
        brush = QBrush(color_fondo)
        painter.setBrush(brush)
        painter.setPen(QPen(QColor("white"), 2))
        rect = QRectF(x - self.radio, y - self.radio, 2 * self.radio, 2 * self.radio)
        painter.drawEllipse(rect)

        # Texto: clave y balance
        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{nodo.clave}\n{obtener_balance(nodo)}")


# === VENTANA PRINCIPAL ===
class VentanaAVL(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVL Tree")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("background: #0a0e2a; color: white;")

        # Divisor horizontal
        splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitter)

        # === PANEL IZQUIERDO: VISUALIZACIÓN DEL ÁRBOL ===
        panel_izq = QWidget()
        layout_izq = QVBoxLayout(panel_izq)
        label_izq = QLabel("SIMULACIÓN DEL ÁRBOL AVL")
        label_izq.setAlignment(Qt.AlignCenter)
        label_izq.setStyleSheet("color: #00ffcc; font: bold 16px 'Orbitron'; padding: 10px;")
        layout_izq.addWidget(label_izq)

        self.visualizador = VisualizadorAVL()
        layout_izq.addWidget(self.visualizador)

        # Controles de inserción
        input_layout = QHBoxLayout()
        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("Ingresa un número...")
        self.input_clave.setStyleSheet("""
            background: #0f1b33; color: #00ffaa; padding: 10px; border-radius: 8px;
        """)
        btn_insertar = QPushButton("Insertar")
        btn_insertar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006644, stop:1 #00cc99);
            color: white; font-weight: bold; padding: 10px; border-radius: 8px;
        """)
        btn_insertar.clicked.connect(self.insertar_nodo)
        input_layout.addWidget(self.input_clave)
        input_layout.addWidget(btn_insertar)
        layout_izq.addLayout(input_layout)

        # Secuencias predefinidas
        secuencia_layout = QHBoxLayout()
        for nombre, datos in [
            ("LL: 30,20,10", [30, 20, 10]),
            ("RR: 10,20,30", [10, 20, 30]),
            ("LR: 30,10,20", [30, 10, 20]),
            ("RL: 10,30,20", [10, 30, 20])
        ]:
            btn = QPushButton(nombre)
            btn.setStyleSheet("background: #1e3a8a; color: white; padding: 8px;")
            btn.clicked.connect(lambda _, d=datos: self.insertar_secuencia(d))
            secuencia_layout.addWidget(btn)
        layout_izq.addLayout(secuencia_layout)

        # === PANEL DERECHO: HISTORIAL ===
        panel_der = QWidget()
        layout_der = QVBoxLayout(panel_der)
        label_der = QLabel("HISTORIAL")
        label_der.setAlignment(Qt.AlignCenter)
        label_der.setStyleSheet("color: #ff6600; font: bold 16px 'Orbitron'; padding: 10px;")
        layout_der.addWidget(label_der)

        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setStyleSheet("""
            background: #0a1428; color: #00ffcc; font-family: 'Courier New';
            border: 2px solid #00b386; border-radius: 10px; padding: 10px;
        """)
        layout_der.addWidget(self.historial)

        # Añadir paneles al splitter
        splitter.addWidget(panel_izq)
        splitter.addWidget(panel_der)
        splitter.setSizes([800, 600])  # Ajusta anchos

        # Estado inicial
        self.raiz = None
        self.historial.append("<h3>Sistema AVL Inicializado</h3>")
        self.historial.append("Inserta nodos o usa una secuencia predefinida.")

    def insertar_nodo(self):
        try:
            clave = int(self.input_clave.text())
            historial_local = []
            self.raiz = insertar_avl(self.raiz, clave, historial_local)
            for linea in historial_local:
                self.historial.append(linea)
            self.visualizador.set_arbol(self.raiz)
            self.input_clave.clear()
        except ValueError:
            self.historial.append("<b>Error:</b> Ingresa un número válido.")

    def insertar_secuencia(self, secuencia):
        self.historial.append(f"<h4>Secuencia: {secuencia}</h4>")
        for clave in secuencia:
            time.sleep(0.7)
            historial_local = []
            self.raiz = insertar_avl(self.raiz, clave, historial_local)
            for linea in historial_local:
                self.historial.append(linea)
            self.visualizador.set_arbol(self.raiz)
            QApplication.processEvents()  # Actualiza UI durante animación


# === EJECUCIÓN ===
if __name__ == "__main__":
    import random
    app = QApplication(sys.argv)
    ventana = VentanaAVL()
    ventana.show()
    sys.exit(app.exec_())