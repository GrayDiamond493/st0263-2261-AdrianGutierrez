# Despliegue Monolítico

## Prerequisitos

- Una VM con Debian GNU/Linux 11 (bullseye).
- IP Pública.
    - Preferiblemente ‘Estática’ o ‘Elástica’.
- Permitir tráfico de puertos 80 (HTTP) y 443 (HTTPS).
- Una conexión a Internet a cada máquina.
- Usuario con privilegios root (sudo).
- Acceso y credenciales al cliente VPN académico.

## Instalar Docker y docker-compose
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

## Create docker-compose.yml
- Crear directorio para el proyecto en home. 
```bash
mkdir ~/project
```
- Cambia el directorio. 
```bash
cd ~/project
```
- Finalmente, crear un archivo de nombre `docker-compose.yml` fy pegar el siguiente contenido:
    ```yml
    version: '2'
    services:
    mariadb:
        image: docker.io/bitnami/mariadb:10.6
        environment:
        # ALLOW_EMPTY_PASSWORD is recommended only for development.
        - ALLOW_EMPTY_PASSWORD=yes
        - MARIADB_USER=bn_moodle
        - MARIADB_DATABASE=bitnami_moodle
        - MARIADB_CHARACTER_SET=utf8mb4
        - MARIADB_COLLATE=utf8mb4_unicode_ci
        volumes:
        - 'mariadb_data:/bitnami/mariadb'
    moodle:
        image: docker.io/bitnami/moodle:3
        ports:
        - '80:8080'
        - '443:8443'
        environment:
        - MOODLE_DATABASE_HOST=mariadb
        - MOODLE_DATABASE_PORT_NUMBER=3306
        - MOODLE_DATABASE_USER=bn_moodle
        - MOODLE_DATABASE_NAME=bitnami_moodle
        # ALLOW_EMPTY_PASSWORD is recommended only for development.
        - ALLOW_EMPTY_PASSWORD=yes
        volumes:
        - 'moodle_data:/bitnami/moodle'
        - 'moodledata_data:/bitnami/moodledata'
        depends_on:
        - mariadb
    volumes:
    mariadb_data:
        driver: local
    moodle_data:
        driver: local
    moodledata_data:
        driver: local
    ```

## Corre el proyecto

```bash
docker-compose up -d
```
