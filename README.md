# durobot - fotos duras

## Descripción
 Este bot da fotos duras

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

```bash
!durosave
```

Este comando guarda una foto dura, tienes que pones una foto

---

```
!duro
```

Este comando muestra aleatoriamente una foto dura anteriormente guardada en el server

--- 

```
!lmaosave
```

Este comando guarda un video gracioso. tienes que pones un video

--- 

```
!lmao
```

Este comando muestra aleatoriamente un video gracioso que fue guardado.

---

### TODO:

- mensajes custom para cada server
- mas comandos de fotos y videos duros
- comandos para admin

De momento no hay ningún bot publico, pero proximamente habrá
