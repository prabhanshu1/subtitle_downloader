import xmlrpclib
import os,struct
import wx
import wx.lib.agw.genericmessagedialog as GMD
class OpenSubtitles:
    useragent='OSTestUserAgent'
    url='http://api.opensubtitles.org/xml-rpc'
    token=None

    def __init__(self):
        self.server=xmlrpclib.ServerProxy(self.url)

    def login(self,username='',password='',language='en'):

        try:
            response=self.server.LogIn(username,password,language,self.useragent)
            os.system("pause")
            if response['status']=='200 OK':
                self.token=response['token']

        except:
            ins="Maybe Your Computer is NOT Connected to Internet"
            ins=ins+"\n"+"Or, Authentication not done ."
            instruction=GMD.GenericMessageDialog(None,ins,'Subtitle_downloader',agwStyle=wx.ICON_INFORMATION|wx.OK)
            ins_ans= instruction.ShowModal()
            instruction.Destroy()
            exit()

    def searchSubtitle(self,hash,size,sublanguage='eng'):
        result=self.server.SearchSubtitles(self.token,[{'moviehash':str(hash),'moviebytesize':str(size),'sublanguageid':sublanguage}])
        return result['data']

    def getSize(self,filename):
        return os.path.getsize(filename)

    def getHash(self,filename):
        # http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
        try:
            longlongformat = 'q'  # long long
            bytesize = struct.calcsize(longlongformat)

            f = open(filename, 'rb')
            filesize = os.path.getsize(filename)
            hash = filesize

            maxSize = 65536
            if filesize < (maxSize-1) * 2:
                return "SizeError"

            for x in range(maxSize/bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

            f.seek(max(0, filesize-maxSize), 0)
            for x in range(maxSize/bytesize):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

            f.close()
            returnedhash = "%016x" % hash
            return returnedhash

        except (IOError):
            return "IOError"
