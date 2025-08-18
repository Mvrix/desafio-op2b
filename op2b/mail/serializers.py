


from rest_framework import serializers

class MailTextSerializer(serializers.Serializer):
    texto = serializers.CharField(max_length=1000, required=True)
    destinatario = serializers.EmailField(required=True)
    titulo = serializers.CharField(max_length=50, required=False, allow_blank=True)