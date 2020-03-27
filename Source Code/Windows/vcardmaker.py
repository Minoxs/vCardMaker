from pathlib import Path as find

#function that prints to a file with extension .vcf
def printer(add_to_log,save_location, extension = ".vcf"):
	path = save_location+extension
	p = open(path, "a+")
	p.write(str(add_to_log) + "\n")
	p.close()

#unpacks .txt into a list containing all emails
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
	except:
		print(150*"\n")
		print("Arquivo Inválido!")
		return 0
	return emails

#function to create a default save folder if one doesn't exist already
def create_save_folder():
	find(str(find.cwd())+"/Save").mkdir(parents=True,exist_ok=True) 

def check_for_duplicate(email_list, emails_to_add, group_name):
	for new_email in emails_to_add:
		for i in range(len(email_list[1])):
			if new_email == email_list[1][i]:
				print("Duplicações devem ser resolvidas manualmente")
				print("Email {} Já existe".format(new_email))
				print("Grupos {} e {}".format(email_list[0][i], group_name))
		email_list[0].append(group_name) #em email_list[0] estão o nome do grupo
		email_list[1].append(new_email)	 #em email_list[1] está o email da pessoa
	return email_list

#function to generate vCards
def generate_vcard(emails,save_path,group_name):
	
	#if group_name is a list, means each email can have a different group name
	#useful for making the card with every email
	group_list = None #initializing variable for later use if necessary
	if type(group_name) is list:
		group_list = list(group_name)
		group_name = "TodosContatos"

	vcard_filename = "contatos_{}".format(group_name)
	save_location = "{}/{}".format(save_path,vcard_filename)

	#vCard naming portion
	j = 1
	temp = save_location
	while find(save_location+".vcf").exists():
		save_location = "{}({})".format(temp,j)
		j += 1
	del temp
	#if vCard exists, adds (n) to the end of name, where n is how many vCards with that name exists
	if j > 1:
		print(2*"\n")
		print("Arquivo vCard já existe!")
		print("Novo nome do vCard: {}({})".format(vcard_filename,j-1))
		print(2*"\n")

	#vCard creation portion
	check = 0
	prob = 0
	for i in range(len(emails)):
		#error check portion of email
		if emails[i].strip() == "":
			continue
		elif emails[i].count("@") > 1:
			print("\n")
			print("ERRO!")
			print("Há mais de um email na linha número {}".format(i+1))
			print("Exemplo: {}".format(emails[i]))
			print("\n")
			printer(emails[i],save_location+"_problemas",".txt")
			prob += 1
			continue
		elif emails[i].count("@") < 1:
			print("\n")
			print("ERRO!")
			print("Não há um email válido na linha número {}".format(i+1))
			print("Exemplo: {}".format(emails[i]))
			print("\n")
			printer(emails[i],save_location+"_problemas",".txt")
			prob += 1
			continue
		#vCard is being created here
		printer("BEGIN:VCARD",save_location)
		printer("VERSION:3.0",save_location)
		if group_name.strip() != "":
			if group_list is not None:
				group_name = group_list[i]
			printer("FN:{} - {}".format(group_name, emails[i]),save_location)
		elif group_name.strip() =="":
			printer("FN:{}".format(emails[i]),save_location)
		printer("EMAIL;type=INTERNET:{}".format(emails[i]),save_location)
		printer("END:VCARD",save_location)
		check += 1
	#creates new list of emails without any problems
	if prob >= 1:
		for i in range(len(emails)):
			if emails[i].count("@") == 1:
				printer(emails[i],save_location+"_clean",".txt")

	if check > 0:
		return "Arquivo salvo em {}.vcf".format(save_location)
	elif check == 0:
		return "Arquivo de vCards vazio; Apenas arquivo de problemas criado."