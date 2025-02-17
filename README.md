# NovaPass: Aplicación de Gestión Segura de Contraseñas

## Descripción General

NovaPass es una aplicación local de gestión de contraseñas desarrollada con Python, diseñada para ayudar a los usuarios a almacenar y administrar sus contraseñas de servicios con un cifrado robusto. La aplicación proporciona una interfaz fácil de usar para guardar, recuperar y gestionar contraseñas de manera segura.

## Características

### 🔐 Cifrado Avanzado
- Utiliza cifrado AES-256 para proteger contraseñas almacenadas
- Genera y administra una clave de cifrado única para cada instalación
- Cifra archivos CSV completos, no solo entradas individuales

### 🖥️ Interfaz de Usuario
- Construida con Flet para una aplicación de escritorio moderna y receptiva
- Experiencia de usuario limpia e intuitiva con múltiples páginas:
  - Pantalla de bienvenida
  - Registro e inicio de sesión de usuario
  - Panel de gestión de contraseñas
  - Funcionalidad de búsqueda para recuperación rápida de contraseñas

### 🛡️ Aspectos de Seguridad
- Validación de correo electrónico durante el registro
- Confirmación de contraseña durante el registro
- Almacenamiento cifrado que previene la exposición de contraseñas en texto plano
- Almacenamiento y recuperación de contraseñas por usuario

## Tecnologías Utilizadas

- **Framework**: Flet
- **Cifrado**: PyCryptodome (Cifrado AES)
- **Manejo de Datos**: Pandas
- **Lenguaje**: Python

## Mecanismo de Cifrado

NovaPass implementa un sistema de cifrado sofisticado:

1. **Generación de Claves**:
   - Genera una clave de cifrado única de 32 bytes
   - Almacena la clave en un archivo separado (`encryption_key.key`)
   - Crea una nueva clave si no se encuentra ninguna existente

2. **Proceso de Cifrado**:
   - Convierte datos a JSON
   - Genera un vector de inicialización (IV) único
   - Usa AES en modo de Encadenamiento de Bloques de Cifrado (CBC)
   - Rellena datos para garantizar tamaños de bloque consistentes
   - Codifica los datos cifrados en Base64

3. **Proceso de Descifrado**:
   - Invierte los pasos de cifrado
   - Maneja errores de descifrado de manera elegante
   - Restaura la estructura de datos original

## Instalación

### Requisitos Previos
- Python 3.8+
- Bibliotecas:
  ```bash
  pip install flet pandas pycryptodome
  ```

### Ejecutar la Aplicación
```bash
python interface.py
```

## Uso

1. Inicie la aplicación
2. Registre una nueva cuenta o inicie sesión
3. Añada contraseñas para diversos servicios
4. Busque y administre sus contraseñas almacenadas

## Consideraciones de Seguridad

- Contraseñas cifradas localmente
- Sin almacenamiento en la nube ni transmisión externa
- Cifrado único por instalación
- Datos sensibles nunca almacenados en texto plano

## Mejoras Futuras

- Implementar verificador de fortaleza de contraseñas
- Añadir autenticación de dos factores
- Crear funcionalidad de exportación/importación
- Mejorar búsqueda y capacidades de filtrado

## Contribución

¡Las contribuciones son bienvenidas! No dude en enviar una solicitud de extracción.


## Descargo de Responsabilidad

Este es un proyecto educativo. Aunque es seguro, no debe considerarse un reemplazo de gestores de contraseñas profesionales.