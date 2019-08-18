##Initial Checks and Important variables############################################################################################################################
lb = "\n"
import platform
import datetime
from pathlib import Path as find
error_msg = "Something went Wrong!"

#Função que detecta e diz o sistema quando compilado
def os_detect():
	sys = platform.system()
	plt = platform.release()
	os_name = "{} {}".format(sys,plt)
	print("Sistema Operacional: "+os_name)

os_detect()

#Função que define aonde será salvo logs
def set_filepath(save_to = "not_set"):
	saving = str(find.cwd())+"\\"
	return saving

filepath = set_filepath()
print("Pasta atual: "+filepath)

time_now = datetime.datetime.now()
print("Data: "+str(time_now))

##Funções############################################################################################################################
#Adiciona o que acontece em um .txt
def printer(add_to_log, title = "log", extension = ".vcf"):
	path = filepath+str(title)+extension
	p = open(path, "a+")
	p.write(str(add_to_log) + lb)
	p.close()

#####################################################################################
print(150*"\n")
print("Pasta atual: {}".format(filepath))
print("(Certifique-se que o arquivo contendo os emails está na mesma pasta que esse executável!)")
arq = input("Qual o nome do arquivo que contém os emails? ")

def abrir():
	global arq
	global hre
	try:
		h = open(filepath+arq+".txt")
		hre = h.readlines()
		h.close()
	except:
		print(150*"\n")
		print("Arquivo de emails não encontrado!")
		print("Pasta atual: {}".format(filepath))
		print("(Certifique-se que o arquivo contendo os emails está na mesma pasta que esse executável!)")
		arq = input("Qual o nome do arquivo que contém os emails? ")
		abrir()

abrir()

grupo = input("Qual o grupo ao qual os contatos serão inseridos? ")

find("{}vcard\\".format(filepath)).mkdir(parents=True, exist_ok=True)
save_path = "{}vcard\\".format(filepath)

#g = open(filepath+"nomes.txt")
#gre = g.readlines()
#g.close()

#names = []
emails = []

#for i in gre:
#	names.append(i.strip("\n"))

for i in hre:
	emails.append(i.strip("\n").lower().strip().strip(";").strip(".").strip(',').strip(":"))

fin = "contatos_{}".format(grupo)
place = "vcard\\{}".format(fin)

j = 1

while find(filepath+place+".vcf").exists():
	place = "vcard\\{}({})".format(fin,j)
	j += 1

if j > 1:
	print(3*"\n")
	print("Arquivo vCard já existe!")
	print("Novo nome do vCard: {}({})".format(fin,j-1))
	print(3*"\n")

for i in range(len(emails)):
	if emails[i].strip() == "":
		continue
	if emails[i].count("@") > 1:
		print(2*"\n")
		print("ERRO!")
		print("Há mais de um email na linha número {}".format(i+1))
		print("Exemplo: {}".format(emails[i]))
		print(2*"\n")
		printer(emails[i],place+"_problemas",".txt")
		continue
	if emails[i].count("@") < 1:
		print(2*"\n")
		print("ERRO!")
		print("Não há um email válido na linha número {}".format(i+1))
		print("Exemplo: {}".format(emails[i]))
		print(2*"\n")
		printer(emails[i],place+"_problemas",".txt")
		continue
	printer("BEGIN:VCARD",place)
	printer("VERSION:3.0",place)
	if grupo.strip() != "":
		printer("FN:{} - {}".format(grupo, emails[i]),place)
	elif grupo.strip() =="":
		printer("FN:{}".format(emails[i]),place)
	printer("EMAIL;type=INTERNET:{}".format(emails[i]),place)
	printer("END:VCARD",place)

print("Arquivo salvo em {}{}.vcf".format(filepath,place))
a = input("Pressione ENTER para sair.")