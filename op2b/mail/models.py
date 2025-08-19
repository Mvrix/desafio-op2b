from django.db import models

class MailSenderConfig(models.Model):
    caracters_per_line = models.IntegerField(default=40)

    def __str__(self):
        return self.name
    
class MailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    raw_text = models.TextField()
    justified_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    caracters_per_line = models.ForeignKey(MailSenderConfig, on_delete=models.CASCADE)

    def __str__(self):
        return f"Email to {self.recipient} at {self.sent_at}"