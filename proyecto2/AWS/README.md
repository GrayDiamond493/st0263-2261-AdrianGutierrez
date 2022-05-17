# Despliegue AWS

Para este proyecto, se pretende desplegar una aplicación open source LAMP de comunidad que represente un sistema de información del tipo Sistema de Gestión de Aprendizaje (LMS, por sus siglas en inglés). En este caso se seleccionará Moodle para ser desplegado en AWS.

El objetivo de este proyecto es migrarlo al dominio *moodletelematica.tk*.

## Prerequisitos

## Arquitectura

Para alcanzar un modelo de altamente escalable, con alta disponibilidad y rendimiento, se plantea la siguiente arquitectura de referencia:

![Arquitectura](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/AWS/Images/moodlearch2.jpg) 

*Recuperado de: https://aws.amazon.com/es/blogs/aws-spanish/despliegue-de-moodle-en-alta-disponibilidad-en-aws/*

No obstante, la arquitectura final utilizada es la siguiente, la cual consiste en una variante que toma como base la referencia anterior:

![Arquitectura](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/AWS/Images/ArquitecturaAWS.PNG)

## Configuración

### Security Groups

Se debe escoger la opción “create security group” y configurar los siguientes parámetros:
- Security group name: SG-Web
- Description: Enable HTTP Access
- VPC: VPC-default

Una vez esté creado, deben agregarse las reglas de tráfico de entrada a este. En la pestaña de “Inbound rules”, con los siguientes parámetros:

*Para permitir tráfico desde un browser*
- Type: HTTP
- Source: Anywhere
- Description: Permit Web Requests

*Para permitir conexión remota a máquinas por medio de ssh*
- Type: SSH
- Source: Anywhere
- Description: Permit SSH Requests

*Para permitir la conexión con el sistema de archivos*
- Type: NFS
- Source: Anywhere 
- Description: Permit NFS Requests for EFS

### Security Groups (Base de Datos)

Se debe escoger la opción “create security group” y configurar los siguientes parámetros:
- Security group name: SG-RDS-DB
- Description: Permit Access from web security group.
- VPC: VPC-default

Una vez esté creado, deben agregarse las reglas de tráfico de entrada a este. En la pestaña de “Inbound rules”, con los siguientes parámetros:

*Para permitir conexión a bases de datos*
- Type: MySQL/Aurora
- Source: Custom
- Description: Allow DB connection

### Sistema de Archivos

