# GDG Devfest Bandung 2024 Demo

Title: Semantic Caching of Gemini AI Response with RedisVL

## Prequisites

### Backend Flask Python

- python3
- pip3
- venv
- docker engine
- docker-compose

### Frontend Flutter Web

```
Doctor summary (to see all details, run flutter doctor -v):
[✓] Flutter (Channel stable, 3.24.5, on macOS 14.6.1 23G93
    darwin-arm64, locale en-ID)
[✗] Android toolchain - develop for Android devices
[✗] Xcode - develop for iOS and macOS
[✓] Chrome - develop for the web
[!] Android Studio (not installed)
[✓] IntelliJ IDEA Community Edition (version 2024.2.5)
[✓] VS Code (version 1.95.3)
[✓] Connected device (2 available)
[✓] Network resources
```

## How to run

### Backend

0. Initiate venv

```
$ python3 -m venv venv
```

1. Move to directory demo/backend

```
$ cd demo/backend
```

2. Run containers

```
$ docker-compose up -d
```

3. Start venv

```
$ source venv/bin/activate
```

4. Install dependencies

```
$ pip3 install -r requirements.txt
```

5. Copy and fill the environment variables in `.env` with correct values

```
mv .env.sample .env
```

6. Run server

```
$ python3 app.py
```

If it shows message similiar to below, then you are ready to go in `http://127.0.0.1:3000`

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:3000
Press CTRL+C to quit
 * Restarting with stat
08:24:54 redisvl.index.index INFO   Index already exists, not overwriting.
 * Debugger is active!
 * Debugger PIN: 620-094-968
```

### Frontend

0. Install dependencies

```
$ flutter pub get
```

1. Copy and fill the environment variables in `web/assets/.env` with correct values

```
mv web/assets/.env.sample web/assets/.env
```

2. Run server

```
$ flutter run -d chrome
```

If it shows message similiar to below, then you are ready to go in `http://127.0.0.1:50787`

```
Launching lib/main.dart on Chrome in debug mode...
Waiting for connection from debug service on Chrome...              9.7s
This app is linked to the debug service:
ws://127.0.0.1:50787/AQW6Re1rlss=/ws
Debug service listening on ws://127.0.0.1:50787/AQW6Re1rlss=/ws

🔥  To hot restart changes while running, press "r" or "R".
For a more detailed help message, press "h". To quit, press "q".

A Dart VM Service on Chrome is available at:
http://127.0.0.1:50787/AQW6Re1rlss=
[INFO] 2024-12-07 08:25:13.831: AppLogger - Initializing session
[INFO] 2024-12-07 08:25:13.841: AppLogger - Response: 201 {
  "data": {
    "expires_in": 3600,
    "value":
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpcCI6IjEyNy4wLjAuMSJ9.qAq0
    vI3ZMCpTPyGEd1nq1xDHjs1LRFXznf_kqa3xOg4"
  },
  "success": true
}

[INFO] 2024-12-07 08:25:13.842: AppLogger - Session initialized and
stored.
The Flutter DevTools debugger and profiler on Chrome is available at:
http://127.0.0.1:9101?uri=http://127.0.0.1:50787/AQW6Re1rlss=
```
