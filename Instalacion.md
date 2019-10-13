# Servidor para juego del gato

## Proyecto de la materia de Diseño de Sistemas Inteligentes

### Instalación

Es necesario el uso de un entorno virtual para utilizar solo las dependencias necesarias.

Para crear un entorno virtual es necesario instalar `virtualenv` con pip.

```bash
pip install virtualenv
```

O si se cuenta con `pip3`:

```bash
pip3 install virtualenv
```

Accedemos en la terminal hasta el directorio donde se clonó este repositorio y ejecutamos el comando:

```bash
virtualenv NOMBRE_ENTORNO_VIRTUAL
```

Esto generará una carpeta con el nombre que le dimos al entorno virtual, procederemos a activar el entorno virtual:

```bash
source NOMBRE_ENTORNO_VIRTUAL/bin/activate
```

Nuestra terminal deberá mostrar el nombre del entorno virtual en paréntesis `(entorno)`.

### Instalación de dependencias

Hay un archivo con las dependencias listadas, ejecute el siguiente comando para instalarlas en su entorno virtual:

```bash
pip install -r dependencias.txt
```

### Levantar el servidor

```bash
python server.py
```

Nos indicará en la consola que está escuchando en el puerto 9000.

Posteriormente ejecute un cliente:

```bash
python cliente.py
```

Este script se conectará a través de un websocket hacia el servidor, el juego comenzará hasta que se conecte el segundo jugador. Puede ejecutar lo mismo en otra terminal para simular al segundo jugador.

> Es posible que se encuentren errores o que el funcionamiento no sea el esperado.