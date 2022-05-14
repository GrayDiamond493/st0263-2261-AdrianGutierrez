# Despliegue AWS

Para este proyecto, se pretende desplegar una aplicación open source LAMP de comunidad que represente un sistema de información del tipo Sistema de Gestión de Aprendizaje (LMS, por sus siglas en inglés). En este caso se seleccionará Moodle para ser desplegado en AWS.

El objetivo de este proyecto es migrarlo al dominio *moodletelematica.tk*.

## Prerequisitos

## Arquitectura

Para alcanzar un modelo de altamente escalable, con alta disponibilidad y rendimiento, se planteó la siguiente arquitectura:

![Arquitectura](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/AWS/Images/moodlearch2.jpg) 

*Recuperado de: https://aws.amazon.com/es/blogs/aws-spanish/despliegue-de-moodle-en-alta-disponibilidad-en-aws/*

## Configuración


![image](https://user-images.githubusercontent.com/71454879/168447398-ba313f6a-ab0a-4091-a307-f09c92846e3f.png)
Base de datos MariaDB creada usando el servicio de RDS de AWS, todas las maquinas de Moodle se conectaran a esta mediante el siguiente punto de montaje:
![image](https://user-images.githubusercontent.com/71454879/168447426-91957ebb-1244-4030-a6e7-aabd9fd0b9e2.png)
Ese punto de enlace irá en el archivo Docker-compose.yml; además debemos asegurarnos de que tenga abierto el puerto 3306. 

Además de esto todas las maquinas compartirán un sistema de archivos, el cual fue creado el servicio de EFS brindado por AWS, quedando de la siguiente manera:
![image](https://user-images.githubusercontent.com/71454879/168447449-bf4fc2b1-dd4c-42f0-b2a0-8b7ce9dba63e.png)

![image](https://user-images.githubusercontent.com/71454879/168447476-b7ae1e0c-42d8-4f04-b553-f8bedfc0a5bd.png)
Al entrar en el EFS que hemos creado, usamos el boton de asociar para obtener el script necesario para asociar el EFS con la máquina en cuestión, en este caso
se hará mediante Ip:
![image](https://user-images.githubusercontent.com/71454879/168447491-38f552c5-2aa1-4f5e-95dd-deb0381652ea.png)


![image](https://user-images.githubusercontent.com/71454879/168447301-2bde6766-11b2-4041-b299-8d9d45ce893a.png)
Imagen AMI de la maquina con todo configurado pero con Ip pública, se usará para crear las maquinas sin ip pública ya que estás no tienen acceso a internet.

![image](https://user-images.githubusercontent.com/71454879/168447690-3ee062bf-0470-4be6-9893-47ebe085a0a5.png)
Dado que tendremos multiples máquinas para el Auto-scaling sin dirección ip pública, se hace necesaria la creación de una máquina Bastion Host para acceder a estas,
está maquina no tiene ninguna particularidad en su creación salvo que solo tendrá habilitado el puerto 22. 

![image](https://user-images.githubusercontent.com/71454879/168447545-9df2316c-70cc-4dd3-89e4-f6a6bc529826.png)
Ya que las máquinas que contienen el Moodle no tienen conexión a internet, tenemos que conectarnos desde el Bastion Host, para esto tenemos que enviarle nuestro 
archivo de claves .pem y usar el script de conexión mediante SSH que nos proporciona la máquina sin ip, el cual usa su dirección privada. 

![image](https://user-images.githubusercontent.com/71454879/168447810-34d20a17-2d29-4883-9fd3-52e6f7a3a767.png)
Posterior a la instalación de docker y todo lo necesario en la máquina, se crea una carpeta llamada moodle y dentro de esta creamos usando nano o vim, un archivo
docker-compose.yml con los siguientes contenidos:
![image](https://user-images.githubusercontent.com/71454879/168447768-4d815008-9d11-4afb-85ce-ba4289e45d22.png)
En MOODLE_DATABASE_HOST colocamos el punto de enlace de nuestra base de datos, en MOODLE_DATABASE_USER y MOODLE_DATABASE_PASSWORD serán las credenciales que definimos
cuando estabamos creando la base de datos. 

Ahora se creará el grupo de destino, con miras a comenzar con el auto-scaling.
Dentro del apartado EC2 de AWS nos iremos a la categoria de equilibrio de carga y después a Grupos de Destino:
![image](https://user-images.githubusercontent.com/71454879/168447994-f73dba0b-82c6-452c-a540-1148f6fd20f8.png)
Aqui dentro crearemos el grupo de destino con la siguiente configuración:
● Choose a target type: Instances.
● Target group name: TG-MyWebApp.
● Protocol: HTTP:80
● VPC: VPC-default
● Protocol version: HTTP1

En el siguiente paso podremos seleccionar que instancias deseamos para el grupo de destino, sin embargo no seleccionaremos ninguna ni haremos ninguna configuración aqui, por lo que daremos directamente en Create Target Group.
![image](https://user-images.githubusercontent.com/71454879/168448162-2008fffd-3ef7-409b-886d-2c14ac88034e.png)

Ahora crearemos nuestro balanceador de carga, para esto dentro del apartado de EC2, en la misma categoria de equilibrio de carga, iremos a balanceadores de carga:
![image](https://user-images.githubusercontent.com/71454879/168448201-8b485828-34e2-4d1c-96ed-c098ee66dc1b.png)

Dentro de esto haremos click en Crear balanceador de carga:
![image](https://user-images.githubusercontent.com/71454879/168448218-29c372b3-d801-499f-9dee-4c9b5b9c3715.png)

![image](https://user-images.githubusercontent.com/71454879/168448228-8bc2d135-c161-47dc-a99b-bd876c00c194.png)
Podemos ver que tenemos tres tipos distintos, en este caso usaremos Application Load Balancer.

En el apartado de configuración que veremos usaremos los siguientes parametros:
● En la sección de configuración básica:
  - Name: ELB-MyWebApp
  - Scheme: Seleccione internet-facing.
  - IP address type: ipv4
  - VPC: VPC-default.
● En la sección de Listeners:
  - Load Balancer Protocol: http.
  - Load Balancer Port: 80.
  - Default action: seleccionamos el grupo de destino creado anteriormente: TG-MyWebApp
● En la sección de Network mapping:
  - VPC: VPC-default
  - Availability Zones: Seleccionamos la casilla todas las zonas de disponibilidad.
● En la sección de Security Settings no haremos nada y pasaremos a los Security Groups
● En la sección de Configure Security Group, seleccionamos la opción de escoger un security group
existente, aqui escogeremos el grupo de SG-Web.

Si todo salió bien veremos la siguiente pantalla:
![image](https://user-images.githubusercontent.com/71454879/168448578-0da7ecf8-b0a5-4811-a228-b710ce53d9dd.png)

Ahora coniguraremos el Launch Template y el grupo de Auto-Scaling, comenzaremos por el Launch Template, esta será la plantilla que se usará para crear todas las maquinas del grupo de Auto-Scaling.
Dentro del apartado de EC2 en la categoria de instancias seleecionamos Plantillas de lanzamiento:
![image](https://user-images.githubusercontent.com/71454879/168448640-f339786a-6018-4aa1-9207-2bd80bb42388.png)

Esta vez lo haremos con las siguientes configuraciones:
▪ Launch configuration name: MyWebApp
▪ Template version description: Template for web moodle.
▪ Auto Scaling guidance: Activamos la casilla.

Ahora en Launch template contents
▪ Application and OS Images (Amazon Machine Image): En myAMIs, click en
Owned by me, aqui seleccionamos nuestra AMI creada anteriormente para esto.
▪ Instance type: t2.micro
▪ Key pair: Aqui seleccionamos nuestras claves de acceso para las instancias EC2.

Todo lo demás queda por defecto y podemos crear nuestra plantilla:
![image](https://user-images.githubusercontent.com/71454879/168448748-47b5197d-2cfc-4466-8ff6-ffaaa28ac6b8.png)

Ahora crearemos el grupo de Auto-Scaling, para esto podemos usar el vinculo que nos brindó la pantalla anterior. 
En el primer paso tendremos esta configuración:
![image](https://user-images.githubusercontent.com/71454879/168448790-1d961b57-6940-4428-9c9d-0a0f4c2fca5a.png)
Vamos a siguiente, en red tendremos estas configuraciones y pasamos al siguiente:
![image](https://user-images.githubusercontent.com/71454879/168448817-202e2d2c-26ed-4243-a014-4d56169078c6.png)
 Aqui en opciones avanzadas tendremos esto:
 ![image](https://user-images.githubusercontent.com/71454879/168448861-c79e4c03-e06f-4d08-a37c-0fea166a198a.png)
![image](https://user-images.githubusercontent.com/71454879/168448862-dfadd62b-1c04-45c1-8f08-54c8f210e20d.png)
Vamos a siguiente, donde tendremos lo siguiente:
![image](https://user-images.githubusercontent.com/71454879/168448897-8e1fa1b7-0692-4e3c-adf5-e375e2b028d0.png)
En el apartado Añadir notificación no haremos nada, siguiente:
![image](https://user-images.githubusercontent.com/71454879/168448937-4d50ea17-75cc-4877-ad42-868bbd79ad84.png)
Para finalizar, en crear etiqueta tendremos lo siguiente:
![image](https://user-images.githubusercontent.com/71454879/168448960-e71cae04-9880-4761-afdf-aad54ddcebb1.png)

Si todo salió bien veremos esto:
![image](https://user-images.githubusercontent.com/71454879/168448988-1ebca9df-3406-4132-a6e6-8662c23eba90.png)



### Confirmación

Una vez llegado a este punto, puede probarse que funciona correctamente al digitar el dominio en cualquier browser
- *moodletelematica.tk*

Debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/moodleScreen.PNG)
