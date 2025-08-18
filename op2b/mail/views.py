from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MailTextSerializer



class MailFormatter(APIView):
    serializer = MailTextSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        palavras = serializer.validated_data['texto'].replace('\n', ' ').split()
        linhas = []
        linha_atual = ""
        result_text = ""
        formated_text = ""
        
        for palavra in palavras:
            if len(linha_atual) + len(palavra) + 1 <= 40:
                formated_text += palavra + " "
                if linha_atual:
                    linha_atual += " " + palavra
                else:
                    linha_atual = palavra
            else:
                linhas.append(linha_atual)
                linha_atual = palavra

        result_text = "\n".join(linhas)

        resultado = {
            "link para abrir caixa de e-mail": f"mailto:{serializer.validated_data['destinatario']}?subject={serializer.validated_data['titulo']}%20Formatado&body={result_text}",
            "texto formatado": result_text,
            "texto justificado": formated_text
            }

        return Response(resultado, status=status.HTTP_200_OK)