# AHAII Backend API

African Health AI Infrastructure Index - Backend API Server

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual configuration
nano .env
```

### 2. Start the Server
```bash
# Simple start (development mode)
./start_backend.sh

# Production mode
./start_backend.sh production

# Custom host/port
./start_backend.sh development localhost 8080
```

### 3. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Countries API**: http://localhost:8000/api/countries/

## 📋 Requirements

- Python 3.8+
- pip or pip3
- Virtual environment (created automatically)
- Supabase account and project (for database)

## 🔧 Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SUPABASE_URL="your-supabase-url"
export SUPABASE_ANON_KEY="your-key"

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🛠 API Endpoints

### Countries API (`/api/countries/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/with-scores` | GET | All countries with AHAII scores |
| `/featured` | GET | Featured countries for homepage |
| `/by-region/{region}` | GET | Countries by African region |
| `/{country_id}/details` | GET | Detailed country profile |
| `/recent-activity` | GET | Countries with recent activity |
| `/statistics` | GET | Platform statistics |
| `/regions` | GET | Regional overview |
| `/{country_id}/refresh-score` | POST | Refresh country score |

### System Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive documentation |
| `/config/info` | GET | Configuration info |

## 📊 Data Sources

- **Database**: Supabase (PostgreSQL)
- **ETL Pipeline**: Automated data collection
- **Academic Papers**: PubMed, arXiv
- **News Sources**: RSS feeds, African tech news
- **Scoring**: Real-time AHAII methodology

## 🔑 Environment Variables

Required variables (see `.env.example`):

```bash
# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Server
ENVIRONMENT=development
HOST=0.0.0.0  
PORT=8000

# Optional API keys for enhanced functionality
SERPAPI_KEY=your-serpapi-key
OPENAI_API_KEY=your-openai-key
```

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test countries API
curl http://localhost:8000/api/countries/featured

# View API documentation
open http://localhost:8000/docs
```

## 🏗 Architecture

```
backend/
├── main.py                 # FastAPI application
├── start_backend.sh        # Startup script
├── requirements.txt        # Dependencies
├── api/
│   └── countries.py        # Countries API endpoints
├── config/
│   ├── database.py         # Database configuration
│   └── settings.py         # Application settings
├── services/
│   ├── database_service.py # Database operations
│   ├── ahaii_scoring_service.py # Scoring logic
│   └── vector_service.py   # Vector operations
└── etl/                    # ETL pipeline components
    ├── academic/           # Academic data processing
    └── news/              # News monitoring
```

## 🔄 ETL Pipeline Integration

The API integrates with a comprehensive ETL pipeline:

- **Academic Processing**: PubMed and arXiv scraping
- **News Monitoring**: RSS feeds and African tech news
- **Scoring Service**: Real-time AHAII calculations
- **Vector Search**: Semantic similarity matching
- **Signal Processing**: Infrastructure indicator extraction

## 🚦 Development vs Production

### Development Mode
- Auto-reload on code changes
- Detailed logging
- CORS enabled for localhost
- Single worker process

### Production Mode  
- Multiple worker processes
- Optimized logging
- Production CORS settings
- Enhanced error handling

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check environment variables
   echo $SUPABASE_URL
   echo $SUPABASE_ANON_KEY
   
   # Test connection manually
   python3 -c "from config.database import supabase; print(supabase.table('countries').select('id').limit(1).execute())"
   ```

2. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **Port Already in Use**
   ```bash
   # Use different port
   ./start_backend.sh development 0.0.0.0 8001
   
   # Kill existing processes
   pkill -f uvicorn
   ```

### Logs

Check logs for detailed error information:
- Development: Console output
- Production: Log files (if configured)

## 📈 Monitoring

### Health Checks
- `/health` - Basic health status
- Database connectivity test
- Service availability check

### Metrics
- `/api/countries/statistics` - Platform statistics
- Response times and error rates
- Database query performance

## 🔒 Security

- Environment variables for sensitive data
- CORS configuration for frontend integration
- Input validation on all endpoints
- Rate limiting (configurable)

## 📚 Documentation

- Interactive API docs: `/docs`
- OpenAPI specification: `/openapi.json`
- ReDoc documentation: `/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Follow code style (Black, flake8)
4. Add tests for new functionality
5. Submit pull request

## 📄 License

African Health AI Infrastructure Index Backend API
Part of the AHAII project for automated health AI infrastructure assessment.

---

**Need Help?** Check the `/docs` endpoint for interactive API documentation or review the health check at `/health`.
