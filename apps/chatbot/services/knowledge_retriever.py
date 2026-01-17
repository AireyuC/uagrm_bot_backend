from django.db.models import Q
from pgvector.django import CosineDistance

from apps.institutional.models import KnowledgeBase, DocumentChunk
from apps.institutional.services.ingestion import get_embedding

def search_knowledge_base(query_text):
    """
    Busca información institucional mediante Búsqueda Vectorial (PDFs) e Híbrida (Legacy).
    """
    if not query_text:
        return ""

    context_str = ""

    # 1. Búsqueda Vectorial (PDFs) - Prioridad Alta
    query_embedding = get_embedding(query_text)
    if query_embedding:
        # Buscamos los 4 chunks más similares
        vector_results = DocumentChunk.objects.annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')[:4]

        if vector_results.exists():
            context_str += "INFORMACIÓN DE DOCUMENTOS OFICIALES (PDFs):\n"
            for chunk in vector_results:
                # Opcional: Filtrar por distancia si es muy irrelevante (distancia > 0.5)
                context_str += f"- Fuente: {chunk.document.title}\n  Fragmento: {chunk.chunk_text}\n\n"

    # 2. Búsqueda por Palabras Clave (Legacy KnowledgeBase) - Respaldo
    terms = query_text.split()
    q_objects = Q()
    for term in terms:
        if len(term) > 2: 
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(content__icontains=term)
            q_objects |= Q(keywords__icontains=term)
    
    if q_objects:
        keyword_results = KnowledgeBase.objects.filter(is_active=True).filter(q_objects).distinct()[:2]
        if keyword_results.exists():
            context_str += "INFORMACIÓN GENERAL (REGLAMENTOS WEB):\n"
            for item in keyword_results:
                context_str += f"- Título: {item.title}\n  Contenido: {item.content}\n\n"

    if not context_str:
        return ""
    
    return context_str
