"""
GFW Check API Backend

todo 21, 165
"""

from datetime import datetime
import httpx
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GFW Check API")

# allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Set to specific frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHECK_TIMEOUT = 10  # seconds
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def is_url_valid(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


async def check_url_accessibility(url: str) -> dict:
    """
    Check if a URL is accessible from China
    Returns: {"blocked": bool, "status_code": int or None, "error": str or None}
    """
    try:
        # Ensure URL has a scheme
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        async with httpx.AsyncClient(timeout=CHECK_TIMEOUT) as client:
            try:
                response = await client.get(
                    url,
                    follow_redirects=True,
                    headers={"User-Agent": USER_AGENT},
                )
                
                # any response = site accessible
                logger.info(f"URL {url} is accessible - Status: {response.status_code}")
                return {
                    "blocked": False,
                    "status_code": response.status_code,
                    "error": None,
                }
            
            except httpx.ConnectError as e:
                # Connection refused or couldn't reach host
                logger.warning(f"Connection error for {url}: {str(e)}")
                return {
                    "blocked": True,
                    "status_code": None,
                    "error": "Connection refused",
                }
            
            except httpx.TimeoutException as e:
                # Timeout usually indicates blocking (case of google and discord)
                logger.warning(f"Timeout for {url}: {str(e)}")
                return {
                    "blocked": True,
                    "status_code": None,
                    "error": "Connection timeout",
                }
            
            except httpx.ReadError as e:
                # Connection reset or read error
                logger.warning(f"Read error for {url}: {str(e)}")
                return {
                    "blocked": True,
                    "status_code": None,
                    "error": "Connection reset",
                }
            
            except Exception as e:
                # Unknown error - prolly blocking
                logger.warning(f"Unknown error for {url}: {str(e)}")
                return {
                    "blocked": True,
                    "status_code": None,
                    "error": "Unknown error",
                }
    
    except Exception as e:
        logger.error(f"Unexpected error checking {url}: {str(e)}")
        return {
            "blocked": True,
            "status_code": None,
            "error": "Unexpected error",
        }


@app.get("/")
async def root():
    return {"message": "GFW Check API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/check")
async def check_url_endpoint(url: str = Query(..., description="URL to check")):
    """
    Check if a URL is blocked by GFW
    
    Args:
        url: The URL to check (e.g., https://google.com or google.com)
    
    Returns:
        {
            "url": "https://google.com",
            "blocked": false,
            "status_code": 200,
            "error": null,
            "timestamp": "2024-01-01T12:00:00Z"
        }
    """
    # Validate URL format
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
    
    if not is_url_valid(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL format. Please provide a valid URL (e.g., https://google.com)"
        )
    
    # add protocol to beginning of URL
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    logger.info(f"Checking URL: {url}")
    
    # Check site status
    check_result = await check_url_accessibility(url)
    
    return {
        "url": url,
        "blocked": check_result["blocked"],
        "status_code": check_result["status_code"],
        "error": check_result["error"],
        "timestamp": datetime.utcnow().isoformat() + "Z", # TODO forgot syntax. change later
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
