#!/usr/bin/env python3
import PySimpleGUI as gui
from vcardmaker import *

#change colour of GUI's background
gui.change_look_and_feel('Dark Blue 3')

layout = [
	[gui.T("Agora é possível selecionar vários emails de uma vez!")],
	[gui.T("O Nome do vCard será definido pelo arquivo da lista de emails!")],
	[gui.T("Arquivo de Emails",size=(15,1)),gui.In(size=(70,2),key="file"),gui.FilesBrowse("Procurar",file_types=(("Arquivo de Texto","*.txt"),))],
	[gui.T("Salvar em:",size=(15,1)),gui.In(size=(70,2),key="save"),gui.FolderBrowse("Procurar")],
	[gui.Checkbox("Checar existencia de emails duplicados", key="dupe_check")],
	[gui.Checkbox("Criar lista adicional única com todos emails", key="group_emails_check")],
	[gui.Output(size=(112,20))],
	[gui.Button("Confirmar",size=(100,2))],
	[gui.T("Versão 3.1", text_color="dark gray"), gui.Button("Sair",size=(10,1))]
]

create_save_folder() #creates save folder if one doesn't exist already
window = gui.Window("vCardMaker",layout)

while True:
	event, values = window.read()
	if event in (None,"Sair"):
		break
	if event == "Confirmar":
		#gets input values
		get_file = values['file']
		get_save_folder = values['save']
		checkForDuplicate = values['dupe_check']
		doCreateAllEmailCard = values['group_emails_check']
		#if anything is empty, throws a soft error
		if get_file.strip() == "":
			print("Selecione o arquivo .txt de emails.")
			continue
		if get_save_folder.strip() == "":
			print("Caminho para salvar não especificado.")
			continue

		#get_file is a giant string with filepaths separated by ;
		#use string.split() to turn into a list of strings (of filepaths to email list)
		all_files = get_file.split(";")
		all_emails = [[],[]] #all_emails[0] holds group name and #all_emails[1] holds emails
		for file in all_files:
			group_name = file[file.rfind("/")+1:file.find(".txt")] #gets group name from the filepath itself
			email_list = abrir(file)

			if checkForDuplicate:
				all_emails = check_for_duplicate(all_emails , email_list, group_name)	

			status = generate_vcard(email_list,get_save_folder,group_name)
			print(status)
		
		if doCreateAllEmailCard:
			status = generate_vcard(all_emails[1], get_save_folder, all_emails[0])
			print(status)

		loc = window.CurrentLocation()
		gui.Popup("vCards Gerado com Sucesso!",location=(loc[0]+200,loc[1]+100),keep_on_top=True,title="Sucesso!")

window.Close()