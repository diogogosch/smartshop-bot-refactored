# SmartShopBot - Production Deployment Guide

## Overview
This comprehensive guide covers deploying SmartShopBot as a fully containerized Telegram bot using Docker and Portainer. The bot uses async-first architecture with SQLAlchemy AsyncIO, PostgreSQL, and Redis.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Portainer Deployment](#portainer-deployment)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
7. [Production Best Practices](#production-best-practices)

## Prerequisites

### Required Software
- **Docker**: v20.10+
- **Docker Compose**: v2.0+
- **Portainer**: v2.15+ (optional but recommended)
- **Git**: For repository cloning

### Required Accounts & Tokens
- **Telegram Bot Token**: Create via [@BotFather](https://t.me/botfather)
- **OpenAI API Key** (optional): For AI suggestions
- **Server/VPS**: Minimum 1GB RAM, 20GB SSD

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/diogogosch/smartshop-bot-refactored.git
cd smartshop-bot-refactored
```

### 2. Configure Environment Variables
Create `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
OPENAI_API_KEY=sk-...your-key-here
POSTGRES_USER=smartshop
POSTGRES_PASSWORD=super_secure_password_here
POSTGRES_DB=smartshop_db
LOG_LEVEL=INFO
```

### 3. Deploy with Docker Compose
```bash
docker-compose up -d
```

### 4. Verify Deployment
```bash
# Check container status
docker-compose ps

# View bot logs
docker-compose logs -f bot

# Access database admin
# Open browser to http://localhost:8181
```

## Portainer Deployment

### Step-by-Step Setup

#### 1. Access Portainer Dashboard
- Navigate to your Portainer instance: `https://your-server:9443`
- Login with your credentials

#### 2. Create New Stack
1. Go to **Stacks** → **Add stack**
2. Name: `smartshop-bot`
3. Select build method:
   - **GitHub**: Point to repo URL if public
   - **Upload**: Upload the docker-compose.yml file

#### 3. Configure Environment
In Portainer, add environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| TELEGRAM_TOKEN | Your bot token | Required |
| POSTGRES_USER | smartshop | DB username |
| POSTGRES_PASSWORD | Strong password | DB password |
| POSTGRES_DB | smartshop_db | Database name |
| OPENAI_API_KEY | Your key or empty | Optional |
| LOG_LEVEL | INFO | DEBUG/INFO/WARNING |

#### 4. Deploy
- Click **Deploy the stack**
- Wait 30-60 seconds for containers to start

#### 5. Verify Status
- Check **Containers** → Look for `smartshop_bot` (should be **Healthy** - green)
- All 4 containers should show:
  - `smartshop_bot` ✓ Healthy
  - `smartshop_db` ✓ Healthy
  - `smartshop_redis` ✓ Healthy
  - `smartshop_adminer` ✓ Running

### Container Health Checks
The Docker image includes built-in health checks:
- **Bot Health**: Pings `http://localhost:8080/health` every 30 seconds
- **Database Health**: Runs `pg_isready` every 10 seconds
- **Redis Health**: Runs `redis-cli ping` every 10 seconds

## Configuration

### Environment Variables

#### Required
- `TELEGRAM_TOKEN`: Your Telegram Bot API token (from @BotFather)
- `DATABASE_URL`: PostgreSQL connection string (auto-generated from docker-compose)
- `REDIS_URL`: Redis connection URL (auto-generated)

#### Optional
- `OPENAI_API_KEY`: For AI-powered suggestions
- `LOG_LEVEL`: Logging verbosity (DEBUG|INFO|WARNING|ERROR)

#### Docker Configuration
- `HOST`: HTTP server bind address (default: 0.0.0.0)
- `PORT`: Health check server port (default: 8080)

### Secrets Management

**NEVER commit `.env` files to Git!**

For production:
1. Use Portainer Secrets or Environment Variables section
2. Use external secret management (HashiCorp Vault, AWS Secrets Manager)
3. Rotate tokens periodically
4. Use strong, unique passwords for databases

## Database Setup

### PostgreSQL Initialization
The `init.sql` file runs automatically when the database container starts.

It creates:
- All necessary tables
- Indexes for performance
- User roles

### Database Access

**Using Adminer (recommended):**
1. Open http://localhost:8181 or http://your-server:8181
2. System: PostgreSQL
3. Server: `postgres` (Docker service name)
4. Username: Your `POSTGRES_USER`
5. Password: Your `POSTGRES_PASSWORD`
6. Database: Your `POSTGRES_DB`

**Using psql (command line):**
```bash
docker exec -it smartshop_db psql -U smartshop -d smartshop_db

# List tables
\dt

# View users
SELECT * FROM users;
```

### Backup Database
```bash
# Backup
docker exec smartshop_db pg_dump -U smartshop smartshop_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
cat backup_20240101_120000.sql | docker exec -i smartshop_db psql -U smartshop smartshop_db
```

## Monitoring & Troubleshooting

### View Logs

```bash
# Bot logs
docker-compose logs -f bot

# Database logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis

# All logs with timestamps
docker-compose logs --timestamps -f
```

### Common Issues

#### 1. Bot Not Responding
```bash
# Check if token is set
docker exec smartshop_bot env | grep TELEGRAM_TOKEN

# Check logs
docker-compose logs bot | tail -50

# Restart bot
docker-compose restart bot
```

#### 2. Database Connection Errors
```bash
# Check database status
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection from bot container
docker exec smartshop_bot python -c "from app.core.database import engine; print(engine)"
```

#### 3. Health Check Failures
```bash
# Check health check status in Portainer or:
docker ps --filter "name=smartshop_bot" --no-trunc

# Manually test health endpoint
docker exec smartshop_bot curl -f http://localhost:8080/health || echo "Failed"
```

### Performance Monitoring

```bash
# CPU/Memory usage
docker stats

# Database connection pool status
docker exec smartshop_db psql -U smartshop smartshop_db -c "SELECT count(*) FROM pg_stat_activity;"

# Redis memory usage
docker exec smartshop_redis redis-cli INFO memory
```

## Production Best Practices

### 1. Resource Limits

Add to `docker-compose.yml` for each service:
```yaml
services:
  bot:
    ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### 2. Security
- Always use strong, randomly generated passwords
- Rotate tokens and credentials regularly
- Keep Docker images updated: `docker pull postgres:15-alpine`
- Run bot container as non-root user (already configured)
- Use Docker networks (already configured)

### 3. Backup Strategy
- Automated daily database backups
- Store backups in external storage (S3, GCS, etc.)
- Test restores regularly

### 4. Logging & Monitoring
- Configure centralized logging (ELK Stack, Splunk)
- Set up alerts for container crashes
- Monitor bot response times

### 5. Updates & Patches
```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

## Scaling

### Horizontal Scaling with Multiple Bot Instances
```yaml
services:
  bot:
    deploy:
      replicas: 3  # Run 3 instances
```

### Load Balancing
For multiple bot instances, use:
- **Nginx/HAProxy**: Round-robin the health check endpoints
- **Redis**: Shared message queue for handlers

## Advanced Configuration

### Custom Network
```bash
# Create custom network
docker network create smartshop-network

# Connect containers
docker network connect smartshop-network smartshop_bot
```

### SSL/TLS for HTTP Endpoint
```yaml
bot:
  ports:
    - "8443:8080"  # Expose with SSL reverse proxy
```

## Support & Resources

- **Telegram Bot API Docs**: https://core.telegram.org/bots/api
- **Docker Documentation**: https://docs.docker.com
- **Portainer Documentation**: https://www.portainer.io/documentation/
- **SQLAlchemy AsyncIO**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

## License
MIT License - See LICENSE file

## Contributing
See CONTRIBUTING.md for guidelines
