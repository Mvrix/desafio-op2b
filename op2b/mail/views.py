from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination

from mail.serializers import MailLogSerializer, MailTextSerializer
from rest_framework.viewsets import ModelViewSet

from mail.models import MailLog, MailSenderConfig


class LogPagination(pagination.PageNumberPagination):
    page_size = 20

class MailLogView(ModelViewSet, APIView):
    serializer_class = MailLogSerializer
    pagination_class = LogPagination
    
    
    def get_queryset(self):
        return MailLog.objects.all()

class MailFormatterView(ModelViewSet, APIView):
    serializer = MailTextSerializer
    
    def get_object(self):
        try:
            return MailSenderConfig.objects.first()
        except MailSenderConfig.DoesNotExist:
            return MailSenderConfig.objects.create()

    def create(self, request):
        obj = self.get_object()
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        words = serializer.validated_data['text'].replace('\n', ' ').split()
        lines = self.formater(words, obj.caracters_per_line)
        justified_text = self.justifier(lines, obj.caracters_per_line)
        result_text = "\n".join(lines)
        justified_text = "\n".join(justified_text)

        resultado = {
            "link para abrir caixa de e-mail": f"mailto:{serializer.validated_data['recipient']}?subject={serializer.validated_data['subject']}%20Formatado&body={justified_text}",
            "texto formatado": result_text,
            "texto justificado": justified_text
            }

        MailLog.objects.create(
            recipient=serializer.validated_data['recipient'],
            subject=serializer.validated_data['subject'],
            body=result_text,
            raw_text=serializer.validated_data['text'],
            justified_text=justified_text,
            caracters_per_line=self.get_object().caracters_per_line
        )

        return Response(resultado, status=status.HTTP_200_OK)

    def partial_update(self, request):
        serializer = self.serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = self.get_object()
        obj.caracters_per_line = serializer.validated_data['caracters_per_line']
        obj.save()
        
        resultado = {
            "caracters_perline": obj.caracters_per_line,
            }
        
        return Response(resultado, status=status.HTTP_200_OK)

    def justifier(self, lines, parameter):
        justified_text = []
        for i in lines:
            spaces_faltants = parameter - (len(i))
            words = i.split()
            if len(words) == 1:
                justified_line = words[0] + ' ' * spaces_faltants
            else:
                spaces_needed = len(words) - 1
                spaces = [' ' * (1+spaces_faltants // spaces_needed + (1 if x < spaces_faltants % spaces_needed else 0)) for x in range(spaces_needed)]
                justified_line = ''.join(word + (spaces[idx] if idx < len(spaces) else '') for idx, word in enumerate(words))
            justified_text.append(justified_line)
            
        return justified_text

    def formater(self, words, parameter):
        lines = []
        atual_line = ""
        
        for word in words:
            if len(atual_line) + len(word) + 1 <= parameter:
                if atual_line:
                    atual_line += " " + word
                else:
                    atual_line = word
            else:
                lines.append(atual_line)
                atual_line = word

        return lines