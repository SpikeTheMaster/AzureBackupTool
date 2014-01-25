from azure.storage import BlobService
import platform
from datetime import datetime
import subprocess

regVPS = 'backupsregvps'
DOVPS = 'backupsredsearch'

timeStamp = datetime.today().strftime("%Y-%m-%dT%H%M%SZ")

pathToZip = ''
sevenZip = ''
fileName = 'Backup_'+timeStamp+'.7z'
activeContainer = ''

if platform.system() == 'Windows' :
    pathToZip = 'C:\\SQLBackups\\' + fileName
    sevenZip = 'C:\\SQLBackups\\7Zip\\7za.exe'
    activeContainer = regVPS
else:
    # sudo apt-get install p7zip-full
    pathToZip = '/var/tmp/'+fileName
    sevenZip = '7z'
    activeContainer = DOVPS

#Create archive.7z containing Backups Directory with max compression
zipArgs = "a "+ pathToZip +" Backups -mx9"

subprocess.call(sevenZip + " " + zipArgs)

blob_service = BlobService('storageAccountName', 'storageKey')

blob_service.create_container(regVPS)
blob_service.create_container(DOVPS)

blob_service.put_block_blob_from_path(activeContainer, fileName, pathToZip)

