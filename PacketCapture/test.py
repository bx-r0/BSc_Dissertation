import wget
import os

link = 'ftp://speedtest.tele2.net/'
filename = '5MB.zip'

wget.download(link + filename)

os.system('rm -rv {}'.format(filename))
