# 🎮 Launcher de Juegos en Python

Este proyecto es un **launcher de juegos** de escritorio creado en **Python con Pygame**, que permite gestionar juegos locales empaquetados en archivos `.zip`. Ofrece una interfaz gráfica moderna e interactiva donde puedes buscar juegos, instalarlos, actualizarlos y ejecutarlos con un solo clic.

---

## 🧩 Características principales

- 🎨 Interfaz visual moderna y sombreada usando Pygame.
- 🔍 Barra de búsqueda en tiempo real para filtrar juegos por nombre.
- 📦 Instalación automática desde archivos `.zip`.
- 🆕 Detección y aplicación de actualizaciones si hay una versión más nueva.
- ▶️ Ejecución directa del juego desde un archivo `inicio.py`.
- 📁 Organización por panel: cada juego abre un panel con sus acciones disponibles.
- ❌ Cierre del panel sin afectar el resto del launcher.

---

## 📂 Estructura del proyecto

```plaintext
Launcher/
│
├── launcher.py         # Código principal del launcher
├── GAMES/              # Carpeta para los juegos (archivos .zip)
│   ├── Juego1.zip
│   └── Juego2.zip
└── README.md           # Este archivo
