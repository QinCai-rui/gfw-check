# GFW Check

A webapp & API that checks if a website is blocked by the Great Firewall of China (GFW).

## How it works

This software is made of two parts: a frontend and a backend.

### Frontend

The frontend is a React app that allows users to input a URL and see the results (hosted on my server in New Zealand).

See [frontend/README.md](frontend/README.md) for setup and development instructions.

### Backend

The backend is a FastAPI server that gets the URL from the frontend, checks if it is blocked by the GFW, and then returns the results to the frontend.

It is hosted on my Raspberry Pi Zero 2 in Mainland China, which allows it to check if a website is accessible behind the GFW.

Features:
- RESTful API for checking URLs
- CORS support for frontend

See [backend/README.md](backend/README.md) for setup and API documentation.

## Why I made this

I made this project because I wanted to have a website that can check if a site is accessible behind the GFW, and one that JUST WORKS. In my experience there are many websites out there that claim to do this, but more often than not they just DON'T WORK!!! Or the results are inaccurate.

Examples (not comprehensive):

- <https://www.chinafirewalltest.com/> (lies about google.com being accessible)
- <https://www.comparitech.com/privacy-security-tools/blockedinchina/> (504 Gateway Timeout)
- <https://blocky.greatfire.org/> (502 Bad Gateway, at least when I tested it)
- <https://proprivacy.com/tools/blockedinchina> (says that bing.com is blocked, which is not true)
- <https://www.websitepulse.com/tools/china-firewall-test> (hangs indefinitely when I tested it)
- <https://www.cloudwards.net/tools/chinese-firewall-test/> (also hangs indefinitely when I tested it)
- <https://www.dotcom-tools.com/china-firewall-test> (kind of works, but the results are inconsistent and it often hangs for a long time)
