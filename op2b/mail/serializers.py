


from rest_framework import serializers

class MailTextSerializer(serializers.Serializer):
    texto = serializers.CharField(max_length=1000, required=True)