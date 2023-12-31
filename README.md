# durobot - fotos duras

Este bot da fotos duras.

[Invitar al server](https://discord.com/oauth2/authorize?client_id=1177340107649466468&scope=bot&permissions=83968)

## Configuración

### Paso 1: Crear una nueva aplicación en el Portal de Desarrolladores de Discord

1. Ve al [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).
2. Crea una nueva aplicación.
3. En la sección "Bot", haz clic en "Add Bot" para convertir tu aplicación en un bot.
4. Copia el token del bot.

### Paso 2: Configurar el entorno

1. Crea un archivo llamado `.env` en el directorio del bot.
2. Agrega el token del bot al archivo `.env`:

  ```env
  DISCORD_TOKEN=your_bot_token_here
  ```

### Paso 3: Instalar dependencias

Ejecuta el siguiente comando en tu terminal para instalar las dependencias necesarias:

  ```bash
  pip install -r requirements.txt
  ```

### Paso 4: Ejecutar el bot

Ejecuta el bot con el siguiente comando:

```bash
python bot.py
```

# Comandos:

```
!durosave
```

Este comando guarda una foto dura, tienes que pones una foto


```
!duro
```

Este comando muestra aleatoriamente una foto dura anteriormente guardada en el server

--- 

```
!lmaosave
```

Este comando guarda un video gracioso. tienes que pones un video


```
!lmao
```

Este comando muestra aleatoriamente un video gracioso que fue guardado.

---

```
!durumsave
```

Este comando guarda un durum, tienes que subir una foto de un durum


```
!durum
```

Este comando muestra aleatoriamente un durum

---

### Cosas para admins

Cuando corrais el bot por primera vez, se os crearán 2 carpetas con 1 archivo dentro de cada una.

La carpeta `server_lists` contiene un archivo csv con el id de vuestro server. Este archivo contiene los links de los archivos, quien lo ha subido, su hash sha256 (usado para ver si el archivo ya existía), y su tipo (0 -> duro, 1 -> lmao, 2 -> durum).

La carpeta `server_config` contiene un archivo json con el id de vuestro server. Este archivo contiene las frases que quieres que diga el bot cada vez que ocurre una acción. Este archivo tambien contiene una configuración por si quieres usar fotos publicas o solo las privadas que subas tu. Simplemente cambia `use_public_images` a `true` si quieres usar las fotos publicas, o a `false` si solo quieres usar las que guardes con durosave

### TODO:

- mas comandos de fotos y videos duros
- comandos para admin
