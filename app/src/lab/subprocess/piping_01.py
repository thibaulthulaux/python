# See https://linuxhint.com/python-subprocess-pipes/
# zcat f1.dat.gz f2.dat.gz | pigz > out.gz

import subprocess

p1 = subprocess.Popen(["zcat", "f1.dat.gz", "f2.dat.gz"], stdout=subprocess.PIPE)

fout = open('out.gz', 'wb')

p2 = subprocess.run(['pigz'], stdin=p1.stdout, stdout=fout)

