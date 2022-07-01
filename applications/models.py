from django.db import models
from django.contrib.auth.models import User


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    status = models.CharField(default="Created", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
        ]

    def get_data(self):
        return {"id": self.id, "price": self.price, "status": self.status, "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")}

    def __str__(self):
        return self.user.username + " " + str(self.price)
