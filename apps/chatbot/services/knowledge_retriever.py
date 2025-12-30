from django.db.models import Q
from apps.institutional.models import KnowledgeBase

def search_knowledge_base(query_text):
    """
    Busca información institucional relevante basada en el texto de consulta.
    Retorna un string con la información encontrada o vacío.
    """
    if not query_text:
        return ""

    # Dividimos la consulta en palabras para buscar coincidencias parciales
    # Esto es una búsqueda simple. En producción se usaría Vector Search (Embeddings).
    terms = query_text.split()
    
    # 2. Construir filtro dinámico (OR) para buscar CUALQUIER palabra
    q_objects = Q()
    for term in terms:
        # Ignoramos palabras muy cortas (conectores) para reducir ruido
        if len(term) > 2: 
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(content__icontains=term)
            q_objects |= Q(keywords__icontains=term)

    # 3. Filtrar
    if not q_objects:
         return ""

    results = KnowledgeBase.objects.filter(is_active=True).filter(q_objects).distinct()[:3]

    if not results.exists():
        return ""

    context_str = "INFORMACIÓN INSTITUCIONAL (REGLAMENTOS/FECHAS):\n"
    for item in results:
        context_str += f"- Título: {item.title}\n  Contenido: {item.content}\n\n"
    
    return context_str
