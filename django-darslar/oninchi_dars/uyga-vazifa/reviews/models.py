from django.db import models
from utils.models import BaseModel
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(BaseModel):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,related_name="reviewer_reviews", null=True, db_index=True)
    target_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="reviews", null=True, db_index=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"Reviewer: {self.reviewer.username} | Target user: {self.target_user.username} | Rating: {self.rating}"

    class Meta:
        db_table = "reviews"
        verbose_name = "Sharx"
        verbose_name_plural = "Sharxlar"
        constraints = [
            models.UniqueConstraint(fields=["reviewer","target_user"],name='reviewer_target_user_const')
        ]
        indexes = [
            models.Index(fields=["created_at"],name='review_created_at_idx')
        ]