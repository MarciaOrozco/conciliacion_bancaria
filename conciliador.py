from datetime import date
import csv
import os

print("\nInicio")

# Leer extracto_bancario.csv
print("\nExtracto Bancario:")
extracto_bancario = []
try:
    with open('conciliacion_bancaria/datos/extracto_bancario.csv', 'r') as file:
        next(file)
        for line in file:
            line = line.strip()
            partes = line.split(',')
            if len(partes) != 4:
                print(f"\nError: Existe una línea inválida en extracto_bancario.csv: {line}.")
                continue 
            idcuenta, depositos, importe, fecha = partes
            idcuenta = idcuenta.strip('"')
            depositos = depositos.strip('"')
            fecha = fecha.strip('"')
            try:
                importe = float(importe)
            except ValueError:
                print(f"Error: Importe no numérico en extracto_bancario.csv: {line}.")
                continue
                    
            extracto_bancario.append({
                'idcuenta': idcuenta,
                'depositos': depositos,
                'importe': importe,
                'fecha': fecha
            })
except FileNotFoundError:
    print("\nError: No se encontró el archivo 'extracto_bancario.csv' en la carpeta 'datos/'.\n")
    exit(1)

for registro in extracto_bancario:
    print(registro)

# Leer ventas_sistema.csv
print("\nVentas Sistema:")
ventas_sistema = []
try:
    with open('conciliacion_bancaria/datos/ventas_sistema.csv', 'r') as file:
        next(file)  
        for line in file:
            line = line.strip()
            partes = line.split(',')
            if len(partes) != 3:
                print(f"Error: Existe una línea inválida en ventas_sistema.csv: {line}\n")
                continue
            idcuenta, importe, fecha = partes
            idcuenta = idcuenta.strip('"')
            fecha = fecha.strip('"')
            try:
                importe = float(importe)
            except ValueError:
                print(f"Error: Importe no numérico en ventas_sistema.csv: {line}\n")
                continue

            ventas_sistema.append({
                'idcuenta': idcuenta,
                'importe': importe,
                'fecha': fecha
            })
except FileNotFoundError:
    print("\nError: No se encontró el archivo 'ventas_sistema.csv' en la carpeta 'datos/'.\n")
    exit(1)

for venta in ventas_sistema:
    print(venta)


# Buscar conciliados
conciliados = []
for venta in ventas_sistema:
    for deposito in extracto_bancario:
        if (
            venta['idcuenta'] == deposito['idcuenta'] and
            venta['importe'] == deposito['importe'] and 
            venta['fecha'] == deposito['fecha']
        ):
            conciliados.append({
                'idcuenta': venta['idcuenta'],
                'importe': venta['importe'],
                'fecha': venta['fecha'],
                'deposito': deposito['depositos']
            })
            break  
print("\n=== CONCILIADOS ===")
for c in conciliados:
    print(c)


# Ventas sin depositar
ventas_sin_depositar = []
for venta in ventas_sistema:
    encontrado = False
    for deposito in extracto_bancario:
        if (
            venta['idcuenta'] == deposito['idcuenta'] and
            venta['importe'] == deposito['importe'] and
            venta['fecha'] == deposito['fecha']
        ):
            encontrado = True
            break
    if not encontrado:
        ventas_sin_depositar.append(venta)

print("\n=== VENTAS SIN DEPOSITAR ===")
for v in ventas_sin_depositar:
    print(v)

# Depósitos sin registro
depositos_sin_registro = []
for deposito in extracto_bancario:
    encontrado = False
    for venta in ventas_sistema:
        if (
            venta['idcuenta'] == deposito['idcuenta'] and
            venta['importe'] == deposito['importe'] and
            venta['fecha'] == deposito['fecha']
        ):
            encontrado = True
            break
    if not encontrado:
        depositos_sin_registro.append(deposito)

print("\n=== DEPÓSITOS SIN REGISTRO ===")
for d in depositos_sin_registro:
    print(d)


