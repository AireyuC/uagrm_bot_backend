from django.db import migrations, models
import django.db.models.deletion
import pgvector.django

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        pgvector.django.VectorExtension(),
        migrations.CreateModel(
            name='UploadedDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='pdfs/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Documento_Subido',
                'verbose_name_plural': 'Documentos_Subidos',
                'db_table': 'institucional_documentos',
            },
        ),
        migrations.CreateModel(
            name='DocumentChunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chunk_text', models.TextField()),
                ('chunk_index', models.IntegerField()),
                ('embedding', pgvector.django.VectorField(dimensions=1536)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chunks', to='institutional.uploadeddocument')),
            ],
            options={
                'verbose_name': 'Fragmento_de_Documento',
                'verbose_name_plural': 'Fragmentos_de_Documentos',
                'db_table': 'institucional_fragmentos',
                'indexes': [
                    pgvector.django.HnswIndex(
                        name='chunk_embedding_idx',
                        fields=['embedding'],
                        opclasses=['vector_cosine_ops'],
                    )
                ],
            },
        ),
    ]
