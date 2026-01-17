import logging
import math
import openai
from pypdf import PdfReader
from django.conf import settings
from apps.institutional.models import UploadedDocument, DocumentChunk

logger = logging.getLogger(__name__)

# Configurar OpenAI (asegúrate de que settings.OPENAI_API_KEY esté seteado)
openai.api_key = settings.OPENAI_API_KEY

def get_embedding(text):
    """Genera el embedding para un texto dado usando OpenAI."""
    text = text.replace("\n", " ")
    try:
        response = openai.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generando embedding: {e}")
        return None

def process_pdf(document_id):
    """
    Procesa un UploadedDocument:
    1. Lee el PDF
    2. Extrae texto
    3. Divide en chunks
    4. Genera embeddings
    5. Guarda DocumentChunks
    """
    try:
        doc = UploadedDocument.objects.get(id=document_id)
        logger.info(f"Procesando documento: {doc.title}")
        
        # 1. Leer PDF
        reader = PdfReader(doc.file.path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
            
        if not full_text.strip():
            logger.warning("El PDF parece estar vacío o no contiene texto extraíble.")
            return

        # 2. Chunking (Estrategia simple con overlap)
        # OpenAI recomienda chunks de ~500-1000 tokens. 
        # Aproximación: 1 token ~= 4 caracteres. 
        # Chunk size ~3000 chars, Overlap ~200 chars.
        CHUNK_SIZE = 3000
        CHUNK_OVERLAP = 200
        
        chunks = []
        text_len = len(full_text)
        start = 0
        
        while start < text_len:
            end = min(start + CHUNK_SIZE, text_len)
            chunk_content = full_text[start:end]
            chunks.append(chunk_content)
            
            # Mover el cursor, retrocediendo un poco (overlap) excepto si ya acabamos
            if end == text_len:
                break
            start = end - CHUNK_OVERLAP

        # 3. Eliminar chunks anteriores si existen (re-procesamiento)
        doc.chunks.all().delete()
        
        # 4. Generar Embeddings y Guardar
        chunk_objects = []
        for i, text_chunk in enumerate(chunks):
            embedding = get_embedding(text_chunk)
            if embedding:
                chunk_obj = DocumentChunk(
                    document=doc,
                    chunk_text=text_chunk,
                    chunk_index=i,
                    embedding=embedding
                )
                chunk_objects.append(chunk_obj)
        
        # Bulk create es mucho más eficiente
        if chunk_objects:
            DocumentChunk.objects.bulk_create(chunk_objects)
            logger.info(f"Guardados {len(chunk_objects)} chunks para {doc.title}")
            
    except UploadedDocument.DoesNotExist:
        logger.error(f"Documento ID {document_id} no encontrado.")
    except Exception as e:
        logger.error(f"Error procesando PDF ({document_id}): {e}")
