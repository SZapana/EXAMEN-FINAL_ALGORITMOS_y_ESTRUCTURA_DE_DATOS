"""
COMPRESOR DE TEXTO CON ÁRBOL DE HUFFMAN

Funcionalidad:
- Codificación Huffman de texto
- Interfaz gráfica profesional con PyQt5
- Tabla de frecuencias, árbol, texto codificado
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QScrollArea, QFileDialog, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QLinearGradient
)


# === ESTRUCTURA: NODO DE HUFFMAN ===
class NodoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# === ALGORITMO DE HUFFMAN ===
class HuffmanCoder:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        self.root = None

    def build_tree(self, text):
        if not text:
            return None

        # Frecuencias
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1

        # Cola de prioridad
        heap = [NodoHuffman(char, f) for char, f in freq.items()]
        heap.sort(key=lambda x: x.freq)

        # Construir árbol
        while len(heap) > 1:
            left = heap.pop(0)
            right = heap.pop(0)
            merged = NodoHuffman(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            # Insertar manteniendo orden
            i = 0
            while i < len(heap) and heap[i].freq < merged.freq:
                i += 1
            heap.insert(i, merged)

        self.root = heap[0] if heap else None
        self._generate_codes(self.root, "")
        return freq

    def _generate_codes(self, node, current_code):
        if not node:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
        else:
            self._generate_codes(node.left, current_code + "0")
            self._generate_codes(node.right, current_code + "1")

    def encode(self, text):
        return ''.join(self.codes.get(char, '') for char in text)

    def get_compression_ratio(self, original, encoded):
        original_bits = len(original) * 8  # Suponiendo 8 bits por carácter
        compressed_bits = len(encoded)
        ratio = (1 - compressed_bits / original_bits) * 100 if original_bits > 0 else 0
        return ratio, original_bits, compressed_bits


# === WIDGET DE DIBUJO DEL ÁRBOL DE HUFFMAN ===
class VisualizadorHuffman(QWidget):
    def __init__(self):
        super().__init__()
        self.root = None
        self.radio = 15
        self.nivel_dist = 60
        self.hijo_dist = 80

    def set_tree(self, root):
        self.root = root
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QColor(245, 245, 245))  # Fondo claro

        if self.root:
            self._dibujar_nodo(painter, self.root, self.width() // 2, 60, self.width() // 4)

    def _dibujar_nodo(self, painter, nodo, x, y, offset):
        x_izq = x - offset
        x_der = x + offset
        y_siguiente = y + self.nivel_dist

        # Líneas a hijos
        pen = QPen(QColor("#3498db"))
        pen.setWidth(2)
        painter.setPen(pen)

        if nodo.left:
            painter.drawLine(x, y + self.radio, x_izq, y_siguiente - self.radio)
            self._dibujar_nodo(painter, nodo.left, x_izq, y_siguiente, max(20, offset // 2))

        if nodo.right:
            painter.drawLine(x, y + self.radio, x_der, y_siguiente - self.radio)
            self._dibujar_nodo(painter, nodo.right, x_der, y_siguiente, max(20, offset // 2))

        # Nodo actual
        color_fondo = QColor("#2ecc71") if nodo.char else QColor("#9b59b6")
        painter.setBrush(QBrush(color_fondo))
        painter.setPen(QPen(QColor("white"), 2))
        rect = QRectF(x - self.radio, y - self.radio, 2 * self.radio, 2 * self.radio)
        painter.drawEllipse(rect)

        # Texto
        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        if nodo.char:
            painter.drawText(rect, Qt.AlignCenter, f"{nodo.char}")
        else:
            painter.drawText(rect, Qt.AlignCenter, f"{nodo.freq}")


# === VENTANA PRINCIPAL ===
class VentanaHuffman(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧩 Compresor de Texto - Algoritmo de Huffman")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background: #f8f9fa; font-family: 'Arial';")

        # Layout principal
        layout_principal = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)

        # Título
        titulo = QLabel("COMPRESIÓN DE TEXTO CON ÁRBOL DE HUFFMAN")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
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
        desc = QLabel("Codifica texto usando el algoritmo de Huffman y visualiza el árbol generado.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout_principal.addWidget(desc)

        # Panel dividido
        splitter_panel = QFrame()
        splitter_layout = QHBoxLayout(splitter_panel)
        layout_principal.addWidget(splitter_panel)

        # === PANEL IZQUIERDO: ENTRADA Y RESULTADOS ===
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")
        layout_izq = QVBoxLayout(panel_izq)

        # Entrada de texto
        layout_izq.addWidget(QLabel("📝 Texto Original:"))
        self.input_texto = QTextEdit()
        self.input_texto.setPlaceholderText("Escribe o pega el texto que deseas comprimir...")
        self.input_texto.setMaximumHeight(120)
        layout_izq.addWidget(self.input_texto)

        # Botones
        btn_layout = QHBoxLayout()
        btn_codificar = QPushButton("⚙️ Codificar")
        btn_codificar.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_codificar.clicked.connect(self.codificar_texto)

        btn_limpiar = QPushButton("🧹 Limpiar")
        btn_limpiar.setStyleSheet("""
            background-color: #e67e22;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_limpiar.clicked.connect(self.limpiar_todo)

        btn_exportar = QPushButton("📥 Exportar Resultados")
        btn_exportar.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
        """)
        btn_exportar.clicked.connect(self.exportar_resultados)

        btn_layout.addWidget(btn_codificar)
        btn_layout.addWidget(btn_limpiar)
        btn_layout.addWidget(btn_exportar)
        layout_izq.addLayout(btn_layout)

        # Tabla de frecuencias
        tabla_group = QGroupBox("📊 Tabla de Frecuencias")
        tabla_layout = QVBoxLayout()
        self.tabla_frecuencias = QTableWidget()
        self.tabla_frecuencias.setColumnCount(2)
        self.tabla_frecuencias.setHorizontalHeaderLabels(["Carácter", "Frecuencia"])
        self.tabla_frecuencias.horizontalHeader().setStretchLastSection(True)
        tabla_layout.addWidget(self.tabla_frecuencias)
        tabla_group.setLayout(tabla_layout)
        layout_izq.addWidget(tabla_group)

        # Resultados
        resultados_group = QGroupBox("📈 Resultados de Compresión")
        resultados_layout = QVBoxLayout()
        self.area_resultados = QTextEdit()
        self.area_resultados.setReadOnly(True)
        self.area_resultados.setStyleSheet("""
            background: #f8f9fa;
            border: 1px solid #dfe4ea;
            border-radius: 8px;
            font-family: 'Courier New';
            padding: 10px;
        """)
        resultados_layout.addWidget(self.area_resultados)
        resultados_group.setLayout(resultados_layout)
        layout_izq.addWidget(resultados_group)

        # === PANEL DERECHO: VISUALIZACIÓN DEL ÁRBOL ===
        panel_der = QWidget()
        panel_der.setStyleSheet("background: white; border-radius: 10px; padding: 20px;")
        layout_der = QVBoxLayout(panel_der)

        layout_der.addWidget(QLabel("🌳 Árbol de Huffman Generado"))
        self.visualizador = VisualizadorHuffman()
        scroll_canvas = QScrollArea()
        scroll_canvas.setWidgetResizable(True)
        scroll_canvas.setWidget(self.visualizador)
        scroll_canvas.setStyleSheet("background: #f0f0f0; border: none;")
        layout_der.addWidget(scroll_canvas)

        # Añadir paneles
        splitter_layout.addWidget(panel_izq)
        splitter_layout.addWidget(panel_der)
        splitter_layout.setStretch(0, 1)
        splitter_layout.setStretch(1, 1)

        # Variables
        self.huffman = HuffmanCoder()

    def codificar_texto(self):
        texto = self.input_texto.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Vacío", "Por favor ingresa un texto.")
            return

        # Construir árbol
        frecuencias = self.huffman.build_tree(texto)
        if not frecuencias:
            QMessageBox.warning(self, "Error", "No se pudo construir el árbol.")
            return

        # Codificar
        texto_codificado = self.huffman.encode(texto)
        ratio, orig_bits, comp_bits = self.huffman.get_compression_ratio(texto, texto_codificado)

        # Actualizar tabla
        self.tabla_frecuencias.setRowCount(len(frecuencias))
        for i, (char, freq) in enumerate(frecuencias.items()):
            char_str = repr(char) if char in [' ', '\n', '\t'] else char
            self.tabla_frecuencias.setItem(i, 0, QTableWidgetItem(char_str))
            self.tabla_frecuencias.setItem(i, 1, QTableWidgetItem(str(freq)))

        # Resultados
        resultados = f"""
