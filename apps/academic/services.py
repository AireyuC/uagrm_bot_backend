from .models import Notas

def get_notas_alumno(alumno_id):
    return Notas.objects.filter(alumno_id=alumno_id)
