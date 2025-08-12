## 🚀 Features

- **Real-time Stock Monitoring**: Fetches live stock prices every 15 minutes using APScheduler
- **Smart Alerts**: Two types of alerts (Threshold & Duration-based)
- **Email Notifications**: Automated email alerts when conditions are met
- **JWT Authentication**: Secure user authentication and authorization
- **RESTful API**: Complete REST API with Swagger documentation
- **Admin Dashboard**: Django admin interface for system management

## 📊 Alert Types

### 1. Threshold Alerts
Triggers immediately when stock price meets the condition:
\`\`\`json
{
  "stock": 1,
  "alert_type": "threshold",
  "operator": ">",
  "threshold_price": "200.00"
}
\`\`\`

### 2. Duration Alerts
Triggers when condition persists for specified duration:
\`\`\`json
{
  "stock": 1,
  "alert_type": "duration",
  "operator": "<",
  "threshold_price": "150.00",
  "duration_hours": 2
}
### Quick Start

1. **Clone the repository**
\`\`\`bash
git clone https://github.com/FatMAnsour/Stock-Alert.git
cd stock-alert-system
\`\`\`

2. **Create virtual environment**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Environment setup**
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

5. **Database setup**
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
\`\`\`

6. **Initialize stocks**
\`\`\`bash
python manage.py init_stocks
\`\`\`

7. **Run the server**
\`\`\`bash
python manage.py runserver
\`\`\`

## 📚 API Documentation

### Base URL
\`\`\`
http://localhost:8000/api/
\`\`\`

### Swagger Documentation
- **Swagger UI**: http://localhost:8000/swagger/
## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| \`SECRET_KEY\` | Django secret key | Required |
| \`DEBUG\` | Debug mode | \`True\` |
| \`ALLOWED_HOSTS\` | Allowed hosts | \`localhost,127.0.0.1\` |
| \`EMAIL_HOST_USER\` | Gmail address | Required for emails |
| \`EMAIL_HOST_PASSWORD\` | Gmail app password | Required for emails |
| \`STOCK_API_KEY\` | Twelve Data API key | \`demo\` |
