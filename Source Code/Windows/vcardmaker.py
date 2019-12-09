#!/usr/bin/env python3
lb = "\n"
from pathlib import Path as find
from collections import Counter
error_msg = "Something went Wrong!"

def printer(add_to_log,save_location, extension = ".vcf"):
	path = save_location+extension
	p = open(path, "a+")
	p.write(str(add_to_log) + lb)
	p.close()

def abrir(path_to_txt):
	emails = []
	try:
		h = open(path_to_txt)
		hre = h.readlines()
		h.close()
		for i in hre:
			emails.append(i.strip("\n").lower().strip().strip(";").strip(".").strip(',').strip(":").strip())
		if len(emails) == 0:
			print("Arquivo de emails vazio!")
			return 0
		dup_test = Counter(emails)
		for i in dup_test:
			if dup_test[i] > 1:
				for j in range(dup_test[i]-1):
					emails.remove(i)
	except:
		print(150*"\n")
		print("Arquivo Inválido!")
		return 0
	return emails

def create_save_folder():
	find(str(find.cwd())+"\\Save").mkdir(parents=True,exist_ok=True)

def generate_vcard(emails,save_path,group_name):
	vcard_filename = "contatos_{}".format(group_name)
	save_location = "{}\\{}".format(save_path,vcard_filename)

	j = 1

	while find(save_location+".vcf").exists():
		save_location = "{}({})".format(save_location,j)
		j += 1

	if j > 1:
		print(2*"\n")
		print("Arquivo vCard já existe!")
		print("Novo nome do vCard: {}({})".format(vcard_filename,j-1))
		print(2*"\n")

	check = 0
	prob = 0
	for i in range(len(emails)):
		if emails[i].strip() == "":
			continue
		if emails[i].count("@") > 1:
			print("\n")
			print("ERRO!")
			print("Há mais de um email na linha número {}".format(i+1))
			print("Exemplo: {}".format(emails[i]))
			print("\n")
			printer(emails[i],save_location+"_problemas",".txt")
			prob += 1
			continue
		if emails[i].count("@") < 1:
			print("\n")
			print("ERRO!")
			print("Não há um email válido na linha número {}".format(i+1))
			print("Exemplo: {}".format(emails[i]))
			print("\n")
			printer(emails[i],save_location+"_problemas",".txt")
			prob += 1
			continue
		printer("BEGIN:VCARD",save_location)
		printer("VERSION:3.0",save_location)
		if group_name.strip() != "":
			printer("FN:{} - {}".format(group_name, emails[i]),save_location)
		elif group_name.strip() =="":
			printer("FN:{}".format(emails[i]),save_location)
		printer("EMAIL;type=INTERNET:{}".format(emails[i]),save_location)
		printer("END:VCARD",save_location)
		check += 1

	if prob >= 1:
		for i in range(len(emails)):
			if emails[i].count("@") == 1:
				printer(emails[i],save_location+"_clean",".txt")

	if check > 0:
		return "Arquivo salvo em {}.vcf".format(save_location)
	elif check == 0:
		return "Arquivo de vCards vazio; Apenas arquivo de problemas criado."