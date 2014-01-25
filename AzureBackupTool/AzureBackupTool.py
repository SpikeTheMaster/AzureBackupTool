from azure.storage import BlobService
import platform
from datetime import datetime

regVPS = 'Backups\\VPSName'

pathToZip = ''
sevenZip = ''
fileName = 'Backup_'+timeStamp+'.7z'

timeStamp = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

if platform.system() == 'Windows' :
    pathToZip = 'C:\\SQLBackups\\' + fileName
    sevenZip = 'C:\\SQLBackups\\7Zip\\7za.exe'
else:
    # sudo apt-get install p7zip-full
    pathToZip = '/var/tmp/'+fileName
    sevenZip = '7z'

#Create archive.7z containing Backups Directory with max compression
zipArgs = "mx9 a "+ pathToZip +" Backups"

subprocess.call(sevenZip + " " + zipArgs)

blob_service = BlobService(account_name, account_key)
blob_service.create_container('Backups')

blob_service.create_container(regVPS)

blob_service.put_block_blob_from_path(regVPS, fileName, pathToZip)