Todas las máquinas compartirán un sistema de archivos. Para ello,  fue creado el servicio de EFS brindado por AWS.  Este sistema de archivos permite compartir todos los archivos de la aplicación moodle así como todos los archivos estáticos que normalmente maneja un servidor CMS (imágenes, pdfs, videos, sonidos, y en general muchos otros tipos de archivos. Para esto, en la consola de administración de AWS, se escoge el servicio de EFS.

Se debe escoger la opción “Create File System” y configurar los siguientes parámetros:
- Name - optional: Moodle-EFS
- Virtual Private Cloud: (VPC): VPC-default
- Availability and Durability: Regional

Al crearse, debe accederse al mismo y actualizar el Security Group.

Una vez creado, puede verse desde la consola de AWS:
![image](https://user-images.githubusercontent.com/71454879/168447449-bf4fc2b1-dd4c-42f0-b2a0-8b7ce9dba63e.png)

Al entrar en el EFS que hemos creado, usamos el boton de asociar para obtener el script necesario para asociar el EFS con la máquina en cuestión, en este caso
se hará un montaje mediante IP:
![image](https://user-images.githubusercontent.com/71454879/168447491-38f552c5-2aa1-4f5e-95dd-deb0381652ea.png)

De ahí, debe conservarse el comando de conexión. Para nuestro caso concreto, fue el siguiente:
```bash 
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 172.31.7.47:/ efs
```

### Base de Datos

En esta sección se procederá a desplegar una instancia de bases de datos de MySQL en un entorno de múltiples zonas de disponibilidad. Cuando se lanza este servicio, de manera automática Amazon crea una instancia principal de la base de datos y sincroniza los datos con una estancia secundaria que despliega en una zona de disponibilidad diferente en la cual desplegó la primera instancia.

En la consola de gestión, seleccione el servicio de RDS para crear una base de datos con los siguientes parámetros:

*Estos parámetros dependen de cada caso particular*
- DB instance identifier: exampledb
- Master username: (El mismo del Moodle en Docker)
- Master password: (El mismo del Moodle en Docker)

- En la sección de DB instance size:
  - DB instance class: seleccione burstable classes (includes t classes).
  - Seleccione db.t2.micro.
- En la sección Storage, configure:
  - Storage type: General purpose (SSD).
  - Allocated storage: 20
- En la sección de Availability y durability:
  - Multi-AZ deployment. Seleccione a standby instance (recommender for production
usage).
- En la sección de Connectivity
  - Virtual Private Cloud: (VPC): VPC-default.
  - Expanda la opción para Additional connectivity configuration:
- Selecciona las zonas de disponibilidad y subredes para el despliegue de la base de
datos. Recuerde que esta va ubicada en la subred privada.
  - Public access: Click en No.
  - Existing VPC security groups: Seleccione el security group definido para la BD.
- En la sección de Database authentication:
  - Seleccione Password authentication.
- Expanda la opción para Additional configuration:
  - Initial database name: moodle.
  - No marque la opción de “enable automatic backups”
  - No marque la opción de “enable enhanced monitoring

Al crearse, debe poder verse desde la consola:
![image](https://user-images.githubusercontent.com/71454879/168447398-ba313f6a-ab0a-4091-a307-f09c92846e3f.png)
De esta manera, todas las maquinas de Moodle se conectaran a esta mediante el siguiente punto de montaje:
- Punto de enlace: database-1.c4dkqd8k6b30.us-east-1.red.amazonaws.com
- Puerto: 3306

Ese punto de enlace debe ser especificado en el archivo [docker-compose.yml](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/AWS/Scripts/docker-compose.yml). Además, debemos asegurarnos de que tenga abierto el puerto 3306. 

### Lanzar EC2 - Bastion Host

En esta sección crearemos una instancia EC2 la cual actuará como Web Moodle. Esta instancia será creada para servir como Imagen AMI más adelante en el Autoscaling Group. Diríjase al “home” de la consola de administración de AWS. 

Escoja el servicio de EC2. En el panel izquierdo seleccione la opción de “Instances” seleccione la opción “launch instances”. Escoja la imagen de Amazon Machine Image (AMI) la cual contiene la imagen del sistema operativo. Seleccione Amazon Linux 2 AMI (HVM), SSD Volume Type (click select). Seleccione el tipo de instancia t2.micro (columna type) y click “configure instance details”. Ahora configure los siguientes parámetros:

Dado que tendremos multiples máquinas para el Auto-scaling sin dirección ip pública, se hace necesaria la creación de una máquina Bastion Host para acceder a estas,
está maquina no tiene ninguna particularidad en su creación salvo que solo tendrá habilitado el puerto 22. 

- Network: VPC-default
- Subnet: subnet-public
- Auto-assign Public IP: enable
- File systems: Click en “Add file system”
  - Seleccionar el EFS Creado anteriormente (WP-EFS)
  - Como ruta en vez de /mnt/efs/fs1 -> coloque /mnt/efs/moodle
  - Des-seleccionar la opción: Automatically create and attach the required security groups.
- Click en “Add storage”.
- Click en “Add tags”.
  - Key: Name.
  - Value: Web Server.
- Click en “Configure security group”:
  - Seleccione la opción de un security group existente. Seleccione “SG-Web”

Luego, puede lanzarse la instancia. Ahora, puede verse desde la consola de AWS.

![image](https://user-images.githubusercontent.com/71454879/168447690-3ee062bf-0470-4be6-9893-47ebe085a0a5.png)



### Configurar Docker
Dado que las máquinas que contienen el Moodle no tienen conexión a internet, tenemos que conectarnos desde el Bastion Host. Para ello, debe conectarse por medio de ssh.

```bash
ssh -i "Misclaves.pem" ec2-user@172.31.21.235
```

Una vez concretada la conexión a la máquina, puede instalarse Docker y docker-compose.

```bash
sudo amazon-linux-extras install docker -y
sudo yum install git -y
sudo systemctl enable docker
sudo systemctl start docker
7
sudo usermod -a -G docker ec2-user
pip3 install docker-compose
```
Posterior a la instalación de docker y todo lo necesario en la máquina, se crea una carpeta llamada moodle y dentro de esta creamos usando nano o vim, un archivo
[docker-compose.yml](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/AWS/Scripts/docker-compose.yml)
```bash
mkdir moodle
cd moodle
sudo nano docker-compose.yml
```
Se alteraron los siguientes campos en el docker-compose.yml
- MOODLE_DATABASE_HOST = database-1.c4dkqd8k6b30.us-east-1.red.amazonaws.com
- MOODLE_DATABASE_USER = admin
- MOODLE_DATABASE_PASSWORD = moodle123

### AMI - Auto Scaling

Ahora, se crea el grupo de destino, con miras a comenzar con el auto-scaling.
Dentro del apartado EC2 de AWS nos iremos a la categoria de equilibrio de carga y después a Grupos de Destino. 

Aqui dentro crearemos el grupo de destino con la siguiente configuración:
- Choose a target type: Instances.
- Target group name: TG-MyWebApp.
- Protocol: HTTP:80
- VPC: VPC-default
- Protocol version: HTTP1

En el siguiente paso, podremos seleccionar que instancias deseamos para el grupo de destino. No obstante, no se necesita ninguna configuración adicional, por lo que puede crearse el Target Group.

Al crearse, debe poder verse desde la consola de AWS:
![image](https://user-images.githubusercontent.com/71454879/168448162-2008fffd-3ef7-409b-886d-2c14ac88034e.png)

### Balanceador de Cargas
Ahora crearemos nuestro balanceador de carga, para esto dentro del apartado de EC2, en la misma categoria de equilibrio de carga, iremos a balanceadores de carga:

Dentro de la consola, se debe dar click en Crear balanceador de carga:
![image](https://user-images.githubusercontent.com/71454879/168448218-29c372b3-d801-499f-9dee-4c9b5b9c3715.png)

Aunque AWS ofrece distintos tipos, nuestro caso concreto demanda Application Load Balancer.
![image](https://user-images.githubusercontent.com/71454879/168448228-8bc2d135-c161-47dc-a99b-bd876c00c194.png)

Luego, en el apartado de configuración que veremos usaremos los siguientes parámetros:
- En la sección de configuración básica:
  - Name: ELB-MyWebApp
  - Scheme: Seleccione internet-facing.
  - IP address type: ipv4
  - VPC: VPC-default.
- En la sección de Listeners:
  - Load Balancer Protocol: http.
  - Load Balancer Port: 80.
  - Default action: seleccionamos el grupo de destino creado anteriormente: TG-MyWebApp
- En la sección de Network mapping:
  - VPC: VPC-default
  - Availability Zones: Seleccionamos la casilla todas las zonas de disponibilidad.
- En la sección de Security Settings no haremos nada y pasaremos a los Security Groups
- En la sección de Configure Security Group, seleccionamos la opción de escoger un security group existente, aqui escogeremos el grupo de SG-Web.

Si todo salió bien veremos la siguiente pantalla:
![image](https://user-images.githubusercontent.com/71454879/168448578-0da7ecf8-b0a5-4811-a228-b710ce53d9dd.png)

### Launch Template
Esta será la plantilla que se usará para crear todas las maquinas del grupo de Auto-Scaling. Dentro del apartado de EC2 en la categoria de instancias seleecionamos Plantillas de lanzamiento.

Esta vez, se requieren siguientes configuraciones:
- Launch configuration name: MyWebApp
- Template version description: Template for web moodle.
- Auto Scaling guidance: Activamos la casilla.

Ahora en Launch template contents
- Application and OS Images (Amazon Machine Image): En myAMIs, click en
Owned by me, aqui seleccionamos nuestra AMI creada anteriormente para esto.
- Instance type: t2.micro
- Key pair: Aqui seleccionamos nuestras claves de acceso para las instancias EC2.

Todo lo demás queda por defecto y podemos crear nuestra plantilla.
![image](https://user-images.githubusercontent.com/71454879/168448748-47b5197d-2cfc-4466-8ff6-ffaaa28ac6b8.png)

### Auto-Scaling Group
Para esto, podemos usar el vinculo que nos brindó la pantalla anterior. 
En el primer paso tendremos esta configuración:

- Digite el nombre del auto scaling group:
  - Name: MyWebApp-Auto Scaling Group
  - Launch template: MyWebApp

![image](https://user-images.githubusercontent.com/71454879/168448790-1d961b57-6940-4428-9c9d-0a0f4c2fca5a.png)

- En la sección, Network, configure los siguientes parámetros:
- Network: VPC-default.
- Subnet: Seleccione las dos subredes publicas (-1a y -1b) ubicadas en las dos zonas de
disponibilidad.

![image](https://user-images.githubusercontent.com/71454879/168448817-202e2d2c-26ed-4243-a014-4d56169078c6.png)
Al terminar, Tendríamos la siguiente configuración:
![network]()

- En la sección de Configure advanced options:
  - Seleccione la casilla para: Attach to an existing load balancer.
  - Escoja: Choose from your load balancer target groups
  - Escoja el target group que se creó para la aplicación. TG-MyWebApp.
  - Marque la casilla de Enable group metrics collection within CloudWatch.

![image](https://user-images.githubusercontent.com/71454879/168448861-c79e4c03-e06f-4d08-a37c-0fea166a198a.png)
![image](https://user-images.githubusercontent.com/71454879/168448862-dfadd62b-1c04-45c1-8f08-54c8f210e20d.png)
![group]()

- En la sección de Configure Group Size
  - Desired capacity: 2
  - Minimum capacity: 2
  - Maximum capacity: 3.
  *Esta configuración permite escalar entre dos y tres máquinas.*
- En esta misma sección para scaling policies:
  - Seleccione target tracking scaling policy.
  - Scaling policy name: MyWebApp-ScalingPolicy
  - Metric type: Average CPU utilization.
  - Target Value: 60.

Al terminar, Tendríamos la siguiente configuración:
![size]()

Esta configuración le va a indicar al servicio de auto scaling mantener en promedio una utilización de CPU de las instancias del 60%. De esta forma, el servicio de auto scaling automáticamente adicionará o quitará capacidad tanto como sea requerido con el fin de mantener la métrica seleccionada lo más cercana posible al umbral definido. 

- En el apartado Añadir notificación no haremos nada, siguiente:
  - Add Tags

- En el apartado de etiquetas:
  - Key: Name
  - Value: WebServer
  - Click Next


Si todo salió bien veremos esto:
![image](https://user-images.githubusercontent.com/71454879/168448988-1ebca9df-3406-4132-a6e6-8662c23eba90.png)

Al observar detalles del Balanceador de Cargas:
![lb]()



### Confirmación

Una vez llegado a este punto, puede probarse que funciona correctamente al digitar el dominio en cualquier browser
- *http://elb-mywebapp-2141596622.us-east-1.elb.amazonaws.com/*

Debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/moodleScreen.PNG)
