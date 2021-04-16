## Title: Backup - Alice
**Points:** 91  
**Solves:** 82

### Descriptions: 
The backup of the home directories might contain too much information

Service: ssh -p2222 backup-01.play.midnightsunctf.se
Download: backup.tar.gz

### Solution:
There are two public keys in authorized_keys.

We extract the modulus with pycryptodome, and then see that there is a common factor.

```python
import math

n1 = 0x00eff5f6000dd42363b1134a2fb9383c5798ed9c28946ee332fbb38c861cb317572930dcfecf90f398275f10d106769adea169c135670d7652689b82310d57818f474191fbf37f359f2dd15b62d2157e463dce4228f4fd6e1133ea614d29a703d2b3e23db864c367400325ecc68e4a31d137ed53138ac44d304ca722b2958bb4d5a19b2dbcc1042716f987992e1032605d45a0bc978d2131eae70314d13eb9df08ad05adb38779d2d5851df89c473ba57ec96ea3f0f5448b5ab030f1eabb5951202a5a62d6c3f5ee4e6bc4e20914d47b068bd8cc9c5ac0578b32fecfb48d6cbe187ffc5fb4356e07f1997f477c65b7aa73bf29ce5e16a5fa8bd4719c66c2fd8cf1
n2 = 0x00e53d14a1f1c376a9dfa501549fded4271b2ee04a64621fd9364f7a74b555c3df748288968c99fa9e21f40d7bdb152978b5135278ac9d3d06fd1586df138bcc9463907ec0e87424a1883d83310a544ea386b8da9bf888338409f67bed3ea91e6e650e800ae4a0d7bcacb5d7d4ed5e9976ebfd7e158c2bf3b90c8d4fd9ba3007403324c7524652b41f8a960ca95f129b4b9fcaf4e2b4ff4d595ddf5cdb7cdc800e85e61b6c8e2562457f36a51b756d05b4166252e13d11988cd004cb0d8379188584e633829143f940107dfd7e30fa47874a9c6cc8d23bfe0e2c35f1726e374d7fb2b1d869847887bec6b5375f6c4f3b58ffa71d903197b43e184891b485fd8c4b


p = math.gcd(n1,n2)
q = n1//p
e = 0x10001

d = inverse_mod(e,(p-1)*(q-1))

print("n=",n1)
print("p=",p)
print("q=",q)
print("e=",e)
print("d=",d)

```

```python
from Crypto.PublicKey import RSA

n= 30292242746036115971017608982999250727717453656432023769003750409813735934710819201974159210260826408436902577095993755936818096216019228802218008805095250945851943575117108739663821796010390678994297744383588214605732433507054131494086784354478249764431583863823040817137498841468964275285759264488873023055232915029362296237879621242004026789135861602389065223171670193449202825454456361675908992418334133239350991783676572498332103136958336603939895528286642315040568556524401592641941738753256750084061561270732457810477455643729432407190682410033927743753783287469005235658010914542487780332979133840894080158961
p= 171271932272901803774128505983365082675029542666691747200477582499432049482725221456365399113480297074384917169149347993114697250080329906810077468818479458173346323889305093008389190427501456666485586943618415784519402027225089556051642516053179825638237155560833886980519882958785597519492961451928936581189
q= 176866357166853049063661821863387933259117661678458383073695418050077665947238837705599659610321169217662359814277129014996138272302829083941138890846942733275470611626297778550063523219612078877136311507035120322137758493919504728746219706460142413216484996909934940352436565132547185318204637754391138716349
e= 65537
d= 15304430315150248499570686040497553913750287746129983658322522846931391588479941629866585068143891591158494914784403455343149426794156166514644254231129115676153984828657133946915617185524208397884861873663502897200213720583061009016291675187468595266034364913179497146592607597843643684010357126607734175601115245474092119990236356003458527120626241137580787534384073569954403444863526933313078071754271192384335158776738039760390563986544985366286072843618371599436142757880622159296205275039893616989616517015359768932590655535100883090018595132962979215904188675724042994278817743239150298641473776542798417305745

private_key = RSA.construct((n,e,d,p,q),True)

open("id_rsa_sol","wb").write(private_key.export_key("PEM",pkcs=1))```

Using this private key to connect to the service gives us the flag:

midnight{factorization_for_the_Win}