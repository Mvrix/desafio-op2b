# 📌 OP2B

Sistema de consumo de API para **formatação e justificação de textos**.\
O sistema recebe um texto de entrada, processa e retorna:\
- O texto formatado com limite de caracteres por linha.\
- O texto justificado (alinhamento ajustado automaticamente).\
- Link direto para abertura do cliente de e-mail com o texto formatado.

------------------------------------------------------------------------

## 🚀 Tecnologias utilizadas

-   **Python 3.10+**
-   **Django 4.2.7**
-   **Django REST Framework**
-   **SQLite3** (banco padrão do projeto)

------------------------------------------------------------------------

## ⚙️ Instalação do sistema OP2B

### Pré-requisitos

-   Python 3.10.12 ou superior\
-   IDE Python (VS Code recomendado)

### Passo a passo

``` bash
# Clonar o repositório
https://github.com/Mvrix/desafio-op2b.git
cd op2b

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python manage.py makemigrations
python manage.py migrate
```

> 💡 Se quiser iniciar um banco **limpo** sem dados, basta deletar o
> arquivo `db.sqlite3` antes de rodar as migrações.

------------------------------------------------------------------------

## 📖 Como utilizar a solução

O sistema expõe endpoints via **API REST**.

### Exemplo de uso - Formatação de texto

Endpoint:

    POST /mailformatter/

Payload esperado:

``` json
{
  "recipient": "teste@email.com",
  "subject": "Meu texto",
  "text": "Aqui vai o texto que será formatado e justificado automaticamente"
}
```

Resposta:

``` json
{
  "link para abrir caixa de e-mail": "mailto:teste@email.com?subject=Meu%20texto%20Formatado&body=...",
  "texto formatado": "Aqui vai o texto ...",
  "texto justificado": "Aqui   vai   o   texto ..."
}
```

### Configuração do limite de caracteres por linha

Endpoint:

    PATCH /mailformatter/

Payload:

``` json
{
  "caracters_per_line": 50
}
```

Resposta:

``` json
{
  "caracters_perline": 50
}
```

------------------------------------------------------------------------

## 🔍 Desafios e soluções implementadas

1.  **Formatação de texto em linhas**
    -   Problema: garantir que o texto respeite o limite de caracteres.\
    -   Solução: função `formater` quebra o texto em linhas mantendo
        palavras inteiras.
2.  **Justificação automática**
    -   Problema: alinhar o texto em blocos, distribuindo espaços
        uniformemente.\
    -   Solução: função `justifier` calcula espaços extras e distribui
        proporcionalmente entre as palavras.
3.  **Configuração dinâmica do limite de caracteres**
    -   Problema: permitir ao usuário mudar a largura máxima de linha.\
    -   Solução: criado modelo `MailSenderConfig` para armazenar a
        configuração.
4.  **Histórico de formatações**
    -   Problema: registrar requisições para auditoria e reuso.\
    -   Solução: modelo `MailLog` salva todas as entradas e saídas.

------------------------------------------------------------------------

## ⚠️ Tratamento de erros e exceções

-   **Texto vazio**: retorna erro `400 Bad Request`.\
-   **E-mail inválido**: `400 Bad Request` (validação automática do
    Django).\
-   **Configuração ausente**: sistema cria automaticamente uma instância
    padrão de `MailSenderConfig`.\
-   **Palavra maior que limite de caracteres**: atualmente quebra a
    palavra em uma linha isolada (ponto de melhoria futura).

------------------------------------------------------------------------

## 🛠️ Estrutura do projeto

    op2b/
    │── core/
    	├── asgi.py
    	├── settings.py
    	├── urls.py
    	├── wsgi.py
    │── mail/
    │   ├── models.py        # Modelos MailLog e MailSenderConfig
    │   ├── views.py         # Views e lógica principal de formatação
    │   ├── serializers.py   # Serializers DRF
    │── db.sqlite3           # Banco SQLite
    │── manage.py
    │── requirements.txt
    │── README.md

------------------------------------------------------------------------

## 📌 Próximos passos (melhorias futuras)

-   Implementar **testes unitários** para validar as funções `formater`
    e `justifier`.\
-   Tratar casos de **palavras maiores que o limite de caracteres** com
    quebra automática.\
-   Melhorar a API para permitir múltiplos destinatários.\
-   Adicionar suporte a outros bancos (PostgreSQL, MySQL).