from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MailTextSerializer



class MailFormatter(APIView):
    serializer = MailTextSerializer

    def post(self, request):
        serializers.is_valid(raise_exception=True)
        texto = serializers.validated_data['texto']
        
        print("rexec", texto)

        resultado = {"texto_formatado": texto}

        return Response(resultado, status=status.HTTP_200_OK)