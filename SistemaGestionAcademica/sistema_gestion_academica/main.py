# Archivo: main.py
from sistema_gestion_academica.login import mostrar_login
from sistema_gestion_academica.menu_principal import abrir_menu
from sistema_gestion_academica.db.database import crear_bd

def main():
    crear_bd()
    mostrar_login(abrir_menu)