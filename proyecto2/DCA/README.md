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

![Arquitectura]() 

-> Proxy Inverso/Load Balancer: *192.168.10.190*
   Conecta con:
   -> Moodle 1: *192.168.10.205*
        Conecta con:
        MariaDB: *192.168.10.153*
        NFS: *192.168.10.152*

   -> Moodle 2: *192.168.10.206*
        Conecta con:
        MariaDB: *192.168.10.153*
        NFS: *192.168.10.152*


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