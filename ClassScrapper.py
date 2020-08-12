from urllib.request import urlopen
import ssl
import os
import datetime
import json

class baseScrapper():

    @staticmethod
    def jsonfile(dictPDFs):
        pt = os.getcwd()
        with os.fdopen(os.open(os.path.join(pt, 'decretos.json'), os.O_WRONLY | os.O_CREAT), 'w') as fd:
        #os.chmod(os.path.join(pt, 'decretos.json'), 777)
        #with open('decretos.json','w+') as fd:
            fd.write(json.dumps(dictPDFs)) 

    @staticmethod
    def printdict(dictPDFs):
        for key, val  in dictPDFs.items():
            print(f' title: {key}')  
            print(f' link: {val}')
        print("length dict :",len(dictPDFs))

    @staticmethod
    def checkWithTxt(dictPDFs):
        index = 0
        with open('decretos.txt', 'a+') as fd:
            fd.write('**'*100 + '\n')
            fd.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            fd.write('\n')
            for title, urls in dictPDFs.items():
                index += 1
                fd.write(f'{index}.) {title}\n\n')
                for otherindex, url in enumerate(urls):
                    fd.write (f'\t{otherindex + 1}.) {url}\n')
                fd.write('\n')
            fd.write('**'*100 + '\n')
    
    @staticmethod
    def gotPDFs(dictPDFs, folder="Decretos_Covid"):
        '''
        gotPDFS as you can see for the name of this method the main functionality is got the PDF throw
        a request with a dictionary that has a link to do the request and the name of the PDF

        1.) do a contex to forgot the problem about the ssl certificate in the request 
        2.) create a folder in the current directory with the name that you want
        2.) then use a urlib to do a request over eachone link
        3.) open the file in write binary and write the chunk got in the request into the PDF file
        4.) finally if this steps fail print the name of the file that NOT FOUND 

        ''' 
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(path):
            os.mkdir(path)
        for key,url in dictPDFs.items():
            response = urlopen(url, context=ctx)
            try:
                with open(os.path.join(path, key), 'wb+') as fd:
                    while True:
                        chunk = response.read(2000)
                        if not chunk:
                            break
                        fd.write(chunk)
            except:
                print(f'NOT FOUND: {key}')
                continue