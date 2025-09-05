# Sistema de Controle de Ponto para Motoristas

Hospedado: https://sdp.cloudwesns.com.br/

Para testes sem clonar:

User: user.teste

Senha: Aa123456@

Sistema web responsivo desenvolvido em Django para controle de ponto de motoristas de entrega, com captura obrigatória de fotos do odômetro e combustível.

## 🚀 Características

- **Interface responsiva** - Funciona perfeitamente em celulares e tablets
- **Captura de fotos obrigatória** - Acesso direto à câmera, sem galeria
- **Marca d'água automática** - Data/hora nas fotos para evitar fraudes
- **Controle de acesso** - Admin e motoristas com permissões diferentes
- **Relatórios personalizados** - Filtros por período, motorista ou veículo
- **Exportação Excel** - Relatórios exportáveis para planilhas
- **Design moderno** - Interface azul e laranja, limpa e profissional

## 📱 Funcionalidades

### Para Motoristas:
- ✅ Registro de entrada com foto do odômetro e combustível
- ✅ Registro de saída com mesmas informações
- ✅ Dashboard com resumo do dia
- ✅ Histórico de registros pessoais
- ✅ Interface otimizada para celular

### Para Administradores:
- 👥 Gerenciamento completo de motoristas
- 🚗 Cadastro e controle de veículos
- 🏪 Gerenciamento de mercados
- 📊 Dashboard com estatísticas em tempo real
- 📈 Relatórios personalizados com filtros
- 📤 Exportação de dados em Excel
- 👁️ Visualização de todas as fotos e registros

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passo a passo

1. **Clone ou baixe o projeto**
```bash
git clone https://github.com/nwes15/SDP.git
cd sistema-ponto
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Crie as pastas necessárias**
```bash
mkdir media
mkdir media/registros
mkdir logs
mkdir static
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

8. **Acesse o sistema**
- Sistema principal: https://sdp.cloudwesns.com.br/
- Admin Django: https://sdp.cloudwesns.com.br/django-admin

## 📂 Estrutura do Projeto

```
SDP
├── sistema_ponto/          # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ponto/                  # App principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Lógica das páginas
│   ├── forms.py           # Formulários
│   ├── urls.py            # URLs da app
│   └── admin.py           # Configuração admin
├── templates/ponto/        # Templates HTML
│   ├── base.html          # Template base
│   ├── login.html         # Página de login
│   ├── motorista_dashboard.html
│   ├── admin_dashboard.html
│   ├── registrar_ponto.html
│   └── admin/             # Templates administrativos
├── media/                 # Uploads (fotos)
├── static/                # Arquivos estáticos
├── logs/                  # Logs do sistema
└── requirements.txt       # Dependências
```

## 💾 Modelos de Dados

### Mercado
- Nome, endereço, telefone
- Status ativo/inativo

### Veículo  
- Placa, modelo, cor
- Status ativo/inativo

### Motorista
- Dados pessoais (nome, CPF, telefone)
- Valor por dia trabalhado
- Veículo e mercado vinculados
- Usuário Django associado

### RegistroPonto
- Tipo (entrada/saída)
- Data/hora automática
- Fotos do odômetro e combustível
- KM e nível de combustível
- Observações opcionais

## 🔧 Configuração Inicial

### 1. Cadastrar Mercados
Acesse o admin e cadastre os mercados onde os motoristas trabalham.

### 2. Cadastrar Veículos  
Cadastre os veículos com placa, modelo e cor.

### 3. Cadastrar Motoristas
Para cada motorista:
- Crie um usuário no Django
- Associe aos dados pessoais
- Defina veículo e mercado
- Configure valor por dia

### 4. Configurar Permissões
- **Admin**: `is_staff = True` ou `is_superuser = True`
- **Motorista**: usuário comum associado ao modelo Motorista

## 📊 Como Usar

### Fluxo do Motorista:
1. **Login** com usuário e senha
2. **Dashboard** mostra status do dia
3. **Registrar Entrada**:
   - Fotografar odômetro e combustível
   - Informar KM e percentual de combustível
   - Confirmar registro
4. **Registrar Saída** (mesmo processo)

### Fluxo do Admin:
1. **Dashboard** com visão geral
2. **Gerenciar** motoristas, veículos e mercados
3. **Relatórios** personalizados por período
4. **Exportar** dados em Excel
5. **Visualizar** fotos e detalhes dos registros

## 🔒 Segurança

- ✅ Autenticação obrigatória
- ✅ Permissões por tipo de usuário
- ✅ Fotos com marca d'água de data/hora
- ✅ Captura direta da câmera (sem galeria)
- ✅ Validações de dados
- ✅ CSRF Protection
- ✅ Upload limitado a 5MB por foto

## 📱 Responsividade

O sistema foi desenvolvido com **Bootstrap 5** e é totalmente responsivo:
- ✅ Funciona em smartphones
- ✅ Funciona em tablets  
- ✅ Funciona em desktops
- ✅ Interface otimizada para toque
- ✅ Câmera nativa em dispositivos móveis

## 🎨 Design

**Paleta de Cores:**
- Azul principal: `#2563eb`
- Laranja destaque: `#f97316` 
- Fundo branco: `#ffffff`
- Textos escuros: `#1f2937`

**Características visuais:**
- Cards com sombras suaves
- Botões com animações hover
- Icons do Font Awesome
- Typography moderna
- Gradientes sutis

## 🚀 Deploy em Produção

### Preparação:
1. Configure `DEBUG = False`
2. Defina `ALLOWED_HOSTS`
3. Configure banco PostgreSQL (recomendado)
4. Configure servidor de arquivos estáticos
5. Configure SSL/HTTPS

### Variáveis de Ambiente:
```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura
DATABASE_URL=postgres://usuario:senha@host:porta/database
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### Comandos de Deploy:
```bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn sistema_ponto.wsgi:application
```

## 🔧 Manutenção

### Backup Regular:
```bash
python manage.py dumpdata > backup.json
```

### Limpeza de Logs:
```bash
# Limpar logs antigos (> 30 dias)
find logs/ -name "*.log" -mtime +30 -delete
```

### Monitoramento:
- Verifique espaço em disco (fotos)
- Monitore logs de erro
- Backup da base de dados

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `logs/sistema_ponto.log`
2. Consulte a documentação do Django
3. Verifique as permissões de arquivos/pastas

## 📄 Licença

Este projeto foi desenvolvido para uso interno. Todos os direitos reservados.
