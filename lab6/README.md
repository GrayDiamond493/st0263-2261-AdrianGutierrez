# Lab 6 - Unidad 2 - Big Data

## Wordcount EMR

Para este primer paso, se va a ejecutar un wordcount por linea de comando 'pyspark' INTERACTIVO en EMR con datos en HDFS vía ssh en el nodo master. La configuración del Cluster, Security Group, Buckets, entre otros prerrequisitos, fueron creados en el [laboratorio 5](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/tree/main/lab5). Para ello, necesitaremos el comando pyspark, que ya debe estar instalado por defecto en el nodo mater.

### Desde SSH - Bash

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/spark_welcome.PNG)

```bash
pyspark
>>> files_rdd = sc.textFile("hdfs://user/datasets/gutenberg-small/*.txt")
```

O, con datos del Bucket S3

```bash
>>> files_rdd = sc.textFile("s3a://aagutierrldatalake/raw/gutenberg-small/*.txt")
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/files_rdd.PNG)

Luego, se utilizan las siguientes lineas para guardar las salidas en el HDFS
```bash
>>> wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
>>> wc = wc_unsort.sortBy(lambda a: -a[1])
>>> for tupla in wc.take(10):
>>>     print(tupla)
>>> wc.saveAsTextFile("hdfs:///tmp/wcout1")
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/saveAsTextFile.PNG)

Una vez hecho esto, es posible ver el output en el HDFS, en el directorio /tmp, bajo el nombre de wcout1:

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/success_hdfs.PNG)
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/file_hdfs.PNG)

O, todas las salidas en un mismo archivo, en el directorio wcout2:
```bash
>>> wc.coalesce(1).saveAsTextFile("hdfs:///tmp/wcout2")
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/success_hdfs_singletxt.PNG)
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/file2_hdfs.PNG)

### Desde SSH - Python

Del mismo modo, es posible correr un script de Python para ejecutar todos los pasos anteriores. Este script, se encuentra en este repositorio bajo el nombre [wc-pyspark.py](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/scripts/wc-pyspark.py):

```bash
spark-submit --master yarn --deploy-mode cluster wc-pyspark.py
```

Ello, resulta en

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/from_file_in_progress.PNG)

Luego, debe haberse generado una nueva salida en el directorio tmp, bajo el nombre wcout3:

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/success_hdfs_fromfile.PNG)
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/file_hdfs3.PNG)


## Wordcount Zeppelin

Es posible ingresar a Zeppelin desde una URL mostrada en *'Application user interfaces'* desde EMR en AWS. Para este caso concreto, la URL fue

```bash
http://ec2-3-93-23-84.compute-1.amazonaws.com:8890/
```

*Nota: El puerto 8890 debe estar abierto en el Security Group*

Una vez dentro, puede verse la interfaz de Zeppelin.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/zeppelin/zeppelin.PNG)

En Zeppelin, se crea un notebook. Para este caso, se dio el nombre aagutierrl/labspark

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/zeppelin/labspark.PNG)

*Nota: Es importante escoger Spark como Kernel/Interpreter en el notebook para garantizar su funcionamiento*

En el notebook, copiamos y corremos el siguiente Script,el cual ejecuta exactamente las mismas instrucciones que hemos realizado en HDFS.

```python
    %spark2.pyspark
    # WORDCOUNT COMPACTO
    files_rdd = sc.textFile("s3a://aagutierrl/raw/gutenberg-small/*.txt")
    wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    wc = wc_unsort.sortBy(lambda a: -a[1])
    for tupla in wc.take(10):
        print(tupla)
    wc.coalesce(1).saveAsTextFile("hdfs:///tmp/wcout5")
```

Si todo salio correctamente, puede correrse el script en Zeppelin, resultando en lo siguiente:

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/zeppelin/zeppelin_run.PNG)

## Wordcount Jupyter

A continuación, debemos crear un notebook para ser utilizado en Jupyter.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/jupyter/starting_notebook.PNG)

Al crearlo, es posible abrirlo en JupyterLab. Una vez dentro, es posible importar o copiar el script [wordcount-spark.ipynb](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/scripts/wordcount-spark.ipynb). Este script, realiza exactamente lo mismo que hemos hecho anteriormente en HDFS y Zeppelin, guardando un output en el directorio /tmp. No obstante, este cuenta con un paso a paso de distintas operaciones realizadas a los datos. Estas son:

### Primeras 10 palabras

INPUT
```python
files_rdd = sc.textFile("s3a://aagutierrldatalake/raw/gutenberg-small/*.txt")
#files = sc.textFile("hdfs:///user/hadoop/datasets/gutenberg-small/*.txt")
for f in files_rdd.take(10):
    print(f)
```

OUTPUT
```bash
LINCOLN LETTERS

By Abraham Lincoln


Published by The Bibilophile Society
```

### Primeras 10 palabras (como tokens)

INPUT
```python
tokens = files_rdd.flatMap(lambda line: line.split())
for t in tokens.take(10):
    print(t)
```

OUTPUT
```bash
LINCOLN
LETTERS
By
Abraham
Lincoln
Published
by
The
Bibilophile
Society
```

### Imprimir las 10 palabras, como tuplas 

INPUT
```python
wc1 = tokens.map(lambda word: (word, 1))
for c in wc1.take(10):
    print(c)
```

OUTPUT
```bash
('LINCOLN', 1)
('LETTERS', 1)
('By', 1)
('Abraham', 1)
('Lincoln', 1)
('Published', 1)
('by', 1)
('The', 1)
('Bibilophile', 1)
('Society', 1)
```

### Imprimir 10 palabras, con su numero de apariciones

INPUT
```python
wc = wc1.reduceByKey(lambda a, b: a + b)
for c in wc.take(10):
    print(c)
```

OUTPUT
```bash
('thoroughly', 15)
('themselves', 192)
('them.', 371)
('letter', 312)
('A.', 1456)
('ORIGINALS', 1)
('THEY', 1)
('sum', 59)
('singular', 18)
('let', 414)
```

### Imprimir las palabras que aparecen con mayor frecuencia

INPUT
```python
wcsort = wc.sortBy(lambda a: -a[1])
for c in wcsort.take(10):
    print(c)
```

OUTPUT
```bash
('the', 44647)
('of', 28020)
('to', 23208)
('and', 20444)
('in', 13174)
('that', 12265)
('I', 10880)
('a', 10431)
('is', 7776)
('be', 7148)
```

### Guardar resultado 

```python
#salvar los datos de salida, fijarse que no exista: hdfs:///tmp/<your-username>wcout10
wc.coalesce(1).saveAsTextFile("hdfs:///tmp/wcoutj")
#si esta trabajando en aws (igual verifique que no exista previamente wcout10):
wc.coalesce(1).saveAsTextFile("s3://aagutierrldatalake/wcout")
```
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/jupyter/jupyter_progress.PNG)

Esto, guarda la salida del programa tal y como los anteriores scripts utilizados para este laboratorio.

Podemos ver que, efectivamente, se ha guardado la salida en el HDFS:

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/jupyter/success_jupyter.PNG)

Del mismo modo, en S3:

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/jupyter/jupyter_datalake_success.PNG)
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/jupyter/jupyter_datalake_file.PNG)

## Hive (Tablas, Queries)

## Hive (Wordcount)

## Jupyter SparkSQL