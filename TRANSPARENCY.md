# Transparency

### We use SSL powered with Mozilla Open Source License .pem
- What calls to the internet do we do?
  - We call to:
    - `Starting new HTTPS connection (1): api.pokerogue.net:443`
      - and its endpoints for example
      - https://api.pokerogue.net:443 "POST /account/login HTTP/11" 200 None
    - CURL's hosted SSL certificate
      - https://curl.se/docs/caextract.html
    - Our GitHub repo
      - https://api.github.com:443 "GET /repositories/807308129/commits?since=[UTF DATE] HTTP/1.1" 200 2

      ![Preview image](.github/previews/networkResolution.png)
---
- WE DO NOT SAVE ANYTHING and do NOT send any analytics, nothing
  - Only thing we "save" locally is game related:
    - `trainer.json`
    - any `slot_*.json`
    - any `backups/*.json`
---
<a href="https://www.virustotal.com/gui/file/30e6f8451c099444e15a337e41bea14e38861a14b0189d0cd1af6b03a795a5ce?nocache=1"><img src="https://img.shields.io/badge/Latest_Virus_Total-30e6f8451c099444e15a337e41bea14e38861a14b0189d0cd1af6b03a795a5ce-Green"></a>
