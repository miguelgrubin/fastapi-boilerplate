# Arquitectura

**Que?**

Es un ejemplo de blog usando arquitectura hexagonal con modulos de aplicacion. Orientado a proyectos grandes.

**Por que?**

_Por que Arquitectura Hexagonal?_

Puertos y Adaptadores, desacoplamiento, estrategia de testing, trazabilidad de errores. ToDo: Explicar esto

**Como?**

```
Capas              || Componentes    || Estrategia de Testing
=========================================================================================
Presentacion       || Rutas HTTP     || Tests de integracion && E2E
 ↓ ↑               ||                ||
Aplicacion         || Casos de Uso   || Testing Social Unitario (Casos de Uso + Dominio)
 ↓ ↑               ||                ||
Dominio            || Modelos de     || Testing Unitario Solitario (clase o funcion individual)
                   || Dominio        ||
 ↓ ↑               ||                ||
Infraestructura    || Repositorios   || Testing de integracion
```

## Esquema del Proyecto

```
src
├── app
│   ├── blog
│   │   ├── domain
│   │   │   ├── article.py                      <=  Modelo de Dominio de Articulo
│   │   │   ├── article_repository.py           <=  Repositorio Abstracto de Articulo
│   │   │   ├── errors/                         <=  Errores del Dominio del Blog (UserNotFound, UserAlreadyExists, ...)
│   │   │   ├── events/                         <=  Eventos del Dominio del Blog (ArticleCreated, UserFollowed, ...)
│   │   │   ├── user.py                         <=  Modelo de Dominio de Usuario
│   │   │   └── user_repository.py              <=  Repositorio Abstracto de Usuario
│   │   ├── use_cases/                          <=  Casos de Uso
│   │   │   └── user_creator.py
│   │   ├── infrastructure
│   │   │   ├── mappers/                        <=  Mappers para transformar (DTO <=> Modelo de Dominio <=> Modelo ORM)
│   │   │   │   └── user_mapper.py
│   │   │   ├── server/                         <=  Rutas HTTP
│   │   │   │   ├── article_routes.py           <=  Rutas de Articulo
│   │   │   │   ├── user_dtos.py                <=  DTOs de Usuario (Peticiones, respuestas, parametros)
│   │   │   │   └── user_routes.py              <=  Rutas de Usuario
│   │   │   └── storage/                        <=  Implementaciones de Repositorios
│   │   │       ├── article_repository_memory.py
│   │   │       ├── user_repository_memory.py
│   │   │       └── user_repository_mongodb.py
│   │   ├── factory.py                          <=  Fabricas para inicializar el modulo Blog
│   │   └── types.py                            <=  Objetos de tipado del Blog
│   └── shared                                  <=  Modulo Compartido
│       ├── domain/
│       │   ├── domain_model.py                 <=  Modelo de Dominio Base
│       │   └── events/                         <=  Eventos de Dominio & Tipos de Eventos
│       │       ├── domain_event.py
│       │       └── event_types.py
│       ├── services/                           <=  Servicios Compartidos
│       │   ├── domain/
│       │   │   └── password_service.py         <=  Servicio Abstracto de Contrasenas
│       │   ├── infrastructure/
│       │   │   ├── password_service_argon.py   <=  Servicio de Contrasenas Argon2
│       │   │   └── password_service_fake.py    <=  Servicio de Contrasenas Falso (testing)
│       │   └── factories.py                    <=  Fabricas de servicios
│       └── use_case.py                         <=  Definicion base de Caso de Uso
├── config.py                                   <=  Configuracion de la App
├── factories.py                                <=  Fabricas para inicializar una instancia de la App
└── main.py                                     <=  Punto de entrada
```

## Capa de Infraestructura

