import logging
import math
import nest_asyncio
nest_asyncio.apply()

import openai
# from pypdf import PdfReader  # Removed in favor of LlamaParse
from llama_parse import LlamaParse
from llama_index.core.node_parser import MarkdownNodeParser
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

def extract_text_from_pdf(file_path):
    """
    Usa LlamaParse para extraer texto optimizado (Markdown) de PDFs complejos.
    """
    try:
        parser = LlamaParse(
            api_key=settings.LLAMA_CLOUD_API_KEY,
            result_type="markdown",  # Clave: Esto reconstruye las tablas perfectamente
            language="es",  # Opcional, ayuda con el español
            verbose=True
        )

        # LlamaParse procesa el archivo
        documents = parser.load_data(file_path)
        return documents
        
        # Unir todas las páginas en un solo texto (YA NO SE USA, RETORNAMOS DOCS)
        # full_text = "\n\n".join([doc.text for doc in documents])
        # return full_text
    except Exception as e:
        logger.error(f"Error extracting text with LlamaParse: {e}")
        raise e

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
        
        # 1. Leer PDF con LlamaParse
        # reader = PdfReader(doc.file.path)
        # full_text = ""
        # for page in reader.pages:
        #     full_text += page.extract_text() + "\n"
        
        # 1. Leer PDF con LlamaParse y obtener Documentos
        documents = extract_text_from_pdf(doc.file.path)
            
        if not documents:
            logger.warning("El PDF parece estar vacío o no contiene documentos.")
            return

        # 2. Chunking inteligente con MarkdownNodeParser (LlamaIndex)
        # Esto respeta la estructura de Markdown (tablas, headers)
        parser = MarkdownNodeParser()
        nodes = parser.get_nodes_from_documents(documents)
        
        chunks = [node.text for node in nodes]

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
