# Lab 5

## 5-1
### Instalación de EMR en AWS
En primer lugar, se crea un Bucket en S3, que servirá como DataLake para este laboratorio. En él, se cargará el dataset dispuesto por el profesor en el [github de la materia]( https://github.com/st0263eafit/st0263-2261/tree/main/bigdata/datasets).

Una vez creado, debe poder verse desde la consola de AWS para S3.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/create_bucket.png)

Luego, es posible copiar el dataset dentro del Bucket. En este caso, se hace en el directorio /raw

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/upload%20dataset.png)

Este Bucket se encuentra disponible publicamente desde el siguiente URL: https://aagutierrldatalake.s3.amazonaws.com/raw
El sistema de archivos tiene el mismo orden de directorios y archivos que el directorio datasets, que provee el github de la materia.

*Nota: Debe especificar el archivo a acceder. Por ejemplo: https://aagutierrldatalake.s3.amazonaws.com/raw/gutenberg-small/AbrahamLincoln___LincolnLetters.txt*

Posteriormente, se procede a crear el Cluster, desde la sección EMR de AWS.

El cLuster debe contar con la siguiente configuración:

- Release: emr-6.3.1
    Instalando lo siguiente:
    - Hadoop
    - JupyterHub
    - Hive
    - Sqoop
    - Zeppelin
    - Tez
    - JupyterEnterpriseGateway
    - Hue
    - Spark
    - Livy
    - HCatalog

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/emr-config1.PNG)

Debido al alcance académico de este laboratorio, así como a limitantes económicas, se utilizarán máquinas m4.xlarge, con un tiempo de vida de 1 hora (sin ser utilizadas), para evitar malgasto de créditos.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/emr-config2.PNG)

Luego, se asigna un par de claves para el acceso ssh a la instancia *master* de EC2.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/emr-config3.PNG)

Una vez terminada la configuración, se oprime *'Create'* y da inicio la  creación del Cluster. Esto tarda aprox. 20 minutos.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/cluster-waiting.png)
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/cluster-ready.png)

Al estar listo, es posible conectarse a la instancia EC2 master.
*Nota: Para contectarse a la instancia, debe abrirse el puerto 22 en el security group al que se asocia el master*

```bash
ssh -i ~/emr_keys.pem ec2-user@ec2-3-83-22-112.compute-1.amazonaws.com
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/ec2-ssh.png)

Desde la terminal, se crea el usuario 'hadoop'.

```bash
sudo su hadoop
```

Una vez dentro, es posible observar los directorios por defecto de HDFS.

```bash
hdfs dfs -ls /
```
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/ls1.png)

Lo instalado al configurar:

```bash
hdfs dfs -ls /user
```
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/ls2.png)

Finalmente, se activa Hue con user 'hadoop'. Para esto, deben abrirse los siguientes puertos en el Security Group:
-8888
-8890
-9443

Y, también, añadirlos a la sección  de Excepciones en ‘Public Access’ de EMR.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/public%20access.png)

Es posible encontrar la URL de acceso a Hue desde la sección *‘Application User Interfaces’* en el cluster activo. Para este caso concreto, fue esta:
http://ec2-3-83-22-112.compute-1.amazonaws.com:8888/

*Nota: Como el Cluster fue eliminado, ese URL no funciona, existe a modo de ejemplo*

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/hue.png)

## 5-2
### Gestión de Archivos en HDFS y S3

Ahora, se realiza el manejo de archivos desde terminal EC2 en HDFS y desde Hue.

En primera instancia, debemos acceder al URL generado para Hue, al que nos conectamos anteriormente. http://ec2-3-83-22-112.compute-1.amazonaws.com:8888/

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/hue.png)

Desde allí, es posible manejar archivos y directorios. Podemos crear un directorio /user/datasets

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/createdir-hue.png)

También, pueden verse los distintos Buckets creados en S3:

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/s3-hue.png)

Al copiar uno de los contenidos de los Buckes, específicamente, el directorio /raw del Bucket ‘aagutierrrldatalake’, es posible observar sus contenidos también desde la terminal de la instancia EC2, a través del comando 

```bash
hdfs dfs -ls /tmp/raw
```
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/tmp-raw.png)

Ahora, por ejemplo, colocamos los contenidos de uno de los directorios en otro. Primero, veamos los contenidos de gutenberg-small

```bash
hdfs dfs -ls /tmp/raw/gutenberg-small
```
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/ls-gutenberg.png)

Ahora, lo movemos al directorio datasets, creado desde Hue

```bash
hdfs dfs -put /tmp/raw/gutenberg-small /user/hadoop/datasets/
```

Probamos que haya funcionado:

```bash
hdfs dfs -ls /user/hadoop/datasets/
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/put-gutenberg.png)

Además, podemos traer archivos desde S3 hasta HDFS, por ejemplo, el archivo airlines.csv

```bash
hadoop distcp s3://aagutierrldatalake/raw/airlines.csv /tmp/
```
![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/traerS3.png)

Verificamos que funcione:

