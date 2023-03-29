from seleniumwire import webdriver
# import undetected_chromedriver.v2 as uc
import os
import settings


def create_driver(proxy=False, headless=False, ext=False, undetected=False, useragent=False):
    """ Create driver
    proxy state: address or False
    headless state: True or False
    ext state: True or False
    undetected state: True or False
    useragent state: ua or False
    """

    # using proxy
    if proxy is not False:
        options_proxy = {
            'proxy': {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }
        }

    # using undetected chromedriver
    if undetected:
        print('[DRIVER]: UNDETECTED MODE - ON')
        # options = uc.ChromeOptions()  # required undetected_chromedriver.v2
    else:
        print('[DRIVER]: UNDETECTED MODE - OFF')
        chrome = os.path.abspath(settings.DRIVER)

        caps = webdriver.DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-logging")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--output=/dev/null")
        options.add_argument("--log-level=3")


    # using headless mode
    if headless:
        print('[DRIVER]: HEADLESS MODE - ON')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920x1080')
        
    else:
        
        print('[DRIVER]: HEADLESS MODE - OFF')
    
    # fake ua mode
    if useragent:
        print('[DRIVER]: FAKE USER AGENT - ON')
        options.add_argument(f'user-agent={useragent}')
    else:
        print('[DRIVER]: FAKE USER AGENT - OFF')

    # using extensions
    if ext:
        print('[DRIVER]: EXT - ON')
        options.add_extension(settings.EXT_PATH)
        
    else:
        print('[DRIVER]: EXT - OFF')

    if proxy is not False:
        print('[DRIVER]: PROXY - ON')
        # undetected
        if undetected:
            # undetected add proxy
            options.add_argument(f"--proxy-server={proxy}")

            # driver = uc.Chrome(options=options)  # required undetected_chromedriver.v2
        else:
            driver = webdriver.Chrome(executable_path=chrome, desired_capabilities=caps, options=options,
                                  seleniumwire_options=options_proxy)
    else:
        print('[DRIVER]: PROXY - OFF')
        # undetected
        if undetected:
            # driver = uc.Chrome(options=options)  # required undetected_chromedriver.v2
            pass
        else:
            driver = webdriver.Chrome(executable_path=chrome, desired_capabilities=caps, options=options)


    return driver