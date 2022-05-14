# Despliegue DCA

Para este proyecto, se pretende desplegar una aplicación open source LAMP de comunidad que represente un sistema de información del tipo Sistema de Gestión de Aprendizaje (LMS, por sus siglas en inglés). En este caso se seleccionará Moodle para ser desplegado en DCA (Data Center Academico).

El objetivo de este proyecto es migrarlo al dominio *vpl1.dis.eafit.edu.co/*.

## Prerequisitos

## Conexión

Para conectarse a cada máquina, se debe contar con conexión constante a la VPN académica.

Una vez conectado a la VPN, conectarse remotamente a las máquinas por medio de *ssh*.

``` ssh <user>@<ip>
```

En nuestro caso concreto, al haber configurado las credenciales de cada máquina, sería:

``` ssh userdca@192.168.10.X
```

Donde 'x' consiste en el host al que se desea conectarse. Para este proyecto, se tienen 5 máquinas.

## Arquitectura

## Configuración