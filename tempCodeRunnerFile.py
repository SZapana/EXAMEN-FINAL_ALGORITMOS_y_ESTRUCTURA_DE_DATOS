"""
SISTEMA AVL VISUAL - INTERFAZ FUTURISTA CON PYQT5
Autor: [Tu Nombre]
Docente: Mg. Aldo Hernán Zanabria Gálvez
Curso: Estructuras de Datos

Funcionalidad:
- Visualización animada de inserciones en AVL
- Muestra rotaciones (LL, RR, LR, RL) en tiempo real
- Fondo tecnológico con efecto "Matrix"
- Árbol mostrado jerárquicamente con colores
"""

import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QPainter, QBrush, QLinearGradient, QIcon
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
        historial.append(f"🟢 Insertando nodo <b>{clave}</b> como raíz.")
        return NodoAVL(clave)

    if clave < raiz.clave:
        historial.append(f"➡️  {clave} < {raiz.clave}: bajando a la izquierda...")
        raiz.izq = insertar_avl(raiz.izq, clave, historial)
    elif clave > raiz.clave:
        historial.append(f"➡️  {clave} > {raiz.clave}: bajando a la derecha...")
        raiz.der = insertar_avl(raiz.der, clave, historial)
    else:
        historial.append(f"🟨 Duplicado: <b>{clave}</b> ya existe.")
        return raiz

    actualizar_altura(raiz)
    balance = obtener_balance(raiz)

    # Rotaciones
    if balance > 1:
        if clave < raiz.izq.clave:
            historial.append(f"⚖️  <b>Rotación Derecha (LL)</b> en {raiz.clave}")
            return rotar_derecha(raiz)
        else:
            historial.append(f"⚖️  <b>Rotación LR</b> en {raiz.clave}")
            raiz.izq = rotar_izquierda(raiz.izq)
            return rotar_derecha(raiz)
    if balance < -1:
        if clave > raiz.der.clave:
            historial.append(f"⚖️  <b>Rotación Izquierda (RR)</b> en {raiz.clave}")
            return rotar_izquierda(raiz)
        else:
            historial.append(f"⚖️  <b>Rotación RL</b> en {raiz.clave}")
            raiz.der = rotar_derecha(raiz.der)
            return rotar_izquierda(raiz)

    return raiz


# === WIDGET DE FONDO MATRIX ===
class FondoMatrix(QWidget):
    def __init__(self):
        super().__init__()
        self.drops = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_drops)
        self.timer.start(33)  # 30 FPS
        self.init_drops()

    def init_drops(self):
        self.drops = [[random.randint(0, self.width()), -random.randint(0, 600)] for _ in range(50)]

    def update_drops(self):
        self.drops = [[x, y + 5] if y < self.height() else [random.randint(0, self.width()), -20] for x, y in self.drops]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(10, 15, 30))  # Fondo oscuro profundo

        painter.setOpacity(0.7)
        for x, y in self.drops:
            color = QColor(0, 255, 180) if random.random() > 0.9 else QColor(0, 180, 120)
            painter.setPen(color)
            painter.drawText(x, int(y), "1")
        painter.end()


