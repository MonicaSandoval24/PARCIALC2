
import sys
import pandas as pd
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# Leer los datos del inventario
datos = pd.read_csv("datos.csv")

# Calcular el valor total de cada producto
datos["valor_total"] = datos["precio"] * datos["cantidad"]


# Analizar la informacion
print("PRIMEROS REGISTROS")
print(datos.head())

print("\nDIMENSIONES DEL INVENTARIO")
print(datos.shape)

print("\nINFORMACION DE LOS DATOS")
datos.info()

print("\nESTADISTICAS")
print(datos.describe())

print("\nUNIDADES POR SUCURSAL")
print(datos.groupby("sucursal")["cantidad"].sum())

print("\nVALOR POR SUCURSAL")
print(datos.groupby("sucursal")["valor_total"].sum())


# Crear la ventana de la aplicacion
class VentanaInventario(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Inventario")
        self.resize(1000, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        titulo = QLabel("ANALISIS DEL INVENTARIO POR SUCURSAL")
        titulo.setStyleSheet(
            "font-size: 18px; font-weight: bold; padding: 10px;"
        )
        layout.addWidget(titulo)

        # Crear los espacios para los graficos
        figura, self.ejes = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvas(figura)

        layout.addWidget(self.canvas)

        self.mostrar_graficos()

    def mostrar_graficos(self):

        # Grafico de unidades por sucursal
        unidades = datos.groupby("sucursal")["cantidad"].sum()

        unidades.plot(
            kind="bar",
            ax=self.ejes[0],
            color="steelblue"
        )

        self.ejes[0].set_title("Unidades disponibles")
        self.ejes[0].set_xlabel("Sucursal")
        self.ejes[0].set_ylabel("Cantidad")
        self.ejes[0].tick_params(axis="x", rotation=35)

        # Grafico del valor del inventario
        valores = datos.groupby("sucursal")["valor_total"].sum()

        valores.plot(
            kind="bar",
            ax=self.ejes[1],
            color="seagreen"
        )

        self.ejes[1].set_title("Valor del inventario")
        self.ejes[1].set_xlabel("Sucursal")
        self.ejes[1].set_ylabel("Valor en dolares")
        self.ejes[1].tick_params(axis="x", rotation=35)

        self.canvas.figure.tight_layout()
        self.canvas.draw()


# Ejecutar la aplicacion
app = QApplication(sys.argv)

ventana = VentanaInventario()
ventana.show()

sys.exit(app.exec_())
