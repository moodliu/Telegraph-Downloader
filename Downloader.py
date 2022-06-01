import re
import os
import argparse
from urllib import request
import subprocess


def web_source_code_process(page_source):
    # folder create
    title_regex = r"<title>.*<\/title>"
    title_name = re.findall(title_regex, page_source)  # list
    dir_path = title_name[0].replace('<title>', '').replace('</title>','').replace(' ','').replace('&#33;','-')
    dir_path = './' + dir_path
    if os.path.isdir(dir_path) == False:
        os.mkdir(dir_path)

    # find <img src="..."> in page source code
    img_src_regex = r"<img src=\"\S*\">"
    img_src_path = re.findall(img_src_regex, page_source)
    # print(len(img_src_path))

    # extract file name from img_src_path , output file_name.jpg or file_name.png
    img_file_name = list()
    for name in img_src_path:
        name = name.replace('<img src="', '').replace('">', '')
        if name[0] == '/':
            name = 'https://telegra.ph' + name
        elif name.count('https://imageproxy.pimg.tw/resize?url='):
            name = name.replace('https://imageproxy.pimg.tw/resize?url=',
                                '').replace('%3A', ':').replace('%2F', '/')
        img_file_name.append(name)

    # delete duplicate file name
    no_duplicate_jpg_file = list()
    for i in img_file_name:
        if i not in no_duplicate_jpg_file:
            no_duplicate_jpg_file.append(i)

    return dir_path, no_duplicate_jpg_file


def pic_file_txt(no_duplicate_jpg_file, dir_path):
    with open(dir_path+'/file_path.txt', 'w') as fp:
        for item in no_duplicate_jpg_file:
            fp.write(item+'\n')
        fp.close()


def get_file_from_cmd(txt_file, dir_path):
    '''
    https://aria2.github.io/manual/en/html/aria2c.html
    '''
    save_dir = dir_path
    txt_path = dir_path + '/'+txt_file
    os.system("aria2c.exe " + '-d ' + save_dir +
              ' -x 10 -j 10 ' + '-i ' + txt_path)


def rename_downloaded_file(no_duplicate_jpg_file, dir_path):
    # rename
    i = 0
    for item in no_duplicate_jpg_file:
        file_name = re.findall(r"\w*.jpg|\w*.png|\w*.jpeg", item)
        if file_name[0].count('.jpg'):
            os.rename(dir_path+'/'+file_name[0], dir_path +
                      '/'+'{:03}'.format(i+1)+'.jpg')
        elif file_name[0].count('.png'):
            os.rename(dir_path+'/'+file_name[0], dir_path +
                      '/'+'{:03}'.format(i+1)+'.png')
        elif file_name[0].count('.jpeg'):
            os.rename(dir_path+'/'+file_name[0], dir_path +
                      '/'+'{:03}'.format(i+1)+'.jpeg')
        i = i+1


def argument():
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument('--url')
    args = parser.parse_args()
    url_value = args.url
    return url_value


url_value = argument()
#url_value = ''
response = request.urlopen(url_value)
page_source = response.read().decode('utf-8')

dir_path, file_path = web_source_code_process(page_source)
# create txt file
pic_file_txt(file_path, dir_path)
# download via txt by using aria2c
get_file_from_cmd('file_path.txt', dir_path)
#rename and ordered
print('Renameing...')
rename_downloaded_file(file_path, dir_path)
os.remove(dir_path+'/file_path.txt')
print('Finish.')
print('Download complete.')
