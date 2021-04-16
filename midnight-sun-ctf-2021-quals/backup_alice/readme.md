## Title: Backup - Bob
**Points:** 91  
**Solves:** 81

### Descriptions: 
The backup of the home directories might contain too much information

Service: ssh -p2222 backup-01.play.midnightsunctf.se
Download: backup.tar.gz

### Solution:
running `RsaCtfTool/RsaCtfTool.py --publickey .ssh/authorized_keys --private` prints the private key, which can be used to connect to the ssh server and retreive the flag.
