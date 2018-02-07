import wget
import os

link = 'ftp://speedtest.tele2.net/'
filename = '100KB.zip'

wget.download(link + filename)

os.system('rm -rv {}'.format(filename))
