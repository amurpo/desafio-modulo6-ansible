# Usar una imagen base, por ejemplo, Ubuntu 20.04
FROM ubuntu:20.04

# Instalar servidor SSH y otras dependencias necesarias
RUN apt-get update && apt-get install -y \
  openssh-server \
  python3 \
  && rm -rf /var/lib/apt/lists/*

# Crear directorio para el proceso SSH
RUN mkdir /var/run/sshd

# Permitir autenticación por contraseña (opcional, pero menos seguro)
RUN echo 'root:12345678' | chpasswd

# Configurar SSH para permitir acceso remoto
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Exponer el puerto SSH
EXPOSE 22
EXPOSE 80

# Iniciar el servidor SSH
CMD ["/usr/sbin/sshd", "-D"]

