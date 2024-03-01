from django.contrib.auth.models import User
from utils.validator_cpf import cpf_validator
from django.forms import ValidationError
from django.db import models
import brazilcep

# Create your models here.

"""
    PerfilUsuario
        user - FK user (ou OneToOne)
        idade - Int
        data_nascimento - Date
        cpf - char
        endereco - char
        numero - char
        complemento - char
        bairro - char
        cep - Char
        cidade - char
        estado - Choices
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
"""


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'Users Profiles'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='user_profile'
    )
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    cpf = models.CharField(max_length=11)
    cep = models.CharField(max_length=8)
    adress = models.CharField(max_length=50)
    number_adress = models.CharField(max_length=5)
    complement = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(
        default='SP', max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def clean(self):
        error_messages = {}

        if not cpf_validator(self.cpf):
            error_messages['cpf'] = 'digite um cpf válido'

        if self.cep == '':
            error_messages['cep'] = 'digite um cep'
            raise ValidationError(error_messages)

        try:
            brazilcep.get_address_from_cep(int(self.cep))

        except:  # noqa: E722
            error_messages['cep'] = 'cep invalido'

        if error_messages:
            raise ValidationError(error_messages)

    def __str__(self):
        return f'{self.user.first_name} {self.user.first_name}'
