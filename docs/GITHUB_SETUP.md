# 📤 Guía: Subir el Código a tu GitHub (Windows)

## Paso 1: Instalar Git (si no lo tienes)

### 1.1 Verificar si ya tienes Git

En VS Code, abre la terminal (Ctrl + `) y escribe:

```bash
git --version
```

**¿Qué pasó?**

- ✅ Si dice algo como `git version 2.x.x` → Ya tienes Git, **salta al Paso 2**
- ❌ Si dice `'git' no se reconoce como un comando...` → Continúa abajo

### 1.2 Instalar Git (5 minutos)

1. Ve a: https://git-scm.com/download/win
2. Descarga el instalador (64-bit recomendado)
3. Ejecuta el instalador
4. **IMPORTANTE**: En las opciones, deja todo por defecto EXCEPTO:
   - ✅ Marca "Git from the command line and also from 3rd-party software"
   - ✅ Marca "Use Visual Studio Code as Git's default editor"
5. Click "Next" → "Next" → "Install"
6. **Reinicia VS Code** después de instalar

### 1.3 Verificar instalación

Abre VS Code de nuevo, abre terminal (Ctrl + `) y escribe:

```bash
git --version
```

Debe aparecer la versión. ✅

---

## Paso 2: Configurar Git con tu identidad

**Solo se hace UNA vez en tu vida.** Ejecuta estos comandos en la terminal:

```bash
git config --global user.name "Rodolfo"
git config --global user.email "tu-email-de-github@ejemplo.com"
```

⚠️ **Usa el mismo email de tu cuenta de GitHub**

---

## Paso 3: Descargar los archivos del proyecto

### Opción A: Descargar todos los archivos

Yo te voy a dar un link para descargar un ZIP con todo el código. **Espera mi siguiente mensaje.**

### Opción B: Copiar archivos manualmente

Si ya descargaste los archivos que te di anteriormente:

1. En Windows Explorer, ve a: `C:\Users\TuUsuario\Documents`
2. Crea una carpeta llamada `asistente-ia`
3. Copia TODOS los archivos dentro

---

## Paso 4: Inicializar el repositorio Git

En VS Code:

```bash
# 1. Ir a la carpeta del proyecto
cd Documents\asistente-ia

# 2. Inicializar Git
git init

# 3. Ver qué archivos tenemos
dir
```

Debes ver todos los archivos .py, .md, etc.

---

## Paso 5: Conectar con GitHub

### 5.1 Crear repositorio en GitHub (3 minutos)

1. Ve a: https://github.com/Rodolfo-CWS
2. Click en el botón verde **"New"** (arriba a la derecha)
3. Configuración:
   - **Repository name**: `asistente-ia`
   - **Description**: "Asistente de IA personal por WhatsApp"
   - ✅ **Public** (o Private si prefieres)
   - ❌ NO marques "Add a README file"
   - ❌ NO agregues .gitignore
   - ❌ NO agregues license
4. Click **"Create repository"**

### 5.2 Copiar la URL del repositorio

Después de crear el repo, GitHub te muestra una página con comandos. 

**Copia la URL que aparece**, algo como:
```
https://github.com/Rodolfo-CWS/asistente-ia.git
```

---

## Paso 6: Subir el código

En la terminal de VS Code, ejecuta estos comandos **UNO POR UNO**:

```bash
# 1. Agregar todos los archivos
git add .

# 2. Hacer el primer commit
git commit -m "Initial commit - MVP Asistente IA Personal"

# 3. Agregar la URL de tu repositorio
git remote add origin https://github.com/Rodolfo-CWS/asistente-ia.git

# 4. Cambiar a rama main
git branch -M main

# 5. Subir el código
git push -u origin main
```

### ⚠️ Si te pide usuario y contraseña:

GitHub ya NO acepta contraseñas. Necesitas un **Personal Access Token**.

**Crear token (2 minutos):**

1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Configuración:
   - **Note**: "Asistente IA Token"
   - **Expiration**: 90 days
   - ✅ Marca solo: `repo` (todo lo que está debajo)
4. Click "Generate token"
5. **COPIA EL TOKEN INMEDIATAMENTE** (no lo verás de nuevo)

Cuando Git te pida contraseña, pega el token (no se verá al escribir, es normal).

---

## Paso 7: Verificar que funcionó

1. Ve a: https://github.com/Rodolfo-CWS/asistente-ia
2. Debes ver todos tus archivos ahí ✅

---

## ✅ Listo!

Ya tienes el código en GitHub. Ahora puedes:

1. Clonarlo en cualquier computadora
2. Hacer cambios y subirlos
3. Compartir el proyecto
4. Volver a versiones anteriores

---

## 🆘 Problemas Comunes

**"fatal: not a git repository"**
→ Asegúrate de estar en la carpeta correcta: `cd Documents\asistente-ia`

**"error: remote origin already exists"**
→ Ejecuta: `git remote remove origin` y vuelve a intentar el paso 6.3

**"Permission denied"**
→ Verifica tu token de GitHub o regenera uno nuevo

**"Failed to push"**
→ Puede ser que el repo ya tenga archivos. Ejecuta: `git pull origin main --allow-unrelated-histories`

---

**¿Siguiente paso?** Una vez que esté en GitHub, te enseño a clonarlo en tu máquina y configurar todo para que funcione.
