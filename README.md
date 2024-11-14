## WeatherScraper
### 1. configure chrome driver
   - download a chrome driver with version corresponding to browser ```https://developer.chrome.com/docs/chromedriver/downloads?hl=zh-cn```
   - move the executable file under the path where python installed

### 2. set and start proxy for selenium
- find the path where chrome.exe is installed
- create path selenium/AutomationProfile
- start the proxy: open a terminal and run :```cd </path/to/chrome.exe>```
- then ``` chrome.exe --remote-debugging-port=9222 --user-data-dir="<C:\path\to\selenium\AutomationProfile>"```
- here s an example
-  ```cd C:\Program Files\Google\Chrome\Application\```
-  ``` chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\Dev\Scraper\WeatherScraper\selenium\AutomationProfile" ```

### 3. locating data
- start proxy, run code and browser opens up automatically
- moretools -> developer tools -> customize and control dev tools (3 dots) -> undock into separate window
- clear site cookies (view page info button to the left of the address bar) and refresh page
- 


   
