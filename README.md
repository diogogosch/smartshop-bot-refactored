# SmartShopBot - Refactored Version

🛒 **SmartShopBot** is a fully-featured Telegram bot for intelligent shopping list management, receipt processing, and AI-powered suggestions.

## Features

✨ **Core Features:**
- 📝 **Shopping List Management** - Add, remove, and manage items
- 🧾 **Receipt Processing** - Upload receipt photos for automatic OCR extraction
- 🤖 **AI Suggestions** - Get personalized shopping recommendations using OpenAI/Gemini
- 💰 **Price Tracking** - Historical price tracking for products
- 🌍 **Multi-Language Support** - Support for 10+ languages
- 💵 **Currency Conversion** - Set preferred currency for expense tracking
- 🏪 **Store Management** - Save favorite stores
- 📊 **Analytics** - Spending statistics and analytics

## Improvements in This Refactored Version

### Code Quality
- ✅ Improved error handling and logging
- ✅ Better separation of concerns
- ✅ Enhanced configuration management
- ✅ Type hints throughout
- ✅ Comprehensive documentation

### Architecture
- ✅ Modular handler design
- ✅ Centralized database operations
- ✅ Async/await patterns
- ✅ Connection pooling for database
- ✅ Redis caching support

### Deployment
- ✅ Docker & Docker Compose setup
- ✅ Health check endpoints
- ✅ Environment-based configuration
- ✅ PostgreSQL 15 support
- ✅ Redis 7 support

## Installation

### Prerequisites
- Docker & Docker Compose
- Telegram Bot Token
- OpenAI or Google Vision API Key (optional)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/smartshop-bot-refactored.git
cd smartshop-bot-refactored

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env

# Start services
docker-compose up -d
```

### Environment Variables

```env
TELEGRAM_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_key
GOOGLE_VISION_API_KEY=your_google_vision_key
DATABASE_URL=postgresql://smartshop:password@postgres:5432/smartshop_db
REDIS_URL=redis://redis:6379/0
LOG_LEVEL=INFO
DATABASE_POOL_SIZE=10
DATABASE_PASSWORD=your_secure_password
```

## Available Commands

- `/start` - Welcome message and quick start
- `/help` - Command reference
- `/add <item> [quantity]` - Add item to list
- `/remove <item>` - Remove item from list
- `/list` - View shopping list
- `/clear` - Clear entire shopping list
- `/receipt` - Process receipt photo
- `/suggestions` - Get AI recommendations
- `/stats` - View spending analytics
- `/currency <code>` - Set currency (USD, BRL, EUR, etc.)
- `/language <code>` - Set language (en, pt, es, etc.)
- `/stores` - Manage favorite stores
- `/settings` - View current settings

## Project Structure

```
app/
├── config/
│   ├── settings.py       # Configuration management
│   └── __init__.py
├── core/
│   ├── database.py       # Database operations
│   └── __init__.py
├── handlers/
│   ├── shopping_handler.py
│   ├── receipt_handler.py
│   ├── suggestion_handler.py
│   ├── stats_handler.py
│   ├── settings_handler.py
│   ├── base.py           # Base handler
│   └── __init__.py
├── models/
│   ├── user.py
│   ├── product.py
│   ├── shopping_list.py
│   └── __init__.py
├── services/
│   ├── notification_service.py
│   ├── ai_service.py
│   ├── ocr_service.py
│   └── __init__.py
├── translations/
│   ├── en.json
│   ├── pt.json
│   └── __init__.py
├── utils/
│   ├── i18n.py           # Internationalization
│   ├── logger.py
│   └── __init__.py
├── main.py               # Application entry point
└── __init__.py
```

## Database Schema

- **users** - User profiles and preferences
- **products** - Product catalog
- **shopping_lists** - Shopping list instances
- **shopping_list_items** - Items in lists
- **receipts** - Receipt records
- **receipt_items** - Items extracted from receipts
- **price_history** - Historical pricing data

## API & Services

### Health Check
```
GET http://localhost:8080/health
```

### Database Admin
Adminer is available at `http://localhost:8181` for database management

## Development

### Running Tests
```bash
docker-compose up -d
# Tests will run in CI/CD pipeline
```

### Local Development
```bash
pip install -r requirements.txt
python -m app.main
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## Troubleshooting

### Bot not responding
- Check TELEGRAM_TOKEN is correct
- Verify bot has internet connection
- Check logs: `docker-compose logs -f bot`

### Database connection issues
- Verify PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL format
- Ensure password is correct

### AI features not working
- Verify API keys in .env
- Check API rate limits
- Verify image format for receipt processing (JPG, PNG)

## Performance Tips

- Increase `DATABASE_POOL_SIZE` for high traffic
- Use Redis for caching
- Enable database query logging for optimization
- Monitor memory usage with `docker stats`

## License

MIT License - feel free to use in your own projects

## Support

For issues and questions:
- Open a GitHub issue
- Check existing documentation
- Review error logs in container

---

**Made with ❤️ for shopping lovers**
