from calidad import contar_tolerancias, leer_diametros, reportar
import pytest

def test_contar_caso_general():
    dentro, fuera = contar_tolerancias([1.95, 2.0, 2.06], 2.0, 0.05)
    assert dentro == [1.95, 2.0]
    assert fuera == [2.06]

def test_contar_borde_superior_es_valido():
    dentro, fuera = contar_tolerancias([2.05], 2.0, 0.05)
    assert dentro == [2.05]
    assert fuera == []

def test_contar_borde_inferior_es_valido():
    dentro, fuera = contar_tolerancias([1.95], 2.0, 0.05)
    assert dentro == [1.95]
    assert fuera == []

def test_contar_borde_superior_no_es_valido():
    dentro, fuera = contar_tolerancias([2.0501], 2.0, 0.05)
    assert dentro == []
    assert fuera == [2.0501]

def test_contar_borde_inferior_no_es_valido():
    dentro, fuera = contar_tolerancias([1.9499], 2.0, 0.05)
    assert dentro == []
    assert fuera == [1.9499]

def test_contar_borde_superior_con_nominal_2_1():
    dentro, fuera = contar_tolerancias([2.15], 2.1, 0.05)
    assert dentro == [2.15]
    assert fuera == []

def test_contar_borde_inferior_con_nominal_2_1():
    dentro, fuera = contar_tolerancias([2.05], 2.1, 0.05)
    assert dentro == [2.05]
    assert fuera == []

def test_contar_vacio():
    dentro, fuera = contar_tolerancias([], 2.0, 0.05)
    assert dentro == []
    assert fuera == []

def test_leer_columna_faltante(tmp_path):
    archivo = tmp_path / "prueba.csv"
    archivo.write_text("muestra_id,otra\n1,2.0\n")
    with pytest.raises(ValueError):
        leer_diametros(archivo)

def test_leer_caso_general(tmp_path):
    archivo = tmp_path / "prueba.csv"
    archivo.write_text("muestra_id,diametro_mm\n1,2.00\n2,abc\n3,nan\n4,1.99\n5,inf\n6,2.00\n7\n")
    diametros, rotas = leer_diametros(archivo)
    assert diametros == [2.0, 1.99, 2.0]
    assert rotas == [3, 4, 6, 8]

def test_leer_celda_vacia(tmp_path):
    archivo = tmp_path / "prueba.csv"
    archivo.write_text("muestra_id,diametro_mm\n1\n")
    diametros, rotas = leer_diametros(archivo)
    assert diametros == []
    assert rotas == [2]

def test_leer_sin_archivo(tmp_path):
    archivo = tmp_path / "no_existe.csv"
    with pytest.raises(FileNotFoundError):
        leer_diametros(archivo)

def test_leer_archivo_vacio_lanza_error(tmp_path):
    archivo = tmp_path / "prueba.csv"
    archivo.write_text("")
    with pytest.raises(ValueError):
        leer_diametros(archivo)

def test_leer_solo_encabezado(tmp_path):
    archivo = tmp_path / "prueba.csv"
    archivo.write_text("muestra_id,diametro_mm\n")
    diametros, rotas = leer_diametros(archivo)
    assert diametros == []
    assert rotas == []

def test_reportar_sin_datos(capsys):
    reportar([], [], [])
    salida = capsys.readouterr().out
    assert "NO HAY DATOS QUE MOSTRAR" in salida

def test_reportar_caso_general(capsys):
    reportar([2.0, 1.97], [2.1], [])
    salida = capsys.readouterr().out
    assert "DIAMETROS DENTRO DE TOLERANCIA: 2" in salida
    assert "DIAMETROS FUERA DE RANGO: 1" in salida
    assert "MEDIANA GENERAL: 2.0" in salida

def test_reportar_unico_dato(capsys):
    reportar([2.0], [], [])
    salida = capsys.readouterr().out
    assert "DIAMETROS DENTRO DE TOLERANCIA: 1" in salida
    assert "NO ALCANZAN LOS DATOS PARA CALCULAR EL DESVIO POBLACIONAL" in salida

def test_reportar_filas_rotas(capsys):
    reportar([2.0, 2.01], [], [3, 6])
    salida = capsys.readouterr().out
    assert "DIAMETROS DENTRO DE TOLERANCIA: 2" in salida
    assert "VALORES INVALIDOS: 2" in salida
    assert "Valor invalido en fila 3" in salida
    assert "Valor invalido en fila 6" in salida

def test_reportar_solo_rotos(capsys):
    reportar([], [], [3])
    salida = capsys.readouterr().out
    assert "NO HAY DATOS QUE MOSTRAR" in salida