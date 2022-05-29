# Lab 6 - Unidad 2 - Big Data

## Wordcount EMR

Para este primer paso, se va a ejecutar un wordcount por linea de comando 'pyspark' INTERACTIVO en EMR con datos en HDFS vía ssh en el nodo master. La configuración del Cluster, Security Group, Buckets, entre otros prerrequisitos, fueron creados en el [laboratorio 5](). Para ello, necesitaremos el comando pyspark, que ya debe estar instalado por defecto en el nodo mater.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab6/img/spark-hdfs/spark_welcome.PNG)

```bash
pyspark
>>> files_rdd = sc.textFile("hdfs://user/datasets/gutenberg-small/*.txt")
```

O, con datos del Bucket S3

```bash
>>> files_rdd = sc.textFile("s3a://aagutierrldatalake/raw/gutenberg-small/*.txt")
```

![image]()

Luego, se utilizan las siguientes lineas para guardar las salidas en el HDFS
```bash
>>> wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
>>> wc = wc_unsort.sortBy(lambda a: -a[1])
>>> for tupla in wc.take(10):
>>>     print(tupla)
>>> wc.saveAsTextFile("hdfs:///tmp/wcout1")
```

Una vez hecho esto, es posible ver el output en el HDFS, en el directorio /tmp, bajo el nombre de wcout1:

O, todas las salidas en un mismo archivo, en el directorio wcout2:
```bash
>>> wc.coalesce(1).saveAsTextFile("hdfs:///tmp/wcout2")
```

Del mismo modo, es posible correr un script de Python para ejecutar todos los pasos anteriores. Este script, se encuentra en este repositorio bajo el nombre [wc-pyspark.py]():

```bash
spark-submit --master yarn --deploy-mode cluster wc-pyspark.py
```

Ello, resulta en

## Wordcount Zeppelin

## Wordcount Jupyter

## Hive (Tablas, Queries)

## Hive (Wordcount)

## Jupyter SparkSQL