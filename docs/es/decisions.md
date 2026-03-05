# Registro de Decisiones Arquitectonicas (Lite)

## ADR-001: Usar Arquitectura Hexagonal

Contexto:
- El acoplamiento fuerte entre capas hace que los cambios sean dificiles y riesgosos
- Los cambios de framework/base de datos afectan directamente la logica de negocio
- Dificultad para testear la logica de negocio aislada de la infraestructura
- Preocupaciones de mantenibilidad del codigo a medida que crece el proyecto

Decision:
- Usar Arquitectura Hexagonal (Puertos y Adaptadores) para estructurar la aplicacion
- La capa de dominio no tiene dependencias externas (solo libreria estandar)
- Los casos de uso dependen de interfaces de dominio (puertos), nunca de infraestructura
- La infraestructura implementa las interfaces de dominio (adaptadores)
- Inyeccion de dependencias via constructores, sin service locators

Alternativas consideradas:
- Arquitectura por Capas Tradicional (Controller-Service-Repository): mas simple pero crea acoplamiento fuerte entre capas
- Sin arquitectura formal / Monolitica: rapida para empezar pero no escala con el tamano del equipo o la complejidad

Ventajas y desventajas:
+ Clara separacion de responsabilidades entre dominio, aplicacion e infraestructura
+ La logica de negocio es agnostica al framework y facilmente testeable
+ La infraestructura puede intercambiarse sin afectar al dominio (ej., MongoDB a PostgreSQL)
+ Impone inversion de dependencias, mejorando la modularidad
- Mas codigo boilerplate (interfaces, adaptadores, mappers)
- Curva de aprendizaje mas pronunciada para desarrolladores no familiarizados con el patron

Estado:
- Aceptado (2022-02-26)

## ADR-002: Usar PostgreSQL + pgvector

Contexto:
- La aplicacion requiere capacidades de busqueda vectorial para funcionalidades de IA/ML
- Se necesitan transacciones ACID para integridad de datos

Decision:
- Usar PostgreSQL como base de datos relacional principal
- Usar la extension pgvector para busqueda de similitud vectorial y embeddings
- Usar SQLAlchemy como capa ORM
- Usar Alembic para migraciones de base de datos

Alternativas consideradas:
- Qdrant: Buenas capacidades de busqueda vectorial pero anade complejidad operacional al requerir un sistema separado para gestionar

Ventajas y desventajas:
+ Una sola base de datos para todas las necesidades (relacional + vectorial)
+ Ecosistema maduro con excelente documentacion y soporte de comunidad
+ Consultas vectoriales basadas en SQL usando sintaxis familiar
+ Operaciones simplificadas con menos piezas moviles
+ Consistencia de datos sin necesidad de sincronizacion entre sistemas
- Requiere overhead de gestion de extensiones de PostgreSQL
- pgvector es una tecnologia mas nueva, aun en evolucion

Estado:
- Propuesto (2026-02-08)

## ADR-003: Usar OAuth2 / OpenID Connect

Contexto:
- Evitar gestionar credenciales y contrasenas internamente
- Los clientes empresariales requieren integracion SSO
- Debe cumplir con estandares y mejores practicas de seguridad
- Multiples aplicaciones necesitan autenticacion compartida

Decision:
- Usar Authelia como proveedor de identidad OpenID Connect
- Validar JWTs emitidos por Authelia
- Integrar con las dependencias de seguridad de FastAPI
- Implementar manejo de refresh tokens
- Implementar RBAC via claims de OIDC

Alternativas consideradas:
- Keycloak: Auto-hospedado pero pesado en recursos y complejo de operar
- Solo JWT (sin IdP): Tokens sin estado pero carece de gestion centralizada de identidad y capacidades SSO

Ventajas y desventajas:
+ Gestion delegada de credenciales - no es necesario implementar auth desde cero
+ Protocolos estandar de la industria (OAuth2/OIDC)
+ Gestion centralizada de identidad entre multiples aplicaciones
- Requiere infraestructura adicional para desplegar y mantener Authelia
- Complejidad del protocolo con los flujos de OAuth2/OIDC
- Dependencia externa - la autenticacion depende de la disponibilidad de Authelia

Estado:
- Propuesto (2026-02-08)
