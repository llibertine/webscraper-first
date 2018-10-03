#requests und bs4 installieren
pip install requests BeautifulSoup4

#requests für http requests, 
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

#function
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    Function accepts a single url argument.
    
    The simple_get() function accepts a single url argument. It then makes a GET request to that URL. If nothing goes wrong, you end up with the raw HTML content for the page you requested. If there were any problems with your request (like the URL is bad, or the remote server is down), then your function returns None.

    You may have noticed the use of the closing() function in your definition of simple_get(). The closing() function ensures that any network resources are freed when they go out of scope in that with block. Using closing() like that is good practice and helps to prevent fatal errors and network timeouts.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content #gibt das reine html zurück
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None #returned nix wenn was mit url nicht passt

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

"""Wenn ich jetzt ein html mit namen contrived erhalten habe z.B., dann lese ich es ein und parse es. Für gegebenes HTML z.B.:

<!DOCTYPE html>
<html>
<head>
  <title>Contrived Example</title>
</head>
<body>
<p id="eggman"> I am the egg man </p>
<p id="walrus"> I am the walrus </p>
</body>
</html>
"""
raw_html = open('contrived.html').read()
html = BeautifulSoup(raw_html, 'html.parser')
for p in html.select('p'): #html.select('p') returns a list of paragraph elements
     if p['id'] == 'walrus': #id selected
         print(p.text) #I am the walrus wird geprintet

"""Breaking down the example, you first parse the raw HTML by passing it to the BeautifulSoup constructor. BeautifulSoup accepts multiple back-end parsers, but the standard back-end is 'html.parser', which you supply here as the second argument. (If you neglect to supply that 'html.parser', then the code will still work, but you will see a warning print to your screen.)

The select() method on your html object lets you use CSS selectors to locate elements in the document. In the above case, html.select('p') returns a list of paragraph elements. Each p has HTML attributes that you can access like a dict. In the line if p['id'] == 'walrus', for example, you check if the id attribute is equal to the string 'walrus', which corresponds to <p id="walrus"> in the HTML."""