Texto Original: {texto[:100]}{'...' if len(texto) > 100 else ''}
Longitud: {len(texto)} caracteres

Texto Codificado: {texto_codificado[:100]}{'...' if len(texto_codificado) > 100 else ''}
Longitud: {len(texto_codificado)} bits

Tabla de Códigos:
"""
        for char, code in sorted(self.huffman.codes.items()):
            char_str = repr(char) if char in [' ', '\n', '\t'] else char
            resultados += f"  '{char_str}': {code}\n"

        resultados += f"""
Estadísticas:
- Bits originales: {orig_bits}
- Bits comprimidos: {comp_bits}
- Tasa de Compresión: {ratio:.2f}%
"""
        self.area_resultados.setText(resultados)

        # Actualizar visualización
        self.visualizador.set_tree(self.huffman.root)

    def limpiar_todo(self):
        self.input_texto.clear()
        self.tabla_frecuencias.setRowCount(0)
        self.area_resultados.clear()
        self.visualizador.set_tree(None)

    def exportar_resultados(self):
        texto = self.input_texto.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Advertencia", "No hay texto para exportar.")
            return

        nombre_archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Resultados", "huffman_resultados.txt",
            "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        if nombre_archivo:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DE COMPRESIÓN HUFFMAN ===\n")
                f.write(f"Texto original: {texto}\n")
                f.write(f"Longitud: {len(texto)} caracteres\n\n")
                f.write("Tabla de frecuencias:\n")
                frecuencias = {}
                for char in texto:
                    frecuencias[char] = frecuencias.get(char, 0) + 1
                for char, freq in frecuencias.items():
                    char_str = repr(char) if char in [' ', '\n', '\t'] else char
                    f.write(f"  '{char_str}': {freq}\n")
                f.write("\nCódigos Huffman:\n")
                for char, code in sorted(self.huffman.codes.items()):
                    char_str = repr(char) if char in [' ', '\n', '\t'] else char
                    f.write(f"  '{char_str}': {code}\n")
                f.write(f"\nTexto codificado: {self.huffman.encode(texto)}\n")
            QMessageBox.information(self, "Éxito", f"Resultados exportados a:\n{nombre_archivo}")


# === EJECUCIÓN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaHuffman()
    ventana.show()
    sys.exit(app.exec_())