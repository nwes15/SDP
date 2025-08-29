from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from .models import RegistroPonto, Motorista, Veiculo, Mercado

class RegistroPontoForm(forms.ModelForm):
    class Meta:
        model = RegistroPonto
        fields = [
            'foto_odometro', 
            'foto_combustivel', 
            'km_odometro', 
            'nivel_combustivel', 
            'observacoes'
        ]
        widgets = {
            'foto_odometro': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'capture': 'environment',
                'required': True
            }),
            'foto_combustivel': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'capture': 'environment',
                'required': True
            }),
            'km_odometro': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 125000',
                'min': '0'
            }),
            'nivel_combustivel': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 80',
                'min': '0',
                'max': '100'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações opcionais...'
            })
        }
    
    def clean_foto_odometro(self):
        foto = self.cleaned_data.get('foto_odometro')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('A foto não pode ser maior que 5MB.')
        return foto
    
    def clean_foto_combustivel(self):
        foto = self.cleaned_data.get('foto_combustivel')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('A foto não pode ser maior que 5MB.')
        return foto

class MotoristaForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome de usuário'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
    )
    
    class Meta:
        model = Motorista
        fields = [
            'nome_completo', 
            'cpf', 
            'telefone', 
            'valor_dia', 
            'veiculo', 
            'mercado'
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do motorista'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': '000.000.000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
                'data-mask': '(00) 00000-0000'
            }),
            'valor_dia': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'veiculo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mercado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veiculo'].queryset = Veiculo.objects.filter(ativo=True)
        self.fields['mercado'].queryset = Mercado.objects.filter(ativo=True)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf_limpo) != 11:
            raise ValidationError('CPF deve ter 11 dígitos.')
        
        # Verifica se não é uma sequência de números iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            raise ValidationError('CPF inválido.')
        
        # Verifica se já existe
        if Motorista.objects.filter(cpf=cpf).exists():
            raise ValidationError('Este CPF já está cadastrado.')
        
        return cpf
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('As senhas não coincidem.')
        
        return cleaned_data

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234 ou ABC1D23',
                'style': 'text-transform: uppercase;'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Honda Civic'
            }),
            'cor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Branco'
            })
        }
    
    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa:
            placa = placa.upper().replace('-', '').replace(' ', '')
            # Aceita placa antiga (ABC1234) ou Mercosul (ABC1D23)
            padrao_antigo = r'^[A-Z]{3}[0-9]{4}$'
            padrao_mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'
            if not (re.match(padrao_antigo, placa) or re.match(padrao_mercosul, placa)):
                raise ValidationError('Formato de placa inválido. Use ABC-1234 ou ABC1D23')
            
            # Reformatar: antigo com hífen, Mercosul sem hífen
            if re.match(padrao_antigo, placa):
                placa_formatada = f"{placa[:3]}-{placa[3:]}"
            else:
                placa_formatada = placa  # Mercosul
            
            # Verificar se já existe
            if Veiculo.objects.filter(placa=placa_formatada).exists():
                raise ValidationError('Esta placa já está cadastrada.')
            
            return placa_formatada
        return placa

class MercadoForm(forms.ModelForm):
    class Meta:
        model = Mercado
        fields = ['nome', 'endereco', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do mercado'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
                'data-mask': '(00) 00000-0000'
            })
        }

class RelatorioForm(forms.Form):
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    motorista = forms.ModelChoiceField(
        queryset=Motorista.objects.filter(ativo=True),
        required=False,
        empty_label='Todos os motoristas',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    veiculo = forms.ModelChoiceField(
        queryset=Veiculo.objects.filter(ativo=True),
        required=False,
        empty_label='Todos os veículos',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_inicio > data_fim:
                raise ValidationError('Data início não pode ser maior que data fim.')
        
        return cleaned_data