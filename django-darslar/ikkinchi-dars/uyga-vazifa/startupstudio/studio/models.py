from django.db import models

class StartupIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    market_size = models.CharField(max_length=100)
    difficulty = models.IntegerField(help_text="1-10 scale")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title