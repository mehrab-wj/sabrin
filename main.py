import urllib.request
import urllib.parse
import urllib
import re
import os
import sys
import linecache

try:
    from colorama import init, Fore, Back, Style, deinit
    import validators
except Exception as e:
    print(str(e))
    exit(0)

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

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


def extract_dir_name_by_url(url):
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    url = url.replace('/', '-')
    url = url.replace('?', '-')
    return url


def extract_file_name_by_url(url):
    filename = url[url.rfind("/")+1:]
    if filename == '':
        filename = 'index'
    return filename


def extract_dir_name_by_local_addr(addr, file_name):
    addr = addr.split('/')
    dir_addr = ''
    i = 0
    while i < len(addr):
        slash = '/'
        if i == 0:
            slash = ''
        if addr[i] != file_name:
            dir_addr = '{}{}{}'.format(dir_addr, slash, addr[i])
        i += 1
    return dir_addr
def make_dir(dir_name):
    try:
        dir_name = re.sub(r'(\?.*)', '', dir_name)
        os.makedirs(dir_name)
    except FileExistsError:
        # directory already exists
        pass
def make_file(file_name,content):
    file_name = re.sub(r'(\?.*)', '', file_name)
    the_file = open(file_name, 'w' , encoding="utf-8")
    the_file.write(str(content)) 
    the_file.close()
def new_request(url):
    request = urllib.request.urlopen(url)
    request_content = request.read().decode('utf-8')
    return request_content

try:
    url = 'https://4rd.ir'
    request = urllib.request.urlopen(url)
    request_content = request.read().decode('utf-8')
    show_alert('success', 'request submited successfully!')
    #create template :
    show_alert('warning', 'creating template ...')
    dir_name = extract_dir_name_by_url(url)
    file_name = extract_file_name_by_url(url)
    make_dir(dir_name)
    template_file = open('{}/{}.html'.format(dir_name,file_name), 'w' , encoding="utf-8")
    template_file.write(str(request_content))
    template_file.close()
    show_alert('success', 'template created successfully!')
    #extracting styles :
    show_alert('warning', 'extracting site styles ...')
    styles_list = re.findall(r'<link rel="stylesheet" href="(.*)?".*>', str(request_content))

    for style in styles_list:
        if not validators.url(style):
            #style loaded from local url , we should download it:
            style_file_name = extract_file_name_by_url(style)
            style_dir = extract_dir_name_by_local_addr(style,style_file_name)
            make_dir('{}/{}'.format(dir_name, style_dir))
            style_url = '{}/{}/{}'.format(url, style_dir, style_file_name)
            style_content = new_request(style_url)
            style_path_in_system = '{}/{}/{}'.format(dir_name,style_dir, style_file_name)
            make_file(style_path_in_system,style_content)
            show_alert('info', 'new file created [{}] url: {}'.format(style_url,style_path_in_system))
        
    #extracting sources :
    show_alert('warning','extracting sources ...')
    sources_list = re.findall(r'src="(.*?)"', str(request_content))
    for source in sources_list:
        
        if not validators.url(source):
            #download sources proccess:
            source_file_name = extract_file_name_by_url(source)
            source_dir = extract_dir_name_by_local_addr(source,source_file_name)
            make_dir('{}/{}'.format(dir_name,source_dir))
            source_url = '{}/{}/{}'.format(url,source_dir,source_file_name)
            source_path_in_sytem = '{}/{}/{}'.format(dir_name,source_dir,source_file_name)
            source_path_in_sytem = re.sub(r'(\?.*)', '', source_path_in_sytem)
            f = open(source_path_in_sytem, 'wb')
            f.write(urllib.request.urlopen(source_url).read())
            f.close()
            show_alert('info','new source created[{}] url: {}'.format(source_path_in_sytem,source_url))
        
except:
    PrintException()