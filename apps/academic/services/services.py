from apps.academic.models import MockGrades as Notas

def get_notas_alumno(alumno_id):
    return Notas.objects.filter(alumno_id=alumno_id)