```bash
hdfs dfs -ls /tmp
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/ls-s3.png)

Es posible copiar localmente los archivos. Primero, creamos un directorio llamado 'mis_datasets'

```bash
hdfs dfs -mkdir /hadoop
hdfs dfs -mkdir /hadoop/mis_datasets
```

Entonces, podemos utilizar el comando -copyToLocal y probamos que se haya copiado exitosamente con -ls

```bash
hdfs dfs -copyToLocal /user/hadoop/datasets/Gutenberg-small/ /hadoop/mis_datasets/
hdfs dfs -ls /hadoop/mis_datasets
```

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/copyToLocal.png)

Desde Hue, resulta bastante sencillo e intuitivo copiar y traer datasets a directorios. Por ejemplo, creamos manualmente el directorio datasets, dentro del home.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/datasets-hue.png)

Una vez creado, creamos un nuevo directorio, esta vez, llamado 'ONU', al que se le agregaran archivos del directorio del mismo nombre en los datasets del github de la materia.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/onu-hue.png)

Para cargar el dataset a este nuevo directorio, basta con arrastrarlo desde el explorador de archivos.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/drag-drop-hue.png)

Ahora, podemos ver que, dentro del directorio ONU, se han copiado correctamente los archivos.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/one-content.png)

Como prueba final, podemos ver los contenidos del archivo onu.csv

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/hdfs/onu-csv.png)


## 5-3
### MapReduce con MRJOB en Python

Para poder utilizar la biblioteca MRJOB desde Python localmente, debe ser instalada desde el directorio del proyecto:

```bash
pip install mrjob
```
*Nota: Se asume que ya se cuenta con pip instalado*

Una vez instalada esta biblioteca, se puede empezar a resolver los ejercicios propuestos.

Para todos los puntos, el resultado se da al correr un script con el siguiente comando:

```bash
python <program>.py <dataset>.txt
```
*Donde <program>.py es el script de Python con la solucion y <dataset>.txt el archivo de datos utilizado para el problema*

1) Se tiene un conjunto de datos, que representan el salario anual de los empleados formales en Colombia por sector económico, según la DIAN.

Los datos utilizados para este apartado, se encuentran en el archivo de nombre [dataempleados.txt](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/lab5-3/1.Salarios/dataempleados.txt)

1. El salario promedio por Sector Económico (SE)

Este, fue calculado por medio del script nombrado [dataempleados-mr.py](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/lab5-3/1.Salarios/dataempleados-mr.py)

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/empleados1.png)

2. El salario promedio por Empleado

Este, fue calculado por medio del script nombrado [avgempleado-mr.py](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/lab5-3/1.Salarios/avgempleado-mr.py)

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/empleados2.png)

3. Número de SE por Empleado que ha tenido a lo largo de la estadística

Este, fue calculado por medio del script nombrado [seempleado-mr.py](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/lab5-3/1.Salarios/seempleado-mr.py)

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/empleados3.png)

2) Se tiene un conjunto de acciones de la bolsa, en la cual se reporta a diario el valor promedio por acción.

Los datos utilizados para este apartado, se encuentran en el archivo de nombre [dataempresas.txt]()

1. Por acción, dia-menor-valor, día-mayor-valor

Este, fue calculado por medio del script nombrado [dataempresas-mr1.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/acciones.png)


2. Listado de acciones que siempre han subido o se mantienen estables.

Este, fue calculado por medio del script nombrado [dataempresas-mr2.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/acciones2.png)

3. DIA NEGRO: Saque el día en el que la mayor cantidad de acciones tienen el menor valor de acción (DESPLOME), suponga una inflación independiente del tiempo.

Este, fue calculado por medio del script nombrado [dataempresas-mr2.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/acciones3.png)

3) Sistema de evaluación de películas

Los datos utilizados para este apartado, se encuentran en el archivo de nombre [datapeliculas.txt]()

1. Número de películas vista por un usuario, valor promedio de calificación

Este, fue calculado por medio del script nombrado [datapeliculas-mr1.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis1.png)


2. Día en que más películas se han visto

Este, fue calculado por medio del script nombrado [datapeliculas-mr2.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis2.png)

3. Día en que menos películas se han visto

Este, fue calculado por medio del script nombrado [datapeliculas-mr3.py]()

Y, al correrlo, se obtiene la siguiente solución:

![s3n](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis3.png)


4. Número de usuarios que ven una misma película y el rating promedio

Este, fue calculado por medio del script nombrado [datapeliculas-mr4.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis4.png)


5. Día en que peor evaluación en promedio han dado los usuarios

Este, fue calculado por medio del script nombrado [datapeliculas-mr5.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis5.png)


6. Día en que mejor evaluación han dado los usuarios

Este, fue calculado por medio del script nombrado [datapeliculas-mr6.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis6.png)


7. La mejor y peor película evaluada por genero

Este, fue calculado por medio del script nombrado [datapeliculas-mr7.py]()

Y, al correrlo, se obtiene la siguiente solución:

![sln](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/rmjob/pelis7.png)

