cd /d D:\django_projects\spacebook
D:\django_env\Scripts\activate
-m uvicorn spacebook_project.asgi:application --host 127.0.0.1 --port 8000 --lifespan off --loop asyncio --http auto --timeout-keep-alive 30 --proxy-headers --forwarded-allow-ips="*"
