# desafio-modulo6-ansible
Desafío – Implementación de una Infraestructura Automatizada con Ansible y Docker

Este proyecto utiliza Ansible para configurar y desplegar servidores web con Nginx en contenedores. La configuración incluye la creación de un entorno básico con tareas comunes, la instalación de Nginx, y la implementación de páginas HTML dinámicas.

## Estructura del Proyecto

```plaintext
.
├── ansible.cfg
├── group_vars/
│   └── all.yml
├── requirements.yml
├── site.yml
├── roles/
    ├── common/
    │   └── tasks/
    │       └── main.yml
    └── webserver/
        ├── handlers/
        │   └── main.yml
        ├── meta/
        │   └── main.yml
        ├── tasks/
        │   └── main.yml
        ├── templates/
        │   ├── index.html.j2
        │   └── nginx.conf.j2
        └── vars/
            └── main.yml
```

## Configuración

### Variables de Grupo (`group_vars/all.yml`)
Define las variables globales para los contenedores y la configuración del servidor web:

```yaml
container_names:
  - node1
  - node2
nginx_port: 80
host_port_start: 8081

site_title: "Welcome to {{ ansible_hostname }}"
site_description: "This server is running on {{ ansible_distribution }} {{ ansible_distribution_version }}"
```

### Configuración Local (`ansible.cfg`)
Especifica el archivo de inventario dinámico:

```ini
[defaults]
inventory = ./dynamic_inventory.py
```

## Roles

### Common

El rol `common` incluye tareas generales para preparar el sistema:

#### Tareas (`roles/common/tasks/main.yml`):
```yaml
- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Install required packages
  apt:
    name:
      - nginx
      - curl
      - nano
    state: present
```

### Webserver

El rol `webserver` maneja la instalación y configuración de Nginx.

#### Variables (`roles/webserver/vars/main.yml`):
```yaml
document_root: "/var/www/html"
```

#### Plantillas:

- `index.html.j2`: Página de inicio personalizada con información del sistema.
- `nginx.conf.j2`: Configuración de Nginx para el servidor.

#### Tareas (`roles/webserver/tasks/main.yml`):
Incluye la instalación, configuración y despliegue del servidor:

```yaml
- name: Ensure Nginx is installed
  apt:
    name: nginx
    state: present
  become: true

- name: Create document root
  file:
    path: "{{ document_root }}"
    state: directory
    mode: '0755'

- name: Configure Nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx

- name: Deploy index page
  template:
    src: index.html.j2
    dest: "{{ document_root }}/index.html"
  notify: reload nginx

- name: Ensure Nginx is running
  service:
    name: nginx
    state: started
    enabled: yes

- name: Get server status
  uri:
    url: "http://localhost:{{ nginx_port }}"
    return_content: yes
  register: webpage_content
  ignore_errors: true

- name: Debug webpage content
  debug:
    msg: "Webpage content: {{ webpage_content.content | default('No content fetched') }}"
```

#### Manejadores (`roles/webserver/handlers/main.yml`):
```yaml
- name: restart nginx
  service:
    name: nginx
    state: restarted

- name: reload nginx
  service:
    name: nginx
    state: reloaded
```

#### Dependencias (`roles/webserver/meta/main.yml`):
```yaml
dependencies:
  - role: common
```

## Instalación de Roles Externos

Los roles externos se especifican en `requirements.yml`. Por ejemplo:

```yaml
- src: geerlingguy.docker
  version: "7.4.3"
```

Para instalarlos, ejecuta:
```bash
ansible-galaxy install -r requirements.yml
```

## Despliegue

El archivo principal `site.yml` organiza los roles y configura los servidores web:

```yaml
- name: Deploy web servers in containers
  hosts: all
  become: true
  gather_facts: true

  roles:
    - common
    - webserver
```

Ejecuta el playbook con:
```bash
ansible-playbook -i docker_inventory.py site.yml
```

