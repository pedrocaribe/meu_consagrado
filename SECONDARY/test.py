import requests



url = 'https://www.airlinemanager.com/fuel.php?undefined&fbSig=false&_=1690238957192'

header = {
    'method':'GET',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

}

re = requests.get(url, headers=header)

print(re.text)