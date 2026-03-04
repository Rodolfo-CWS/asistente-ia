#!/bin/bash

echo "🚀 Configurando Asistente IA Personal..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instala Python 3.8+"
    exit 1
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Verificar .env
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita .env con tus API keys:"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - TWILIO_ACCOUNT_SID"
    echo "   - TWILIO_AUTH_TOKEN"
    echo "   - DATABASE_URL"
    echo ""
    read -p "Presiona Enter cuando hayas configurado .env..."
fi

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python -c "from main import engine, Base; Base.metadata.create_all(bind=engine)"

echo ""
echo "✅ Setup completo!"
echo ""
echo "Para iniciar el servidor:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Para exponer con ngrok:"
echo "  ngrok http 8000"
