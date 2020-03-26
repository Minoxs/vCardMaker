#!/usr/bin/env python3
import PySimpleGUI as gui
from vcardmaker import *

gui.change_look_and_feel('Dark Blue 3')

layout = [
	[gui.T("Arquivo de Emails",size=(15,1)),gui.In(size=(70,2),key="file"),gui.FilesBrowse("Procurar",file_types=(("Arquivo de Texto","*.txt"),)),gui.T(" "*13),gui.Button("Sair")],
	[gui.T("Salvar em:",size=(15,1)),gui.In(size=(70,2),key="save"),gui.FolderBrowse("Procurar")],
	[gui.Output(size=(112,20))],
	[gui.Button("Confirmar",size=(100,2))]
]

create_save_folder()
window = gui.Window("vCardMaker",layout)

while True:
	event, values = window.read()
	if event in (None,"Sair"):
		break
	if event == "Confirmar":
		get_file = values['file']
		get_save_folder = values['save']
		if get_file.strip() == "":
			print("Selecione o arquivo .txt de emails.")
			continue
		if get_save_folder.strip() == "":
			print("Caminho para salvar não especificado.")
			continue

		all_files = get_file.split(";")
		all_emails = []
		for file in all_files:
			group_name = file[file.rfind("/")+1:file.find(".txt")]

			email_list = abrir(file)

			#checkForDuplicate = True
			#if checkForDuplicate:
			#	all_emails = check_for_duplicate(all_emails , email_list, group_name)	

			status = generate_vcard(email_list,get_save_folder,group_name)
			print(status)
			loc = window.CurrentLocation()
		gui.Popup("vCards Gerado com Sucesso!",location=(loc[0]+200,loc[1]+100),keep_on_top=True,title="Sucesso!")

window.Close()