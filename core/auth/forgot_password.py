from django.core.mail import send_mail
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


User = get_user_model()

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def ForgotPasswordUser(request):
    email = request.data.get("email")

    if not email:
        return Response({"message": "Email é necessario!"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except:
        return Response({"message": "Usuário não encontrado com esse email"}, status=status.HTTP_404_NOT_FOUND)
    
    reset_code = get_random_string(length=6, allowed_chars='1234567890')
    user.reset_code = reset_code
    user.save()

    subject = 'Redefinição de senha'
    from_email = 'gabriellima2803@gmail.com'
    to_email = [user.email]

    html_content = render_to_string('../templates/html-email/password_reset_email.html', {'reset_code': reset_code, 'user': user})

    send_mail(
        subject,
        '',
        from_email,
        to_email,
        fail_silently=False,
        html_message=html_content,
    )

    return Response({"message": "Código de redefinição enviado por e-mail."}, status=status.HTTP_200_OK)