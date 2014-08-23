import uuid
import platform
import time
import win32api
import win32file
import win32pdh
import socket
import os
import win32com.shell.shell as shell

### BASIC INFO ###

print "Date and time: " + time.ctime(time.time())
print "Random id: " + str(uuid.uuid4())
print "Computer name: " + platform.node()
print "OS: " + platform.system()
print "Machine type: " + platform.machine()
print "Windows version: " + platform.platform()
print "Current User: " + win32api.GetUserName()
print "IP adress: " + socket.gethostbyname(platform.node())

### RUNNING PROCESSES ###
#SOURCE: http://www.blog.pythonlibrary.org/2010/10/03/how-to-find-and-list-all-running-processes-with-python/#
#slightly modified by Joren

def procids():
    """Returns a list with all running processes and their pids."""
    #each instance is a process, you can have multiple processes w/same name
    junk, instances = win32pdh.EnumObjectItems(None,None,'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids=[]
    proc_dict={}

    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] += 1
        else:
            proc_dict[instance] = 0

    for instance, max_instances in proc_dict.items():
        for inum in xrange(max_instances+1):
            hq = win32pdh.OpenQuery() # initializes the query handle 
            path = win32pdh.MakeCounterPath( (None,'process',instance, None, inum,'ID Process') )
            counter_handle=win32pdh.AddCounter(hq, path) 
            win32pdh.CollectQueryData(hq) #collects data for the counter 
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance,str(val)))
            win32pdh.CloseQuery(hq) 
 
    return proc_ids

print
print "Running processes:"
for i in procids():
    print i


### ALL DRIVES ###

##Drive types
##0 Unknown
##1 No Root Directory
##2 Removable Disk
##3 Local Disk
##4 Network Drive
##5 CD
##6 RAM Disk
drives = win32api.GetLogicalDriveStrings()
drives = [i for i in drives.split("\000") if i != ""]

print 
print "Interesting Drives:"
for i in drives:
    drivetype = win32file.GetDriveType(i)
    if drivetype in range(2,5):
        print i

### PORT SCANNER ###
### Some of my old code, not the best port scanner code could be improved

localip = socket.gethostbyname(platform.node())
iprange24 = ".".join(localip.split(".")[:3])

ports = sorted([53,21,22,23,80,8080,443,3389,445])

print 
for i in range(256):
    ip = iprange24 + "." + str(i)
    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(.005)
            if sock.connect_ex((ip, port)) == 0:
                print "Open port: " + ip + ":" + str(port)
            sock.close()
        
    except socket.error, socket.gaierror:
        pass

### FILE LISTER ###
folder = 'C:\\Temp\\'

print 
print "Contents of " + folder
for root, dirs, files in os.walk(folder):
    for file in files:
        print os.path.join(root, file)

### Execute javascript in windows via python ###
### Explanation: http://thisissecurity.net/2014/08/20/poweliks-command-line-confusion/
shell.ShellExecuteEx(lpFile="rundll32.exe", lpParameters = 'javascript:"\..\mshtml,RunHTMLApplication ";alert("foo");')
