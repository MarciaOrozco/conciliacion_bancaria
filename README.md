# conciliacion_bancaria

Sistema en Python para realizar **conciliaciones bancarias** comparando los depósitos registrados en el extracto bancario con las ventas registradas en el sistema interno de la empresa.

## Funcionalidades

- Carga y validación de datos desde archivos CSV.
- Conciliación de registros.
- Detecta ventas sin depósitos correspondientes.
- Detecta depósitos sin ventas correspondientes.
- Encuentra diferencias de importe en registros de misma fecha y cuenta.
- Genera reportes.

## Estructura del Proyecto

conciliacion_bancaria/
├── datos/
│ ├── extracto_bancario.csv
│ └── ventas_sistema.csv
├── resultados/
│ ├── conciliados.csv
│ ├── ventas_sin_depositar.csv
│ ├── depositos_sin_registro.csv
│ └── diferencias_importe.csv
├── conciliador.py
└── README.md

## Notas importantes para los archivos de entrada(datos/):

- La fecha debe estar en formato YYYY-MM-DD.
- Los montos deben ser numéricos.
- El sistema valida errores en las líneas.

## Reportes generados (carpeta `resultados/`)

- conciliados.csv: Registros de ventas y depósitos que coinciden.
- ventas_sin_depositar.csv: Ventas que no tienen depósito correspondiente.
- depositos_sin_registro.csv: Depósitos que no tienen venta correspondiente.
- diferencias_importe.csv: Registros de misma cuenta/fecha con montos diferentes.

## Cómo usar el sistema

1. Colocar los archivos `extracto_bancario.csv` y `ventas_sistema.csv` en la carpeta `datos/`.
2. Ejecutar el programa desde la terminal: python3 conciliador.py
3. Revisar el reporte en consola y los archivos generados en la carpeta resultados/.
