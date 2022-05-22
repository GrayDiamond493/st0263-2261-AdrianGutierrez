# Lab 5

## 5-1
### Instalación de EMR en AWS
En primer lugar, se crea un Bucket en S3, que servirá como DataLake para este laboratorio. En él, se cargará el dataset dispuesto por el profesor en el [github de la materia]( https://github.com/st0263eafit/st0263-2261/tree/main/bigdata/datasets).

Una vez creado, debe poder verse desde la consola de AWS para S3.

![image](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/lab5/images/emr/create_bucket.png)

Luego, es posible copiar el dataset dentro del Bucket. En este caso, se hace en el directorio /raw

![image]()

Posteriormente, se procede a crear el Cluster, desde la sección EMR de AWS.

![image]()

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

![image]()

Debido al alcance académico de este laboratorio, así como a limitantes económicas, se utilizarán máquinas m4.xlarge, con un tiempo de vida de 1 hora (sin ser utilizadas), para evitar malgasto de créditos.

![image]()

Luego, se asigna un par de claves para el acceso ssh a la instancia *master* de EC2.

![image]()

Una vez terminada la configuración, se oprime *'Create'* y da inicio la  creación del Cluster. Esto tarda aprox. 20 minutos.

![image]()

Al estar listo, es posible conectarse a la instancia EC2 master.
*Nota: Para contectarse a la instancia, debe abrirse el puerto 22 en el security group al que se asocia el master*

```bash
ssh -i ~/emr_keys.pem ec2-user@ec2-3-83-22-112.compute-1.amazonaws.com
```

![image]()

Desde la terminal, se crea el usuario 'hadoop'.

```bash
sudo su hadoop
```

Una vez dentro, es posible observar los directorios por defecto de HDFS.

```bash
hdfs dfs -ls /
```
![image]()

Lo instalado al configurar:

```bash
hdfs dfs -ls /user
```
![image]()

Finalmente, se activa Hue con user 'hadoop'. Para esto, deben abrirse los siguientes puertos en el Security Group:
-8888
-8890
-9443

Y, también, añadirlos a la sección  de Excepciones en ‘Public Access’ de EMR.

Es posible encontrar la URL de acceso a Hue desde la sección *‘Application User Interfaces’* en el cluster activo. Para este caso concreto, fue esta:
http://ec2-3-83-22-112.compute-1.amazonaws.com:8888/

*Nota: Como el Cluster fue eliminado, ese URL no funciona, existe a modo de ejemplo*

![image]()

## 5-2
### Gestión de Archivos en HDFS y S3

## 5-3
### MapReduce con MRJOB en Python
