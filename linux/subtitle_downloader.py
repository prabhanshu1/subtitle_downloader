from opensubapi  import OpenSubtitles
import wx
import sys
import os
import requests
import zipfile
import urllib
import wx.lib.agw.genericmessagedialog as GMD

app=wx.App()
win=wx.Frame(None,title="subtitle",size=(200,1000))
panel=wx.Panel(win)

selected = os.environ.get('NAUTILUS_SCRIPT_SELECTED_URIS', '')    #get the selected file name
curdir = os.environ.get('NAUTILUS_SCRIPT_CURRENT_URI', os.curdir)  #get the directory name



op=OpenSubtitles()

op.login()


file_name=selected[7:-1]   #for linux to cut "file://"
file_name=urllib.unquote(file_name)
hash =op.getHash(file_name)

size=op.getSize(file_name)

search=op.searchSubtitle(hash,size)

if search is False :

    ins="Try to Rename the file name ,such that there is no special character."
    ins=ins+"\n"+"If that do not work the I can not help you out"
    instruction=GMD.GenericMessageDialog(None,ins,'Subtitle_downloader',agwStyle=wx.ICON_INFORMATION|wx.OK)
    ins_ans= instruction.ShowModal()
    instruction.Destroy()
    exit()
arr=[]
for x in search:
    arr.append(x["SubFileName"])

chooseonebox=wx.SingleChoiceDialog(None,"Which sub you want",
                                   "which one?",arr)

if chooseonebox.ShowModal() == wx.ID_OK:
    sub_choice=chooseonebox.GetStringSelection()

sub_arr=[]
for x in search:
    if x["SubFileName"] ==sub_choice:
        sub_arr.append(x["ZipDownloadLink"])

print "downloading with requests"
for url in sub_arr:
    r = requests.get(url)
    with open("subtitle.zip", "wb") as code:
        code.write(r.content)

    fh = open("subtitle.zip", 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        fileName,fileExtension =os.path.splitext(name)
        if fileExtension !=".srt":
            continue

        z.extract(name)
    fh.close()
    os.remove("subtitle.zip")


#win.Show()
#app.MainLoop()
exit(sub_arr)