- **Server**: Son responsables de exponer la aplicacion al mundo exterior. En este ejemplo tenemos un Servidor HTTP implementado con FastAPI, pero podria ser un servidor gRPC o incluso Servidores MCP.
- **Storage**: Son responsables de persistir y recuperar datos de la base de datos. Implementan los repositorios abstractos definidos en la Capa de Dominio. En este ejemplo tenemos dos implementaciones para cada repositorio: en memoria y MongoDB.
- **Services**: Son responsables de interactuar con servicios externos (email, pagos, ...).
- **Mappers**: Son responsables de transformar datos entre diferentes capas (DTO <=> Modelo de Dominio <=> Modelo ORM).

### Componentes del Servidor HTTP

- **Routers**: APIRouter de FastAPI con los endpoints HTTP.
- **DTOs**: Objetos de Transferencia de Datos. Modelos Pydantic para definir la forma de los datos en la capa HTTP (peticiones, respuestas, parametros, ...).
- **Error Handlers**: Funciones para transformar Errores de Dominio en Errores HTTP (codigo de estado, mensaje de error, ...).
- **Guards**: Funciones para verificar precondiciones antes de ejecutar un Caso de Uso (Esta autenticado el usuario? Tiene permisos el usuario para ejecutar esta accion? ...). ToDo: No implementado aun.

### Componentes de Storage (Repositorios)

Son responsables de persistir y recuperar datos de la base de datos. Implementan los repositorios abstractos definidos en la Capa de Dominio. En este ejemplo tenemos dos implementaciones para cada repositorio: en memoria y MongoDB.

### Servicios Externos

Son responsables de interactuar con servicios externos (email, pagos, ...). Implementan los servicios abstractos definidos en la Capa de Dominio Compartido. ToDo: No implementado aun.

## Capa de Aplicacion

- **Casos de Uso**: Son responsables de ejecutar la logica de negocio de la aplicacion. Interactuan con la Capa de Dominio para ejecutar las reglas de negocio y con la Capa de Infraestructura para persistir datos o interactuar con servicios externos. Son el componente principal de la Capa de Aplicacion y el unico que deberia testearse con Testing Social Unitario (Casos de Uso + Dominio). ToDo: Explicar por que.
- **Servicios de Aplicacion**: Son servicios que contienen logica de aplicacion que no pertenece a ningun Caso de Uso especifico. Pueden usarse para implementar reglas de aplicacion complejas que involucran multiples Casos de Uso. ToDo: No implementado aun.

## Capa de Dominio

- **Modelos de Dominio**: Son el componente principal de la Capa de Dominio. Representan las entidades principales de la aplicacion (Usuario, Articulo, ...). Contienen las reglas de negocio y la logica de la aplicacion. Deberian testearse con Testing Unitario Solitario (clase o funcion individual) para asegurar que las reglas de negocio estan correctamente implementadas. ToDo: Explicar por que.
- **Repositorios Abstractos**: Son interfaces que definen los metodos para persistir y recuperar datos de la base de datos. Son implementados por los componentes de Storage de la Capa de Infraestructura.
- **Errores de Dominio**: Son excepciones personalizadas que representan los errores que pueden ocurrir en la Capa de Dominio (UserNotFound, UserAlreadyExists, ...). Se usan para manejar errores en los Casos de Uso y para transformarlos en Errores HTTP en los Error Handlers del Servidor.
- **Eventos de Dominio**: Son eventos que representan algo que ha ocurrido en la Capa de Dominio (ArticleCreated, UserFollowed, ...). Pueden usarse para disparar acciones en la aplicacion (enviar un email cuando se crea un usuario, ...). Las clases base estan definidas en `shared/domain/events/`.
- **Tipos de Evento**: Son un Enum con todos los tipos de evento de la Capa de Dominio (`shared/domain/events/event_types.py`). Pueden usarse para identificar el tipo de un evento cuando queremos disparar acciones en la aplicacion.
- **Servicios de Dominio**: Son servicios que contienen logica de negocio que no pertenece a ningun Modelo de Dominio especifico. Pueden usarse para implementar reglas de negocio complejas que involucran multiples Modelos de Dominio. ToDo: No implementado aun.
