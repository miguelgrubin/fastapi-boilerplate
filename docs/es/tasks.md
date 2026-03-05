# Lista de Tareas Futuras

Este documento rastrea las mejoras planificadas e implementaciones pendientes del proyecto.

## Prioridad Alta

- [x] Implementar Autenticacion y Autorizacion usando OpenID con Authelia y Traefik.
- [ ] Usar App Factory para crear Servidor MCP, Servidor HTTP y comandos CLI.

## Prioridad Media

- [x] Crear caso de uso de Articulos e implementaciones de repositorio relacionadas.
- [x] Usar SQLAlchemy y Alembic para interacciones y migraciones de base de datos.
- [ ] Crear implementaciones de repositorio SQL para Usuario y Articulo.
- [ ] Crear Servidor MCP con FastMCP
- [x] Crear Servidor HTTP con FastAPI
- [ ] Crear comandos CLI para crear y listar usuarios.

## Prioridad Baja

- [ ] Implementar OpenTelemetry para trazabilidad y monitoreo.
- [ ] Implementar stack LGTM
- [ ] Definir reglas para agentes
- [ ] Crear agentes para generar componentes

## Completado

- [x] Crear Configuracion de la App
- [x] Implementar error handlers para transformar errores de dominio en errores HTTP (codigo de estado, mensaje de error).
- [x] Clases base de Eventos de Dominio (`shared/domain/events/`)
- [x] Enum de Tipos de Evento (`shared/domain/events/event_types.py`)
- [x] Abstraccion e implementaciones del Servicio de Contrasenas
- [x] Caso de uso de Creacion de Usuario
- [x] Implementaciones de repositorio en Memoria y MongoDB para Usuario
- [x] Implementacion de repositorio en Memoria para Articulo
