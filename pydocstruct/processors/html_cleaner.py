import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

class HtmlNoiseCleaner:
    """Cleaner to remove content noise (headers, footers, navigation, etc.) from HTML"""
    
    # Tags, classes, or IDs to remove
    NOISE_TAGS = ['script', 'style', 'head', 'iframe', 'noscript', 'meta', 'svg']
    NOISE_CLASSES = ['header', 'footer', 'nav', 'menu', 'sidebar', 'ad', 'advertisement', 'cookie', 'popup']
    
    @classmethod
    def clean(cls, html_content: str) -> str:
        """Extract and clean main content from HTML content"""
        if BeautifulSoup is None:
            raise ImportError("beautifulsoup4 is required. pip install beautifulsoup4")
            
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove unnecessary tags
        for tag in cls.NOISE_TAGS:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove semantic tags like header, footer, nav
        for tag in ['header', 'footer', 'nav', 'aside']:
            for element in soup.find_all(tag):
                element.decompose()
                
        # Remove by class name or ID if matching noise keywords
        # (Be careful, remove only widely identifiable noise)
        for element in soup.find_all(attrs={"class": True}):
            classes = element.get("class")
            if isinstance(classes, list):
                classes = " ".join(classes)
            if any(noise in classes.lower() for noise in cls.NOISE_CLASSES):
                element.decompose()
                
        for element in soup.find_all(attrs={"id": True}):
            id_val = element.get("id")
            if any(noise in id_val.lower() for noise in cls.NOISE_CLASSES):
                element.decompose()
        
        # Extract text
        text = soup.get_text(separator="\n", strip=True)
        # Normalize continuous newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text
