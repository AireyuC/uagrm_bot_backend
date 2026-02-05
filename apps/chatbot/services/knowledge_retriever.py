from django.db.models import Q
from pgvector.django import CosineDistance

from apps.institutional.models import DocumentChunk
from apps.institutional.services.ingestion import get_embedding

def search_knowledge_base(query_text, user_role='public'):
    """
    Busca información institucional mediante Búsqueda Vectorial (PDFs).
    - user_role='public': Solo ve 'public'.
    - user_role='student': Ve 'public' Y 'student'.
    """
    if not query_text:
        return ""

    context_str = ""

    # 1. Definir niveles permitidos
    niveles_permitidos = ['public']
    
    # Lógica de herencia de permisos
    if user_role == 'student':
        niveles_permitidos.append('student')
        
    elif user_role == 'teacher':
        niveles_permitidos.append('teacher')
        niveles_permitidos.append('staff') # El docente ve lo suyo Y lo compartido
        
    elif user_role == 'admin':
        niveles_permitidos.append('admin')
        niveles_permitidos.append('staff') # El admin ve lo suyo Y lo compartido

    # 2. Búsqueda Vectorial (PDFs) - Prioridad Alta
    query_embedding = get_embedding(query_text)
    if query_embedding:
        # Buscamos los 4 chunks más similares FILTRANDO por permiso
        vector_results = DocumentChunk.objects.filter(
            document__access_level__in=niveles_permitidos
        ).annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')[:4]

        if vector_results.exists():
            context_str += "INFORMACIÓN DE DOCUMENTOS OFICIALES (PDFs):\n"
            for chunk in vector_results:
                # Opcional: Filtrar por distancia si es muy irrelevante (distancia > 0.5)
                context_str += f"- Fuente: {chunk.document.title}\n  Fragmento: {chunk.chunk_text}\n\n"

    if not context_str:
        return ""
    
    return context_str
