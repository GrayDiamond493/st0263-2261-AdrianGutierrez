# Despliegue DCA

Para este proyecto, se pretende desplegar una aplicación open source LAMP de comunidad que represente un sistema de información del tipo Sistema de Gestión de Aprendizaje (LMS, por sus siglas en inglés). En este caso se seleccionará Moodle para ser desplegado en DCA (Data Center Academico). En cuanto a seguridad, ya se cuenta con un certificado ssl por parte del dominio asignado. 

El objetivo de este proyecto es migrarlo al dominio *vpl1.dis.eafit.edu.co/*.

## Prerequisitos

- Una VM con Debian GNU/Linux 11 (bullseye).
- IP Pública.
    - Preferiblemente ‘Estática’ o ‘Elástica’.
- Permitir tráfico de puertos 80 (HTTP) y 443 (HTTPS).
- Una conexión a Internet a cada máquina.
- Usuario con privilegios root (sudo).
- Acceso y credenciales al cliente VPN académico.

## Arquitectura

Para alcanzar un modelo de altamente escalable, con alta disponibilidad y rendimiento, se planteó la siguiente arquitectura:

![Arquitectura](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/ArquitecturaDCA.drawio.svg) 

- Proxy Inverso/Load Balancer: *192.168.10.190*
   - Conecta con:
   - Moodle 1: *192.168.10.205*
        - Conecta con:
        - MariaDB: *192.168.10.152*
        - NFS: *192.168.10.153*

   - Moodle 2: *192.168.10.206*
        - Conecta con:
        - MariaDB: *192.168.10.152*
        - NFS: *192.168.10.153*

## Conexión

Para conectarse a cada máquina, se debe contar con conexión constante a la VPN académica.

Una vez conectado a la VPN, conectarse remotamente a las máquinas por medio de *ssh*.

``` 
ssh <user>@<ip>
```

En nuestro caso concreto, al haber configurado las credenciales de cada máquina, sería:

``` 
ssh userdca@192.168.10.X
```

Donde 'x' consiste en el host al que se desea conectarse. Para este proyecto, se tienen las 5 máquinas descritas anteriormente.

## Configuración

Para el despliegue de la aplicación, se inicia desde las capas más bajas (almacenamiento y datos, respectivamente) hasta llegar a la capa de aplicación y balanceo de cargas.

### Instalar Docker y docker-compose

```bash
# Actualizar sistema
sudo apt-get update
# Instalar Dependencias
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
# Instalar Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose
sudo systemctl enable docker --now
# Permitir Docker desde usuarios no-root
USER=$(whoami)
sudo usermod -G docker $USER
```
*Nota: Esto debe realizarse en todas las máquinas.*

### NFS-Server

- Configurar máquina destinada a NFS-Server.

```bash
sudo apt install nfs-kernel-server
sudo mkdir -p /srv/nfs/moodle

# Agregar esta linea al final del archivo /etc/exports
sudo vim /etc/exports
/srv/nfs/moodle 192.168.10.0/24(rw,sync,no_root_squash)

sudo systemctl restart nfs-kernel-server
```
*Recuperado de: https://linuxconfig.org/how-to-set-up-a-nfs-server-on-debian-10-buster*

Una vez terminado, la configuración de la máquina debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/5.NFS.jpg)

### MariaDB

- Clonar repositorio oficial de la materia:

```bash 
cd $HOME
git clone https://github.com/st0263eafit/st0263-2261.git
cd st0263-2261/proyecto2
```

- Configurar máquina destinada a Bases de Datos.

```bash 
mkdir $HOME/mariadb
cp docker-compose-mariadb.yml $HOME/mariadb/docker-compose.yml
cd $HOME/mariadb
```
- *Nota: Es sumamente importante cambiar las IPs en  los archivos docker-compose.yml por las usadas verdaderamente en el proyecto*
- *El archivo docker-compose.yml se encuentra en este repositorio bajo el nombre: [docker-compose-mariadb.yml](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Scripts/docker-compose-mariadb.yml)*
```
# Subir imagen de Docker
docker-compose up -d
```

Una vez terminado, la configuración de la máquina debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/4.MariaDB.jpg)

### Moodle 1
- Clonar repositorio oficial de la materia:

```bash 
cd $HOME
git clone https://github.com/st0263eafit/st0263-2261.git
cd st0263-2261/proyecto2
```

- Instalar NFS-Client nativo en Linux.
*Recordatorio: la IP del NFS-Server es:192.168.10.153*

```bash 
sudo apt install nfs-common
sudo mkdir -p /shares/moodle
# Conectarse manualmente al NFS-Server:
sudo mount -t nfs4 192.168.10.153:/srv/nfs/moodle /shares/moodle
# Configurarlo para cada que baje y suba la máquina, se conecte al NFS-Server
```

Luego, debe agregarse la siguiente línea al final del archivo /etc/fstab

```bash
sudo vim /etc/fstab
192.168.10.153:/srv/nfs/moodle	/shares/moodle	nfs4	defaults,user,exec	0 0
```

*Recuperado de: https://linuxconfig.org/how-to-set-up-a-nfs-server-on-debian-10-buster*

- Configurar máquina destinada a la aplicación (Moodle 1).

```bash 
mkdir $HOME/moodle
cp docker-compose-moodle.yml $HOME/moodle/docker-compose.yml
cd $HOME/moodle
```

- *Nota: Es sumamente importante cambiar las IPs en  los archivos docker-compose.yml por las usadas verdaderamente en el proyecto*
- *El archivo docker-compose.yml se encuentra en este repositorio bajo el nombre: [docker-compose-moodle.yml](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Scripts/docker-compose-moodle.yml)*

```bash 
# Subir imagen de Docker
docker-compose up -d
```

Una vez terminado, la configuración de la máquina debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/2.Moodle1.jpg)

### Moodle 2
- Clonar repositorio oficial de la materia:

```bash 
cd $HOME
git clone https://github.com/st0263eafit/st0263-2261.git
cd st0263-2261/proyecto2
```

- Instalar NFS-Client nativo en Linux.
*Recordatorio: la IP del NFS-Server es:192.168.10.153*

```bash 
sudo apt install nfs-common
sudo mkdir -p /shares/moodle
# Conectarse manualmente al NFS-Server:
sudo mount -t nfs4 192.168.10.153:/srv/nfs/moodle /shares/moodle
# Configurarlo para cada que baje y suba la máquina, se conecte al NFS-Server
```

Luego, debe agregarse la siguiente línea al final del archivo /etc/fstab

```bash
sudo vim /etc/fstab
192.168.10.153:/srv/nfs/moodle	/shares/moodle	nfs4	defaults,user,exec	0 0
```

*Recuperado de: https://linuxconfig.org/how-to-set-up-a-nfs-server-on-debian-10-buster*

- Configurar máquina destinada a la aplicación (Moodle 2).

```bash 
mkdir $HOME/moodle
cp docker-compose-moodle.yml $HOME/moodle/docker-compose.yml
cd $HOME/moodle
```

- *Nota: Es sumamente importante cambiar las IPs en  los archivos docker-compose.yml por las usadas verdaderamente en el proyecto*
- *El archivo docker-compose.yml se encuentra en este repositorio bajo el nombre: [docker-compose-moodle.yml](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Scripts/docker-compose-moodle.yml)*

```bash 
# Subir imagen de Docker
docker-compose up -d
```

Una vez terminado, la configuración de la máquina debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/3.Moodle2.jpg)

### Load Balancer
- Clonar repositorio oficial de la materia:

```bash 
cd $HOME
git clone https://github.com/st0263eafit/st0263-2261.git
cd st0263-2261/proyecto2
```

- Configurar máquina destinada a Balanceador de Carga.

```bash 
mkdir $HOME/nginx-lb
cp docker-compose-nginx-lb.yml $HOME/nginx-lb/docker-compose.yml
cp nginx-lb.conf $HOME/nginx-lb/nginx.conf
cd $HOME/nginx-lb
```

- *Nota: Es sumamente importante cambiar las IPs en  los archivos docker-compose.yml  y ngninx.conf por las usadas verdaderamente en el proyecto*
- *El archivo docker-compose.yml se encuentra en este repositorio bajo el nombre: [docker-compose-nginx-lb.yml](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Scripts/docker-compose-nginx-lb.yml)*
- *El archivo nginx.conf se encuentra en este repositorio bajo el nombre: [nginx-lb.conf](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Scripts/nginx-lb.conf)*

```bash 
# Subir imagen de Docker
docker-compose up -d
```

Una vez terminado, la configuración de la máquina debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/1.NginxLB.jpg)

### Confirmación

Una vez llegado a este punto, puede probarse que funciona correctamente al digitar el dominio en cualquier browser
- *vpl1.dis.eafit.edu.co/*

Debería verse de la siguiente manera:

![Screenshot](https://github.com/GrayDiamond493/st0263-2261-AdrianGutierrez/blob/main/proyecto2/DCA/Images/moodleScreen.PNG)
