from django.core.management.base import BaseCommand
from users.models import Teacher
from embeddings_simmilarities.utils import generate_embedding


class Command(BaseCommand):
    help = 'Update embeddings for all existing teachers'

    def handle(self, *args, **kwargs):
        teachers = Teacher.objects.all()

        for teacher in teachers:
            combined_text = (
                f"Description: {teacher.description}. "
                f"Specialities: {teacher.specialities}. "
                f"Biography: {teacher.biography}. "
                f"Mode: {teacher.mode}. "
                f"Ciudad: {teacher.ciudad}. "
                f"Availability: {teacher.availability}. "
                f"Average rating: {teacher.average_rating}."
            )

            embedding = generate_embedding(combined_text)
            teacher.set_embedding(embedding)
            teacher.save()

        self.stdout.write(self.style.SUCCESS('Embeddings have been updated successfully.'))
