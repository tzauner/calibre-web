import sys
import os
import requests
from flask import Flask
from werkzeug.datastructures import FileStorage


# global config 
upload_REST_url = 'http://localhost:8083/upload'
scan_dir        = './scandir/'
file_ext        = {'pdf','epub'} # use a tuple () instead ?
# end

app = Flask(__name__)

def upload_book(file_name):
    try:
        with open(file_name,'rb') as fd:
            file_store  = FileStorage(fd,name=file_name,content_type='application/pdf') # epub should be application/epub+zip
            url         = upload_REST_url
            payload     = {'btn-upload':file_store}
            http_status = requests.post(url,files=payload)
            if http_status.status_code == 200:
                print('successfully uploaded book: ', file_name)
                fd.close()
                print('removing local copy: ', file_name)
                os.remove(file_name)
            else:
                print('HTTP response error uploading book:', file_name)
                print(http_status)
    except IOError as e:
        print ('I/O error filename: ', file_name,' ', e.strerror)
    except: #handle other exceptions such as attribute errors
        print ('unexpected error:', sys.exc_info()[0])
    ret = 0
    return ret

def main():
    print('scanning for new ebooks')
    included_extensions = ['.pdf','.epub']
    file_names = [fn for fn in os.listdir(scan_dir) if any (fn.endswith(ext) for ext in included_extensions)]
    #print(file_names)
    for new_book in file_names:
        print('Uploading new booKk: ',scan_dir+new_book)
        upload_book(scan_dir+new_book)
    print('scan/upload finished')        
        
   # TEST WITH flask test_client - NOT WORKING
   # with app.test_client() as client:
   #     response= client.post("http://localhost:8083/upload")
   #     fd = open('/home/tom/Calibre/calibre-web/new.pdf','rb')
   #     file_store = FileStorage(fd,name='new.pdf',content_type='application/pdf')
   #     #myreq= request
   #     #setattr(myreq.files,"btn-upload",file_store)
   #     #print(myreq.path)
   #     url   = 'http://localhost:8083/upload'
   #     #payload = {'file': open('/home/tom/Calibre/calibre-web/new.pdf', 'rb'),'btn-upload':file_store}
   #     payload = {'btn-upload':file_store}
   #     s     = requests.post(url,files=payload)
   #     print(s)
    
if __name__ == '__main__':
    main()