# Diferencias de importe 
diferencias_importe = []
depositos_disponibles = extracto_bancario.copy() 
for venta in ventas_sistema:
    for deposito in depositos_disponibles:
        if (
            venta['idcuenta'] == deposito['idcuenta'] and
            venta['fecha'] == deposito['fecha']
        ):
            if (venta['importe'] != deposito['importe']):
                diferencias_importe.append({
                    'idcuenta': venta['idcuenta'],
                    'fecha': venta['fecha'],
                    'importe_venta': venta['importe'],
                    'importe_deposito': deposito['importe'],
                    'diferencia': venta['importe'] - deposito['importe']
                })
                depositos_disponibles.remove(deposito)
                break
            else:
                depositos_disponibles.remove(deposito)
                break
print("\n=== DIFERENCIAS DE IMPORTE ===")
for d in diferencias_importe:
    print(d)

# REPORTE FINAL
total_bancarios = len(extracto_bancario)
total_ventas = len(ventas_sistema)
total_conciliados = len(conciliados)
total_ventas_sin_depositar = len(ventas_sin_depositar)
total_depositos_sin_registro = len(depositos_sin_registro)
total_diferencias_importe = len(diferencias_importe)

porcentaje_conciliados = (total_conciliados / total_ventas) * 100 if total_ventas > 0 else 0

print("\n=== REPORTE DE CONCILIACIÓN BANCARIA ===")
print(f"Fecha: {date.today()}")
print(f"Registros bancarios: {total_bancarios}")
print(f"Registros de ventas: {total_ventas}")

print("\nRESULTADOS:")
print(f"✅ Conciliados: {total_conciliados} ({porcentaje_conciliados:.1f}%)")
print(f"⚠️  Ventas sin depositar: {total_ventas_sin_depositar}")
print(f"❌ Depósitos sin registrar: {total_depositos_sin_registro}")
print(f"💰 Diferencias de importe: {total_diferencias_importe}")

# Resumen por cuenta
print("\nRESUMEN POR CUENTA:")

lista_cuentas = []

for v in ventas_sistema:
    cuenta = v['idcuenta']
    if cuenta not in lista_cuentas:
        lista_cuentas.append(cuenta)

for d in extracto_bancario:
    cuenta = d['idcuenta']
    if cuenta not in lista_cuentas:
        lista_cuentas.append(cuenta)

for cuenta in lista_cuentas:
    conciliados_cuenta = []
    ventas_cuenta = []

    for c in conciliados:
        if c['idcuenta'] == cuenta:
            conciliados_cuenta.append(c)

    for v in ventas_sistema:
        if v['idcuenta'] == cuenta:
            ventas_cuenta.append(v)

    if len(ventas_cuenta) > 0:
        porcentaje = (len(conciliados_cuenta) / len(ventas_cuenta)) * 100
    else:
        porcentaje = 0
    print(cuenta + ": " + str(round(porcentaje)) + "% conciliado")


os.makedirs('conciliacion_bancaria/resultados', exist_ok=True)

with open('conciliacion_bancaria/resultados/conciliados.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['idcuenta', 'importe', 'fecha', 'deposito'])
    writer.writeheader()
    for row in conciliados:
        writer.writerow(row)

with open('conciliacion_bancaria/resultados/ventas_sin_depositar.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['idcuenta', 'importe', 'fecha'])
    writer.writeheader()
    for row in ventas_sin_depositar:
        writer.writerow(row)

with open('conciliacion_bancaria/resultados/depositos_sin_registro.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['idcuenta', 'depositos', 'importe', 'fecha'])
    writer.writeheader()
    for row in depositos_sin_registro:
        writer.writerow(row)

with open('conciliacion_bancaria/resultados/diferencias_importe.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['idcuenta', 'fecha', 'importe_venta', 'importe_deposito', 'diferencia'])
    writer.writeheader()
    for row in diferencias_importe:
        writer.writerow(row)

print("\nArchivos CSV generados en la carpeta 'resultados/'.")
