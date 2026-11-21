import csv
import math
import statistics

def leer_diametros(ruta):
    diametros = []
    filas_rotas = []
    with open(ruta, newline='') as f:
        data = csv.DictReader(f)
        if "diametro_mm" in (data.fieldnames or []):
            for row in data:
                try:
                    diametro = float(row["diametro_mm"])
                except (ValueError, TypeError):
                    filas_rotas.append(data.line_num)
                    continue
                if not math.isfinite(diametro):
                    filas_rotas.append(data.line_num)
                else: 
                    diametros.append(diametro)
        else:
            raise ValueError("Falta la columna 'diametro_mm'")
    return diametros, filas_rotas
            


def contar_tolerancias(diametros, nominal, tolerancia):
    dentro = []
    fuera = []
    limite_sup = round(nominal + tolerancia, 4)
    limite_inf = round(nominal - tolerancia, 4)
    for num in diametros:
        if limite_inf <= num <= limite_sup:
            dentro.append(num)
        else:
            fuera.append(num)
    return dentro, fuera


def reportar(dentro, fuera, filas_rotas):
    print("=== INFORME DE DIAMETROS ===")
    if not dentro and not fuera:
        print("NO HAY DATOS QUE MOSTRAR")
        return
    print("DIAMETROS DENTRO DE TOLERANCIA:", len(dentro))
    print("DIAMETROS FUERA DE RANGO:", len(fuera))
    print("MEDIANA GENERAL:", statistics.median(dentro + fuera), "mm")
    if len(dentro) + len(fuera) < 2:
        print("NO ALCANZAN LOS DATOS PARA CALCULAR EL DESVIO POBLACIONAL")
    else:
        print("DESVIO POBLACIONAL: {:.4f} mm".format(statistics.pstdev(dentro + fuera)))
    print("VALORES INVALIDOS:", len(filas_rotas))
    for fila in filas_rotas:
        print("Valor invalido en fila", fila)


def main():
    try: 
        diametros, rotas = leer_diametros("datos.csv")
    except FileNotFoundError:
        print("No se ha podido abrir el archivo. Revise correctamente")
        return
    except ValueError as e:
        print(e)
        return
    dentro, fuera = contar_tolerancias(diametros, nominal=2.00, tolerancia=0.05)
    reportar(dentro, fuera, rotas)

if __name__ == "__main__":
    main()