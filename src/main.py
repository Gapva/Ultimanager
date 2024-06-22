import dearpygui.dearpygui as dpg
import os
import shutil

dpg.create_context()

appdata_path = os.getenv('APPDATA')
ultimanager_path = os.path.join(appdata_path, 'Ultimanager')
disabled_dir = os.path.join(ultimanager_path, 'disabled')
path_file = os.path.join(ultimanager_path, 'path.txt')

def initialize_directories():
	os.makedirs(disabled_dir, exist_ok=True)
	if not os.path.exists(path_file):
		with open(path_file, 'w') as f:
			f.write('')

def read_last_used_path():
	if os.path.exists(path_file):
		with open(path_file, 'r') as f:
			return f.read().strip()
	return "A:\\my\\path"

def save_last_used_path(path):
	with open(path_file, 'w') as f:
		f.write(path)

initialize_directories()
last_used_path = read_last_used_path()

def refresh_mod_list(mod_dir):
	enabled_mods = [d for d in os.listdir(mod_dir) if os.path.isdir(os.path.join(mod_dir, d))]
	disabled_mods = [d for d in os.listdir(disabled_dir) if os.path.isdir(os.path.join(disabled_dir, d))]
	
	dpg.configure_item("enabled_mods_list", items=enabled_mods)
	dpg.configure_item("disabled_mods_list", items=disabled_mods)
	dpg.configure_item("moddir", default_path=mod_dir)

def disable_mod(sender, app_data, user_data):
	selected_mod = dpg.get_value("enabled_mods_list")
	mod_dir = dpg.get_value("usermoddir")
	
	if selected_mod:
		src = os.path.join(mod_dir, selected_mod)
		dest = os.path.join(disabled_dir, selected_mod)
		
		if os.path.exists(src):
			shutil.move(src, dest)
			refresh_mod_list(mod_dir)

def enable_mod(sender, app_data, user_data):
	selected_mod = dpg.get_value("disabled_mods_list")
	mod_dir = dpg.get_value("usermoddir")
	
	if selected_mod:
		src = os.path.join(disabled_dir, selected_mod)
		dest = os.path.join(mod_dir, selected_mod)
		
		if os.path.exists(src):
			shutil.move(src, dest)
			refresh_mod_list(mod_dir)

def ok_callback(sender, app_data):
	mod_dir = app_data.get("file_path_name")
	dpg.set_value("usermoddir", mod_dir)
	save_last_used_path(mod_dir)
	refresh_mod_list(mod_dir)

def no_callback(sender, app_data):
	print("user canceled mod directory selection")

def center_dialog():
	main_width, main_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
	
	dialog_width, dialog_height = 478, 254
	
	x_pos = (main_width - dialog_width) // 2
	y_pos = (main_height - dialog_height) // 2
	
	try: dpg.set_item_pos("moddir", [x_pos, y_pos])
	except SystemError: pass

def popup():
	dpg.show_item("moddir")
	center_dialog()

with dpg.theme() as global_theme:
	with dpg.theme_component(dpg.mvAll):
		dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

with dpg.window(label="SSBU Mods Manager", tag="main", width=600, height=400):
	dpg.add_file_dialog(
		directory_selector=True, show=False, callback=ok_callback, tag="moddir",
		cancel_callback=no_callback, width=478, height=254
	)
	
	with dpg.group(horizontal=True):
		dpg.add_text("SSBU Mods Path:")
		dpg.add_input_text(label="", tag="usermoddir", width=256, default_value=last_used_path)
		dpg.add_button(label="Browse", callback=popup)

	dpg.add_spacer(height=4)

	with dpg.group(horizontal=True):
		with dpg.group():
			dpg.add_text("Enabled Mods")
			dpg.add_listbox([], tag="enabled_mods_list", width=220, num_items=10)
		
		with dpg.group():
			dpg.add_spacer(height=82)
			dpg.add_button(label=">", callback=disable_mod)
			dpg.add_button(label="<", callback=enable_mod)
		
		with dpg.group():
			dpg.add_text("Disabled Mods")
			dpg.add_listbox([], tag="disabled_mods_list", width=220, num_items=10)
	
	if len(dpg.get_value("usermoddir")) > 0:
		refresh_mod_list(dpg.get_value("usermoddir"))

dpg.create_viewport(title="Ultimanager", width=502, height=290)
dpg.bind_theme(global_theme)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
