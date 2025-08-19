


from rest_framework import serializers

from mail.models import MailLog

class MailTextSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1000, required=True)
    recipient = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=50, required=False, allow_blank=True)
    caracters_per_line = serializers.IntegerField(min_value=10, max_value=100, required=False)
    
    class Meta:
        model = MailLog
        fields = ['text', 'recipient', 'subject', 'caracters_per_line']
        
class MailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailLog
        fields = ["id", "recipient", "subject", "body", "raw_text", "justified_text", "sent_at", "date", "caracters_per_line"]