import urllib.request
import urllib.parse
import re

try:
    from colorama import init, Fore, Back, Style, deinit
    import validators
except Exception as e:
    print(str(e))
    exit(0)


def show_alert(alert_type, message):
    if alert_type == "success":
        print('{}[+]{} {}'.format(Fore.GREEN, Fore.RESET, message))
    elif alert_type == "warning":
        print('{}[!]{} {}'.format(Fore.YELLOW, Fore.RESET, message))
    elif alert_type == "danger":
        print('{}[x]{} {}'.format(Fore.RED, Fore.RESET, message))
    elif alert_type == 'info':
        print('{}[#]{} {}'.format(Fore.CYAN, Fore.RESET, message))
    else:
        print('{}[@]{} {}'.format(Fore.WHITE, Fore.RESET, message))
def detect_file_name(url):
    
try:
    url = 'https://4rd.ir'
    request = urllib.request.urlopen(url)
    request_content = request.read().decode('utf-8')
    show_alert('success','request submited successfully!')
    #create template :
    show_alert('warning','creating template ...')
    #template_file = open('','w')
    show_alert('success','template created successfully!')
    #extracting styles :
    show_alert('warning','extracting site styles ...')
    styles_list = re.findall(r'<link rel="stylesheet" href="(.*)?">',str(request_content))

    for style in styles_list:
        if not validators.url(style):
            #...
        show_alert('info',style)
    #extracting javascript files :
    show_alert('warning','extracting javascripting files ...')
    javascript_list = re.findall(r'<script src="(.*)?">',str(request_content))
    for javascript in javascript_list:
        show_alert('info',javascript)
except Exception as e:
    show_alert('danger',str(e))
