import subprocess
import sys
from multiprocessing import Pool
import urllib.request

if len(sys.argv) <= 1:
    print('error, no url provided')
    exit(1)
url = sys.argv[1]
if not url.startswith('http'):
    print('error, no url provided')
    exit(1)

req = urllib.request.Request(url, method='HEAD')
f = urllib.request.urlopen(req)
lenth = int(f.headers['Content-Length'])
num_of_process = 8 
subprocess.call('rm -rf tmp_fast_download_dir', shell=True)
subprocess.call('mkdir -p tmp_fast_download_dir', shell=True)
def download(i):
    # the ith process
    sub_file_name = 'tmp_fast_download_dir/tmp_fast_download'+str(i)+'.bin'
    sub_log_name = 'tmp_fast_download_dir/tmp_fast_download'+str(i)+'.log'
    begin = (i*lenth)//num_of_process
    end = ((i+1)*lenth)//num_of_process - 1
    if end == lenth-1: end = lenth
    rangestr = str(begin)+'-'+str(end)
    cmd = 'curl -o '+sub_file_name+' -r '+rangestr+' '+url+' 2> '+sub_log_name
    print(cmd)
    subprocess.call(cmd, shell=True)


p = Pool(num_of_process)
p.map(download, range(num_of_process))
