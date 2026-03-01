FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**2. Add a `requirements.txt`** (simpler than poetry for deployment):
```
discord.py==1.7.1
flask==1.1.2
```

**3. Push to a Git repo** (GitHub, GitLab, etc.)

**4. In Coolify:**
- New Resource → **Application**
- Connect your Git repo
- Build Pack: **Dockerfile**
- Set environment variable: `DISCORD_BOT_SECRET` = your bot token
- Deploy

## Important Notes

**Persistent database:** Your `database.db` file will be lost on redeploys since containers are stateless. To fix this, add a persistent volume in Coolify pointing to `/app/database.db`, or migrate to PostgreSQL.

**The keep_alive Flask server** runs on port 8080 — Coolify will detect this, but it's only needed for Replit-style uptime pinging. On Coolify you don't need it; the container stays alive naturally. You can leave it as-is or remove it.

**Port:** If Coolify asks for a port, enter `8080` (from your Flask keep_alive server).

## The `DISCORD_BOT_SECRET` env var
In Coolify → your app → **Environment Variables**, add:
```
DISCORD_BOT_SECRET=your_actual_bot_token_here