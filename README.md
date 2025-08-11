###  E-commerce Testing Suite (COMPLETO)

UI + API + Database Testing Framework para aplicación e-commerce usando Python + Selenium + Pytest + Flask + Sqlite3

## Caracteristicas: 
    [x] UI Testing con Page Object Model (POM)
    [x] Configuracion flexible con variables de entorno
    [x] Screenshots automaticos en caso de fallos
    [x] Reportes HTML detallados
    [x] Tests parametrizados y organizados por marcadores
    [x] Setup/Teardown automatico

## Stack Tecnologico
* Python 4.1+
* Selenium WebDriver 4.x
* Pytest para framework de testing
* WebDriver Manager para gestion automatica de drivers
* Faker para generacion de datos de prueba




## Estructura del proyecto

    E-COMMERCE_TESTING_SUITE/
    ├── api/
    |   ├── base_api.py
    |   ├── mock_server.py     # Mock API para simular endpoints
    |   ├── endpoints/
    |   |   ├── users_api.py        # 
    |   |   ├── products_api.py     #
    |   |   ├── orders_api.py       #
    ├── pages/                 # Page Object Model
    │   ├── base_page.py       # Clase base para páginas
    │   ├── login_page.py      # Página de login  
    │   ├── products_page.py   # Página de productos
    │   ├── cart_page.py       # Página del carrito
    │   └── checkout_page.py   # Página del pago (checkout)
    ├── tests/                 # Tests organizados
    │   ├── ui/                # UI Tests
    │   │   ├── test_login.py      
    │   │   ├── test_products.py    
    │   │   ├── test_cart_flow.py   
    │   │   └── test_checkout.py    
    │   ├── api/              
    │   │   ├── test_orders_api.py
    │   │   ├── test_products_api.py
    │   │   └── test_users_api.py       
    │   └── integration/                # Integration Tests
    │   │   └── test_db_validation.py
    ├── utils/                # Utilidades
    │   ├── config.py         # Configuración
    │   └── helpers.py        # Funciones auxiliares
    │   └── db_utils          # Funciones auxiliares
    ├── data/                 # Datos de prueba
    ├── reports/              # Reportes generados
    ├── screenshots/          # Screenshots de fallos
    ├── conftest.py           # Configuración pytest
    └── ecommerce_test.db     # DB generada automaticamente




## Setup e Instalacion 

    1. Clonar Repositorio
    git clone <tu-repo-url>
    cd ecommerce-testing-suite

    2. Crear entorno virtual
    python -m venv venv

    #Windows
    venv\Scripts\activate

    #Linux/Mac
    source venv/bin/activate

    3. Instalar Dependencias
    pip install -r requirements.txt

    4. Configurar Variables de Entorno
    Crear archivo '.env' en el directorio raiz
    BASE_URL=https://www.saucedemo.com
    BROWSER=chrome
    IMPLICIT_WAIT=10
    EXPLICIT_WAIT=20

    5. Setup del Mock API Server
    python api/mock_server.py
    - Se deberia ver:
    * Running on http://127.0.0.1:5000
    * Debug mode: on


## Ejecutar Tests
Los tests deben ejecutarse en una terminal diferente a la del Mock API Server

### Todos los Tests
    pytest -v

### Tests especificos por marcador
#### Solo tests de smoke
    pytest -m smoke -v

#### Solo tests de regresión
    pytest -m regression -v

#### Solo tests de UI
    pytest -m ui -v

#### Solo tests de API
    pytest -m api -v

#### Solo tests de DB validation
    pytest -m integration -v

### Tests específicos por archivo
#### Solo tests de login
    pytest tests/ui/test_login.py -v

#### Solo tests de productos
    pytest tests/ui/test_products.py -v

#### Test específico
    pytest tests/ui/test_login.py::TestLogin::test_successful_login_standard_user -v

### Con reporte HTML
    pytest -v --html=reports/report.html --self-contained-html

### Tests en paralelo (instalar pytest-xdist)
    pip install pytest-xdist
    pytest -v -n 2  # Ejecutar con 2 procesos paralelos



## Reportes y Logs

Reportes HTML: Se generan en reports/report.html
Screenshots: Se guardan automáticamente en screenshots/ cuando fallan tests
Logs: Output detallado en consola con -v flag


### Casos de Prueba Incluidos
#### Login Tests (test_login.py)

✅ Login exitoso con usuario válido

✅ Login con credenciales inválidas

✅ Login con usuario bloqueado

✅ Validación de campos requeridos

✅ Verificación de elementos de página

#### Products Tests (test_products.py)

✅ Carga correcta de página de productos

✅ Agregar producto individual al carrito

✅ Agregar múltiples productos

✅ Navegación al carrito

✅ Funcionalidad de logout

✅ Tests parametrizados para diferentes productos

#### Cart Flow Tests (test_cart_flow.py)

✅ Visualización de productos en carrito

✅ Remover productos del carrito

✅ Continuar comprando desde carrito

#### Checkout Tests (test_checkout.py)

✅ Verificacion de pago exitoso

✅ Tratar de pagar faltando el nombre

✅ Tratar de pagar faltando el apellido

✅ Tratar de pagar faltando el codigo postal

✅ Cancelar checkout

✅ Volver a la pagina de productos despues de un pago exitoso

#### API Testing

✅ CRUD Usuarios: Crear, obtener, validar duplicados

✅ Gestión Productos: Listar, actualizar stock

✅ Procesamiento Órdenes: Crear órdenes, validar stock

✅ Validaciones Respuesta: Status codes, JSON schemas

#### Database Validations

✅ Usuario creado en DB: Verificar datos completos

✅ Stock después de compra: Tracking en tiempo real

✅ Orden guardada: Validar estructura completa

✅ Rollback en fallos: Stock no cambia si orden falla


#### Próximos Pasos

 - API Testing con requests
 - Database validations
 - CI/CD con GitHub Actions
 - Docker containerización
 - Allure reporting
 - Performance testing básico




## Contacto
* Autor: Laureano Gabriel Carranza Guiñazú
* Email: laureano.piano.2008@gmail.com
* LinkedIn: [https://www.linkedin.com/in/laureano-carranza]
* GitHub: [Onaeru]