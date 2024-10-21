from django.core.management.base import BaseCommand
from classCreation_Schedules.models import Class
from embeddings_simmilarities.utils import generate_embedding


class Command(BaseCommand):
    help = 'Update embeddings for all existing teachers'

    def handle(self, *args, **kwargs):
        classes = Class.objects.all()

        for class_ in classes:
            combined_text = (
                f"Class Name: {class_.className}. "
                f"Description: {class_.description}. "
            )

            embedding = generate_embedding(combined_text)
            class_.set_embedding(embedding)
            class_.save()

        self.stdout.write(self.style.SUCCESS('Embeddings have been updated successfully.'))
