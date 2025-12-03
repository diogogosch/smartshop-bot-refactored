# SmartShopBot - Production-Ready Telegram Bot for Portainer

**SmartShopBot** is a fully-featured, production-ready Telegram bot for shopping list management, receipt processing, and AI-powered suggestions. Optimized for Portainer deployment.

## Core Features

- Shopping List Management - Add, remove, and manage items
- Receipt Processing - Upload photos for automatic OCR
- AI Suggestions - Get shopping recommendations
- Multi-Language Support - 10+ languages
- Analytics Dashboard - Spending statistics
- Price Tracking - Historical pricing data
- Telegram Native - Full bot functionality

## Quick Start (Local)

```bash
git clone https://github.com/diogogosch/smartshop-bot-refactored.git
cd smartshop-bot-refactored
cp .env.example .env
# Edit .env with your TELEGRAM_TOKEN from @BotFather
docker-compose up -d
```

## Environment Variables

### CRITICAL - Required
```
TELEGRAM_TOKEN=your_token_from_botfather
```

### Database
```
DATABASE_URL=postgresql+asyncpg://smartshop:password@postgres:5432/smartshop_db
POSTGRES_USER=smartshop
POSTGRES_PASSWORD=YourSecurePassword123
POSTGRES_DB=smartshop_db
```

### Connection Pool (IMPORTANT)
```
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### Server
```
HOST=0.0.0.0
PORT=8080
LOG_LEVEL=INFO
```

### Optional (AI)
```
OPENAI_API_KEY=sk-your-key
REDIS_URL=redis://redis:6379/0
```

## PORTAINER DEPLOYMENT GUIDE

### Step 1: Prepare on Server

```bash
git clone https://github.com/diogogosch/smartshop-bot-refactored.git /opt/smartshop-bot
cd /opt/smartshop-bot
cp .env.example .env
# Edit .env with your values
nano .env
```

### Step 2: Access Portainer

1. Open Portainer Web UI (https://your-portainer-ip:9443)
2. Login with your credentials
3. Select your Docker environment

### Step 3: Deploy Stack

**Option A: Via Portainer UI**

1. Go to **Stacks** menu
2. Click **+ Add Stack**
3. Name: `smartshop-bot`
4. Choose **Docker Compose**
5. Copy docker-compose.yml content into editor
6. Add Environment Variables:
   - TELEGRAM_TOKEN (required)
   - POSTGRES_PASSWORD (required)
   - DATABASE_POOL_SIZE = 20
   - DATABASE_MAX_OVERFLOW = 10
   - LOG_LEVEL = INFO
7. Click **Deploy the stack**

**Option B: Via CLI**

```bash
cd /opt/smartshop-bot
portainer-cli stack deploy \
  --name smartshop-bot \
  --compose-file docker-compose.yml \
  --env-file .env
```

### Step 4: Verify Deployment

```bash
# Check all services
docker-compose ps

# Health check (should return 200 OK)
curl http://localhost:8080/health

# View bot logs
docker-compose logs -f bot

# Database admin UI
# Browser: http://localhost:8181
```

### Step 5: Test Bot

1. Open Telegram
2. Search for your bot (@BotName)
3. Send `/start` command
4. Bot should respond with welcome message
5. Try `/help` to see commands

6. ## BOT COMMANDS

| Command | Example | Description |
|---------|---------|-------------|
| `/start` | `/start` | Welcome & quick start |
| `/help` | `/help` | Show all commands |
| `/add` | `/add Milk 2` | Add item with quantity |
| `/list` | `/list` | View shopping list |
| `/remove` | `/remove 1` | Remove item by number |
| `/clear` | `/clear` | Clear entire list |
| `/suggestions` | `/suggestions` | Get AI recommendations |
| `/stats` | `/stats` | View spending stats |
| `/receipt` | `/receipt` | Process receipt photo |
| `/currency` | `/currency USD` | Set currency |
| `/language` | `/language pt` | Set language |

## TROUBLESHOOTING

### Bot Not Responding

```bash
# Verify token is valid
echo $TELEGRAM_TOKEN

# Check bot logs
docker-compose logs bot | grep -i error

# Test Telegram API
curl https://api.telegram.org/bot$TELEGRAM_TOKEN/getMe
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
docker-compose exec postgres pg_isready

# Reset database
docker-compose down -v
docker-compose up -d
```

### Health Check Failing

```bash
# Test health endpoint
curl -v http://localhost:8080/health

# Should return: OK with 200 status
```

## SERVICES

- **smartshop_bot** - Main Telegram bot (port 8080 health)
- **smartshop_postgres** - Database (port 5432, internal)
- **smartshop_redis** - Cache (port 6379, internal)
- **smartshop_adminer** - DB admin (port 8181, http://localhost:8181)

## PERFORMANCE TUNING

### Low Traffic (< 10 requests/sec)
```
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=5
```

### Normal Traffic (10-50 requests/sec) - RECOMMENDED
```
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### High Traffic (> 50 requests/sec)
```
DATABASE_POOL_SIZE=40
DATABASE_MAX_OVERFLOW=20
```

## SECURITY NOTES

1. Never commit `.env` to git
2. Use strong passwords (min 16 characters)
3. Rotate API keys periodically
4. Use Portainer Secrets for sensitive data
5. Enable HTTPS for Portainer access
6. Restrict PostgreSQL to internal network
7. Change default credentials

## UPDATING

```bash
cd /opt/smartshop-bot
git pull origin main
docker-compose build --no-cache bot
docker-compose up -d bot
```

Or in Portainer UI:
1. Stacks → smartshop-bot
2. Pull latest image
3. Redeploy stack

## DATABASE ADMIN

Access Adminer at http://localhost:8181
- System: PostgreSQL
- Server: postgres
- User: smartshop
- Password: (from POSTGRES_PASSWORD)
- Database: smartshop_db

## STATUS

✅ Production-Ready | ✅ Docker Certified | ✅ Portainer Compatible

Last Updated: 2025-12-03 | License: MIT

For issues and support: Check docker-compose logs and health endpoint.
