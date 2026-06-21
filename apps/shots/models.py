import os
from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Shot(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='shots/')
    preview = models.ImageField(upload_to='shots/previews/', null=True, blank=True)

    # Зв'язки
    tags = models.ManyToManyField(Tag, related_name='shots', blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shots'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Робота (Shot)'
        verbose_name_plural = 'Роботи (Shots)'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image and not self.preview:
            self.generate_preview()
        super().save(*args, **kwargs)

    def generate_preview(self):
        try:
            img = Image.open(self.image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((800, 600), Image.Resampling.LANCZOS)

            temp_thumb = BytesIO()
            img.save(temp_thumb, format='JPEG', quality=80)
            temp_thumb.seek(0)

            filename = os.path.basename(self.image.name)
            name, _ = os.path.splitext(filename)
            preview_filename = f"{name}_preview.jpg"

            self.preview.save(preview_filename, ContentFile(temp_thumb.read()), save=False)
        except Exception as e:
            print(f"Помилка створення прев'ю: {e}")