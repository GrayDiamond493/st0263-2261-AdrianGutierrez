# Despliegue DCA

Para este proyecto, se pretende desplegar una aplicación open source LAMP de comunidad que represente un sistema de información del tipo Sistema de Gestión de Aprendizaje (LMS, por sus siglas en inglés). En este caso se seleccionará Moodle para ser desplegado en DCA (Data Center Academico).

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
        - MariaDB: *192.168.10.153*
        - NFS: *192.168.10.152*

   - Moodle 2: *192.168.10.206*
        - Conecta con:
        - MariaDB: *192.168.10.153*
        - NFS: *192.168.10.152*


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

Donde 'x' consiste en el host al que se desea conectarse. Para este proyecto, se tienen 5 máquinas.

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

### Moodle 2

### Load Balancer

### Confirmación

Una vez llegado a este punto, puede probarse que funciona correctamente al digitar el dominio en cualquier browser
- *vpl1.dis.eafit.edu.co/*