# === VENTANA PRINCIPAL ===
class VentanaAVL(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌳 AVL Tree Visualizer - Sistema Inteligente")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("https://img.icons8.com/ios-filled/50/000000/binary-search-tree.png"))

        # Fondo
        self.fondo = FondoMatrix()
        self.setCentralWidget(self.fondo)

        # Contenedor principal
        contenedor = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(contenedor)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        self.fondo.layout = QVBoxLayout(self.fondo)
        self.fondo.layout.addWidget(scroll)

        # Título
        titulo = QLabel("ÁRBOL AVL - AUTO-BALANCEO EN TIEMPO REAL")
        titulo.setFont(QFont("Orbitron", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color: #00ffcc;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0a0e2a, stop:1 #1a1a4a);
            border-radius: 15px;
            border: 2px solid #00b386;
        """)
        contenedor.addWidget(titulo)

        # Descripción
        desc = QLabel(
            "Este sistema simula la inserción en un Árbol AVL, mostrando rotaciones (LL, RR, LR, RL)\n"
            "y comparando con un BST tradicional. El AVL mantiene balance para garantizar O(log n)."
        )
        desc.setStyleSheet("color: #a0e7ff; font-size: 14px; font-family: 'Courier New';")
        desc.setAlignment(Qt.AlignCenter)
        contenedor.addWidget(desc)

        # Entrada
        hbox = QHBoxLayout()
        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("Ingresa un número...")
        self.input_clave.setStyleSheet("""
            background: #0f1b33; color: #00ffaa; padding: 10px; border: 1px solid #00b386;
            border-radius: 8px; font-size: 16px;
        """)
        btn_insertar = QPushButton("➕ Insertar")
        btn_insertar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006644, stop:1 #00cc99);
            color: white; font-weight: bold; padding: 10px; border-radius: 8px;
        """)
        btn_insertar.clicked.connect(self.insertar_nodo)
        hbox.addWidget(self.input_clave)
        hbox.addWidget(btn_insertar)
        contenedor.addLayout(hbox)

        # Botones rápidos
        botones = QHBoxLayout()
        secuencias = [
            ("Secuencia LL", [30, 20, 10]),
            ("Secuencia RR", [10, 20, 30]),
            ("Secuencia LR", [30, 10, 20]),
            ("Secuencia RL", [10, 30, 20]),
        ]
        for texto, datos in secuencias:
            btn = QPushButton(texto)
            btn.setStyleSheet("""
                background: #1e3a8a; color: white; padding: 8px; border-radius: 6px;
            """)
            btn.clicked.connect(lambda _, d=datos: self.insertar_secuencia(d))
            botones.addWidget(btn)
        contenedor.addLayout(botones)

        # Historial
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        self.historial.setStyleSheet("""
            background: #0a1428; color: #00ffcc; font-family: 'Courier New';
            border: 2px solid #00b386; border-radius: 10px; padding: 10px;
        """)
        contenedor.addWidget(QLabel("📋 Historial de Operaciones:", styleSheet="color: #00ccff;"))
        contenedor.addWidget(self.historial)

        # Estado del árbol
        self.etiqueta_arbol = QLabel("🌲 Árbol AVL: Vacío")
        self.etiqueta_arbol.setStyleSheet("color: #ff6600; font-size: 16px; font-weight: bold;")
        self.etiqueta_arbol.setAlignment(Qt.AlignCenter)
        contenedor.addWidget(self.etiqueta_arbol)

        # Inicializar
        self.raiz = None
        self.historial.append("<b>🟢 Sistema AVL inicializado. Listo para inserciones.</b>")

    def insertar_nodo(self):
        try:
            clave = int(self.input_clave.text())
            historial_local = []
            self.raiz = insertar_avl(self.raiz, clave, historial_local)
            for linea in historial_local:
                self.historial.append(linea)
            self.actualizar_vista_arbol()
            self.input_clave.clear()
        except ValueError:
            self.historial.append("❌ <b>Error:</b> Ingresa un número válido.")

    def insertar_secuencia(self, secuencia):
        self.historial.append(f"<b>⚡ Insertando secuencia: {secuencia}</b>")
        for clave in secuencia:
            time.sleep(0.8)
            historial_local = []
            self.raiz = insertar_avl(self.raiz, clave, historial_local)
            for linea in historial_local:
                self.historial.append(linea)
            self.actualizar_vista_arbol()

    def actualizar_vista_arbol(self):
        if not self.raiz:
            self.etiqueta_arbol.setText("🌲 Árbol AVL: Vacío")
            return

        resultado = []
        self._inorder(self.raiz, resultado)
        arbol_str = " → ".join(map(str, resultado))
        self.etiqueta_arbol.setText(f"✅ Árbol AVL (in-order): {arbol_str}")

    def _inorder(self, nodo, lista):
        if nodo:
            self._inorder(nodo.izq, lista)
            lista.append(nodo.clave)
            self._inorder(nodo.der, lista)


# === EJECUCIÓN ===
if __name__ == "__main__":
    import random
    app = QApplication(sys.argv)
    ventana = VentanaAVL()
    ventana.show()
    sys.exit(app.exec_())