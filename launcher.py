import pygame
import sys
import os
import zipfile
import shutil
import subprocess
from datetime import datetime

pygame.init()
ANCHO, ALTO = 1000, 700
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Launcher de Juegos')

COLORS = {
    'fondo': (30, 30, 30),
    'panel_fondo': (40, 40, 40),
    'boton': (70, 70, 70),
    'boton_hover': (90, 90, 90),
    'boton_disabled': (50, 50, 50),
    'texto': (255, 255, 255),
    'texto_desactivado': (130, 130, 130),
    'buscador': (50, 50, 50),
    'texto_buscador': (220, 220, 220),
    'sombra': (10, 10, 10)
}

fuente = pygame.font.Font(None, 40)
fuente_buscador = pygame.font.Font(None, 36)

def draw_button(surf, rect, text, base_color, hover_color, font, enabled=True):
    mouse = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mouse) and enabled else base_color
    sombra_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
    pygame.draw.rect(surf, COLORS['sombra'], sombra_rect, border_radius=10)
    pygame.draw.rect(surf, color, rect, border_radius=10)
    text_color = COLORS['texto'] if enabled else COLORS['texto_desactivado']
    txt = font.render(text, True, text_color)
    surf.blit(txt, (rect.x + (rect.w - txt.get_width()) // 2,
                    rect.y + (rect.h - txt.get_height()) // 2))

def draw_search_box(surf, rect, base_color, text, font, text_color):
    sombra_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
    pygame.draw.rect(surf, COLORS['sombra'], sombra_rect, border_radius=10)
    pygame.draw.rect(surf, base_color, rect, border_radius=10)
    txt = font.render(text, True, text_color)
    surf.blit(txt, (rect.x + 10, rect.y + (rect.height - txt.get_height()) // 2))

def cargar_juegos():
    games_folder = "GAMES"
    juegos = []
    if not os.path.exists(games_folder):
        os.makedirs(games_folder)
    for archivo in os.listdir(games_folder):
        if archivo.endswith(".zip"):
            nombre_juego = os.path.splitext(archivo)[0]
            juegos.append({"nombre": nombre_juego, "archivo_zip": archivo})
    return juegos

def obtener_version_desde_txt(path):
    try:
        with open(path, "r") as f:
            for linea in f:
                if linea.startswith("fecha:"):
                    return linea.replace("fecha:", "").strip()
    except:
        pass
    return "1900-01-01 00:00:00"

def obtener_version_zip(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if "version.txt" in zip_ref.namelist():
                with zip_ref.open("version.txt") as vf:
                    for linea in vf.read().decode("utf-8").splitlines():
                        if linea.startswith("fecha:"):
                            return linea.replace("fecha:", "").strip()
    except Exception as e:
        print(f"Error obteniendo la versión del archivo zip: {e}")
    return "1900-01-01 00:00:00"

def parse_fecha(fecha_str):
    formatos = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt)
        except ValueError:
            continue
    return datetime.min

def hay_actualizacion(juego):
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    carpeta_local = os.path.join(escritorio, juego["nombre"])
    version_local = obtener_version_desde_txt(os.path.join(carpeta_local, "version.txt"))
    version_zip = obtener_version_zip(os.path.join("GAMES", juego["archivo_zip"]))
    try:
        fecha_local = parse_fecha(version_local)
        fecha_zip = parse_fecha(version_zip)
        return fecha_zip > fecha_local
    except Exception as e:
        print(f"Error comparando versiones: {e}")
        return False

def actualizar_version_txt(juego):
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    carpeta_local = os.path.join(escritorio, juego["nombre"])
    version_zip = obtener_version_zip(os.path.join("GAMES", juego["archivo_zip"]))
    version_path = os.path.join(carpeta_local, "version.txt")
    try:
        with open(version_path, "w") as f:
            f.write(f"fecha: {version_zip}\n")
    except Exception as e:
        print(f"Error actualizando version.txt: {e}")

def instalar_juego(juego):
    games_folder = "GAMES"
    juego_zip = os.path.join(games_folder, f"{juego['nombre']}.zip")
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    carpeta_destino = os.path.join(escritorio, juego["nombre"])
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)
    os.makedirs(carpeta_destino)
    with zipfile.ZipFile(juego_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_destino)
    contenido = os.listdir(carpeta_destino)
    if len(contenido) == 1:
        subcarpeta = os.path.join(carpeta_destino, contenido[0])
        if os.path.isdir(subcarpeta):
            for item in os.listdir(subcarpeta):
                shutil.move(os.path.join(subcarpeta, item), carpeta_destino)
            os.rmdir(subcarpeta)
    actualizar_version_txt(juego)

def ejecutar_juego(juego):
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta_juego = os.path.join(escritorio, juego["nombre"])
    ruta_inicio = os.path.join(ruta_juego, "inicio.py")
    if os.path.exists(ruta_inicio):
        subprocess.Popen(["python", "inicio.py"], cwd=ruta_juego)
    else:
        print(f"No se encontró inicio.py en {ruta_juego}")

def gestionar_panel_visible(panel, estado):
    panel["visible"] = estado

def mostrar_panel_traductor():
    panel_rect = pygame.Rect(220, 100, 600, 400)  # Definir el panel
    pygame.draw.rect(screen, COLORS['panel_fondo'], panel_rect)
    txt_traductor = fuente.render("Archivos de Traductor", True, COLORS['texto'])
    screen.blit(txt_traductor, (panel_rect.x + 20, panel_rect.y + 20))

    y_offset = 60  # Comenzamos después del título
    btns = []
    margen_vertical = 10  # Espacio entre botones
    margen_horizontal = 20  # Espacio horizontal

    try:
        archivos_traductor = [f for f in os.listdir('traducir') if f.endswith('.qp')]
    except FileNotFoundError:
        archivos_traductor = []

    if archivos_traductor:
        for archivo in archivos_traductor:
            # Botón con el texto del archivo
            btn_archivo = pygame.Rect(panel_rect.x + margen_horizontal, y_offset, panel_rect.width - 2 * margen_horizontal, 40)
            draw_button(screen, btn_archivo, archivo, COLORS['boton'], COLORS['boton_hover'], fuente)
            btns.append((btn_archivo, archivo))
            y_offset += btn_archivo.height + margen_vertical  # Ajuste la posición para el siguiente botón

    return btns

def main_menu():
    buscador_rect = pygame.Rect(60, 20, 920, 40)
    texto_buscador = ""
    juegos_por_fila = 4
    btn_width = 140
    btn_height = 140
    margen = 20

    boton_hamburguesa_rect = pygame.Rect(10, 20, 60, 45)
    menu_lateral_visible = False

    btn_config = pygame.Rect(10, 80, 180, 50)
    btn_traductor = pygame.Rect(10, 140, 180, 50)

    panel_config = {"visible": False}
    panel_traductor = {"visible": False}
    panel_visible = {"visible": False}
    juego_seleccionado = None

    btn_archivos = []

    juegos = cargar_juegos()

    while True:
        screen.fill(COLORS['fondo'])

        if menu_lateral_visible:
            panel_lateral = pygame.Rect(0, 0, 200, ALTO)
            pygame.draw.rect(screen, COLORS['panel_fondo'], panel_lateral)
            draw_button(screen, btn_config, "Config", COLORS['boton'], COLORS['boton_hover'], fuente)
            draw_button(screen, btn_traductor, "Traductor", COLORS['boton'], COLORS['boton_hover'], fuente)

        draw_button(screen, boton_hamburguesa_rect, "☰", COLORS['boton'], COLORS['boton_hover'], fuente)
        draw_search_box(screen, buscador_rect, COLORS['buscador'], texto_buscador, fuente_buscador, COLORS['texto_buscador'])

        juegos_filtrados = [juego for juego in juegos if texto_buscador.lower() in juego["nombre"].lower()]
        y_offset = 80
        x_offset = 60 if not menu_lateral_visible else 220
        botones_juegos = []

        for i, juego in enumerate(juegos_filtrados):
            btn_juego = pygame.Rect(x_offset, y_offset, btn_width, btn_height)
            draw_button(screen, btn_juego, juego["nombre"], COLORS['boton'], COLORS['boton_hover'], fuente)
            botones_juegos.append((btn_juego, juego))
            x_offset += btn_width + margen
            if (i + 1) % juegos_por_fila == 0:
                x_offset = 60 if not menu_lateral_visible else 220
                y_offset += btn_height + margen

        if panel_visible["visible"]:
            # Panel del juego seleccionado
            pass

        if panel_traductor["visible"]:
            btn_archivos = mostrar_panel_traductor()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if boton_hamburguesa_rect.collidepoint(e.pos):
                    menu_lateral_visible = not menu_lateral_visible
                if btn_config.collidepoint(e.pos):
                    gestionar_panel_visible(panel_config, True)
                if btn_traductor.collidepoint(e.pos):
                    gestionar_panel_visible(panel_traductor, True)
                for btn_juego, juego in botones_juegos:
                    if btn_juego.collidepoint(e.pos):
                        juego_seleccionado = juego
                        gestionar_panel_visible(panel_visible, True)
                if panel_traductor["visible"]:
                    for btn_archivo, archivo in btn_archivos:
                        if btn_archivo.collidepoint(e.pos):
                            print(f"Has seleccionado el archivo: {archivo}")

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    texto_buscador = texto_buscador[:-1]
                else:
                    texto_buscador += e.unicode

        pygame.display.update()

# Cargar juegos y lanzar el menú principal
main_menu()
