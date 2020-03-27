#!/usr/bin/env python3
import PySimpleGUI as gui
from vcardmaker import *

gui.change_look_and_feel('Dark Blue 3')

layout = [
	[gui.T("Arquivo de Emails",size=(15,1)),gui.In(size=(48,2),key="file"),gui.FileBrowse("Procurar",file_types=(("Arquivo de Texto","*.txt"),)),gui.T(" "*24),gui.Button("Sair")],
	[gui.T("Salvar em:",size=(15,1)),gui.In(size=(48,2),key="save"),gui.FolderBrowse("Procurar")],
	[gui.T("Nome do Grupo:",size=(15,1)),gui.In(size=(48,2),key="group")],
	[gui.Output(size=(100,15))],
	[gui.Button("Confirmar",size=(99,2))],
	[gui.T("Version 2.0", text_color="dark grey")]
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
		get_group_name = values['group']
		if get_file.strip() == "":
			print("Selecione o arquivo .txt de emails.")
			continue
		if get_save_folder.strip() == "":
			print("Caminho para salvar não especificado.")
			continue
		if get_group_name.strip() == "":
			print("Nome do Grupo não especificado.")
			continue
		email_list = abrir(get_file)
		status = generate_vcard(email_list,get_save_folder,get_group_name)
		print(status)
		loc = window.CurrentLocation()
		gui.Popup(status,location=(loc[0]+200,loc[1]+100),keep_on_top=True,title="Sucesso!")

window.Close()