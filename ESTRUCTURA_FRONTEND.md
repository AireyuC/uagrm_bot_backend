# Estructura del Frontend (Implementada)

Este documento detalla la arquitectura del proyecto React + Vite, organizada por *funcionalidad* (Feature-Based) para escalar junto con el backend Django.

## 🛠 Tech Stack
- **Core**: React 18 + Vite + TypeScript.
- **Estado/Data**: Axios (HTTP) + React Context (Auth).
- **Estilos**: Tailwind CSS + Lucide React (Iconos).
- **Routing**: React Router v6.

## 📂 Árbol de Directorios Actual

```text
uagrm_bot_frontend/
├── 📂 public/
├── 📂 src/
│   ├── 📂 assets/            
│   │
│   ├── 📂 config/            
│   │   └── axios.ts          # Cliente HTTP con Interceptors (Inyecta Token)
│   │
│   ├── 📂 components/        # Componentes Reutilizables Globale
│   │   ├── ProtectedRoute.tsx # 🛡️ Bloquea rutas según Roles (Admin, Verifier, Uploader)
│   │   └── TestChatBubble.tsx # 💬 Chat flotante para pruebas (Solo Admin/Verifier)
│   │
│   ├── 📂 features/          
│   │   ├── 📂 auth/          
│   │   │   ├── services/     # authService.ts (Login/Logout, LocalStorage)
│   │   │   └── types/        # Interfaces (User, AuthResponse)
│   │   │
│   │   └── 📂 chat/          
│   │       └── services/     # chatService.ts (API /api/chat/post/)
│   │
│   ├── 📂 hooks/             
│   │   └── useAuth.ts        # Hook global para acceder al usuario y roles (isAdmin, etc.)
│   │
│   ├── 📂 layouts/
│   │   └── DashboardLayout.tsx # Sidebar dinámico según rol + Logout
│   │
│   ├── 📂 pages/             
│   │   ├── Login.tsx         # Formulario de entrada + Redirección inteligente
│   │   ├── PublicChat.tsx    # Home (Landing Page)
│   │   ├── Unauthorized.tsx  # Página 403
│   │   │
│   │   ├── 📂 admin/
│   │   │   └── AdminDashboard.tsx # Creación de usuarios (Roles)
│   │   │
│   │   ├── 📂 uploader/
│   │   │   └── UploaderDashboard.tsx # Subida de PDFs
│   │   │
│   │   └── 📂 verifier/
│   │       └── VerifierDashboard.tsx # Aprobación/Rechazo de documentos
│   │
│   ├── App.tsx               # Definición de Rutas (Public & Protected)
│   └── main.tsx              
│
├── .env                      # VITE_API_URL=http://localhost:8000
└── vite.config.ts            # Configuración de Proxy/Ports
```

## 🔐 Seguridad y Flujo de Trabajo

### 1. Autenticación
*   El usuario se loguea en `/login`.
*   El backend responde con un **Token** y los datos del usuario (incluyendo `groups`).
*   `authService` guarda el token en `localStorage`.
*   `axios.ts` intercepta todas las peticiones y añade el header `Authorization: Token ...`.

### 2. Control de Acceso (RBAC)
*   **`ProtectedRoute`**: Componente que envuelve las rutas privadas. Verifica:
    1.  Si el usuario está autenticado.
    2.  Si el usuario tiene el rol requerido (`allowedRoles`).
*   **Roles Implementados**:
    *   **Admin**: Acceso total + Gestión de Usuarios.
    *   **Verifier**: Acceso a verificar documentos + Chat de pruebas.
    *   **Uploader**: Acceso a subir documentos.

### 3. Funcionalidades Clave
*   **Chat Público (Landing)**: Informativo, redirige a WhatsApp.
*   **Test Chat Bubble**: Herramienta de desarrollo dentro del dashboard para probar el bot sin usar WhatsApp. Solo visible para Staff.
