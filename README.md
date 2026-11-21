# Control de diámetros con csv simple

Lee un CSV de mediciones, cuenta cuáles caen dentro y fuera de tolerancia,
muestra la mediana y el desvío poblacional. También informa que filas del CSV
no se pudieron leer.

## Como usarlo

```bash
git clone https://github.com/klonaush/control-diametros.git
cd control-diametros
python -m venv venv
```

Activar el entorno virtual:

- **Windows:** `venv\Scripts\activate`
- **Linux/Mac:** `source venv/bin/activate`

```bash
pip install -r requirements.txt
python calidad.py
```

(En algunos sistemas el comando es `python3`.)

El programa lee `datos.csv`, que debe estar en la misma carpeta. El
nominal (2.00 mm) y la tolerancia (±0.05 mm) están fijos en `main`,
dentro de `calidad.py`.

## Ejemplo de salida

```text
=== INFORME DE DIAMETROS ===
DIAMETROS DENTRO DE TOLERANCIA: 35
DIAMETROS FUERA DE RANGO: 3
MEDIANA GENERAL: 2.0 mm
DESVIO POBLACIONAL: 0.0313 mm
VALORES INVALIDOS: 2
Valor invalido en fila 24
Valor invalido en fila 32
```

## Formato del CSV

Debe tener una columna llamada exactamente `diametro_mm`; otras
columnas se ignoran. Los decimales van con punto. Los datos del
ejemplo son inventados.

```csv
muestra_id,diametro_mm
1,2.01
2,1.98
3,abc
```

Si falta la columna o el archivo está vacío, el programa avisa y termina.

## Decisiones de diseño

- **Borde inclusivo:** Una medición igual al límite se considera dentro de tolerancia. Es decir; 2.05 cae dentro de tolerancia si 2.05 es su límite. Se considera borde inclusivo teniendo en cuenta este detalle.
- **Medición sin redondear, límites sí:** Los límites (`nominal ± tolerancia`)
  se redondean a 4 decimales porque los floats se guardan en binario y
  la suma puede dejar basura en el último decimal. Un test con nominal
  2.1 y tolerancia 0.05 falló al quitar el redondeo: un borde exacto
  quedaba afuera. La medición se compara tal cual: redondearla haría
  pasar como válida una pieza como 2.0504.
- **Desvío poblacional vs. muestral:** Se usa `pstdev` suponiendo que el CSV contiene el lote completo medido, no una muestra de un proceso mayor. Si fuera una muestra, correspondería `stdev`.
- **Mediana en vez de media:** Se muestra la mediana porque no la distorsionan valores extremos. Limitación: puede ocultar piezas muy fuera de tolerancia, por eso se informa aparte el conteo de fuera de rango.
- **Filas inválidas**: Se toman como filas inválidas aquellas que contengan un diámetro vacío, un diámetro "nan", un diámetro infinito y un diámetro compuesto de letras. Se saltean, se informa su número de línea y no entran en la mediana ni en el desvío.

## Limitaciones conocidas

- Si no hay ninguna medición válida, el informe muestra "NO HAY DATOS QUE
  MOSTRAR" y no lista las filas inválidas.

## Tests

```bash
pytest -v
```
