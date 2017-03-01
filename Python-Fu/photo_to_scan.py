
## https://github.com/Qetuoadgj/GIMP/blob/master/Python-Fu/photo_to_scan.py | v 1.0.3

# подключение библиотек
import os
import glob

# назначение параметров обработки
mode			= 1
# путь и маска для обрабатываемых файлов (mode == 3)
directory		= "D:\Downloads\GIMP_test\test\"
pattern			= "*.jpg"
# закрывать обработанный файл (mode == 2)
close_files		= 1
# фильтр резкости
sharpen			= [35, 35]
# контрастность для  "тёмных" областей
brightness		= [15, 20]
contrast		= [-25, -10]
# эффект фотокопии
mask_radius		= [8, 16]
pct_white		= [0.16, 0.16]
dimensions		= [1920, 2560]
# эффект "Порог"
low_threshold	= [243, 220]
# отключение фильтров
use_sharpen		= 1
use_contrast	= 1
use_photocopy	= 1
use_threshold	= 1
# каналы для применения резкости
channel_R		= 1
channel_G		= 1
channel_B		= 1
# дополнительный проход
extra_pass		= 1
extra_mix		= 50
# запись истории
enable_undo		= 0

# смена кодировки
directory = directory.encode('cp1251')
pattern = pattern.encode('cp1251')

# функция обработки файлов
def photo_to_scan():
	global enable_undo
	# создание списка обрабатываемых файлов
	file_list = []
	# обрабатывать только текущий открытый файл
	if (mode == 1):
		file_list = [gimp.image_list()[0]]
	# обрабатывать все открытые файлы
	if (mode == 2):
		file_list = gimp.image_list()
		enable_undo	= 0
	# обрабатывать файлы из указанной папки
	if (mode == 3):
		base = os.path.splitext(os.path.basename(pattern))
		extension = base[1]
		mask = base[0]
		file_list = glob.glob(directory + mask)
		enable_undo	= 0
	print(file_list)
	for file in file_list:
		# определяем уже открытый файл
		if (mode == 1):
			image = file
		# определяем уже открытый файл
		if (mode == 2):
			image = file
			# создаём новый файл
			new_image = pdb.gimp_image_duplicate(image)
			# определяем рабочий файл
			image = new_image
			# показываем новый файл в редакторе
			if (close_files < 1):
				display = pdb.gimp_display_new(image)
		# открываем файл с диска
		if (mode == 3):
			# загружаем файл
			image = pdb.gimp_file_load(file, "File Name")
			# показываем загруженный файл в редакторе
			display = pdb.gimp_display_new(image)
		# определяем рабочий слой
		drawable = pdb.gimp_image_get_active_drawable(image)
		# полный путь к файлу
		if (mode == 3):
			filename = pdb.gimp_image_get_filename(image)
		else:
			filename = pdb.gimp_image_get_filename(file)
		# папка файла
		file_directory = os.path.dirname(filename)
		# имя файла
		file_name = os.path.splitext(os.path.basename(filename))[0]
		print("file_name: " + file_name)
		# расширение файла
		file_ext = os.path.splitext(os.path.basename(filename))[1]
		# полный путь к новому файлу
		filename = file_directory + "\\" + file_name + " - GIMP" + file_ext
		print("filename: " + filename)
		# запоминаем "основной" рабочий слой
		original = drawable
		# на время отключаем запись истории
		if (enable_undo < 1):
			disabled = pdb.gimp_image_undo_disable(image)
		# создание рабочих слоёв
		for i in range(0, 2):
			# убираем выделение
			pdb.gimp_selection_none(image)
			# создаём копию основного слоя
			layer = pdb.gimp_layer_copy(original, 0)
			pdb.gimp_image_add_layer(image, layer, 0)
			# переопределяем переменную drawable
			drawable = layer
			# фильтр резкости
			if (use_sharpen > 0):
				pdb.plug_in_sharpen(image, drawable, sharpen[i])
			# яркость / контрастность
			if (use_contrast > 0):
				if (channel_R > 0):
					# создаём копию канала (Красный)
					R = pdb.gimp_channel_new_from_component(image, 2, "R")
					pdb.gimp_image_add_channel(image, R, 0)
					# канал в выделение
					pdb.gimp_image_select_item(image, 2, R)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# удаляем копию канала
					pdb.gimp_image_remove_channel(image, R)
				if (channel_G > 0):
					# создаём копию канала (Зелёный)
					G = pdb.gimp_channel_new_from_component(image, 2, "G")
					pdb.gimp_image_add_channel(image, G, 0)
					# канал в выделение
					pdb.gimp_image_select_item(image, 2, G)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# удаляем копию канала
					pdb.gimp_image_remove_channel(image, G)
				if (channel_B > 0):
					# создаём копию канала (Синий)
					B = pdb.gimp_channel_new_from_component(image, 2, "B")
					pdb.gimp_image_add_channel(image, B, 0)
					# канал в выделение
					pdb.gimp_image_select_item(image, 2, B)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# удаляем копию канала
					pdb.gimp_image_remove_channel(image, B)
			# убираем выделение
			pdb.gimp_selection_none(image)
			# эффект фотокопии
			mask_radius_calculated = 8
			if (use_photocopy > 0):
				width = pdb.gimp_image_width(image)
				height = pdb.gimp_image_height(image)
				# вычисление радиуса маски
				mask_radius_calculated = mask_radius[i]
				if (dimensions > 0):
					mask_radius_calculated = mask_radius[i] * pow(float(width*height) / float(dimensions[0]*dimensions[1]), 0.5)
				# нормализация параметра mask_radius_calculated между 3.0 и 50.0
				mask_radius_calculated = min(mask_radius_calculated, 50.0)
				mask_radius_calculated = max(mask_radius_calculated, 3.0)
				# применение эффекта
				pdb.plug_in_photocopy(image, drawable, mask_radius_calculated, 0.75, 0.50, pct_white[i])
			# применение эффекта "Порог"
			if (use_threshold > 0):
				pdb.gimp_threshold(drawable, low_threshold[i], 255)
			# сведение 2х слоёв
			if (i > 0):
				# прозрачность 50% для верхнего слоя
				pdb.gimp_layer_set_opacity(layer, 50)
				# сведение 2х верхних слоёв
				if (mode == 1):
					layer = pdb.gimp_image_merge_down(image, layer, 1)
				# сведение 2х верхних слоёв
				if (mode == 2):
					layer = pdb.gimp_image_merge_down(image, layer, 1)
				# сведение всех слоёв
				if (mode == 3):
					layer = pdb.gimp_image_flatten(image)
				# применение эффекта "Порог" (перевод в Ч/Б)
				if (use_threshold > 0):
					pdb.gimp_threshold(layer, 254, 255)
				# переопределяем переменную drawable
				drawable = layer
				# дополнительный проход
				if (extra_pass > 0):
					# убираем выделение
					pdb.gimp_selection_none(image)
					# создаём копию основного слоя
					layer = pdb.gimp_layer_copy(original, 0)
					pdb.gimp_image_add_layer(image, layer, 0)
					# прозрачность extra_mix% для верхнего слоя
					pdb.gimp_layer_set_opacity(layer, extra_mix)
					# сведение 2х верхних слоёв
					if (mode == 1):
						layer = pdb.gimp_image_merge_down(image, layer, 1)
					# сведение 2х верхних слоёв
					if (mode == 2):
						layer = pdb.gimp_image_merge_down(image, layer, 1)
					# сведение всех слоёв
					if (mode == 3):
						layer = pdb.gimp_image_flatten(image)
					# применение эффекта "Порог" (перевод в Ч/Б)
					if (use_threshold > 0):
						pdb.gimp_threshold(layer, 128, 255)
					# переопределяем переменную drawable
					drawable = layer
		# включаем запись истории
		if (enable_undo < 1):
			enabled = pdb.gimp_image_undo_enable(image)
		# сохраняем файл
		pdb.gimp_file_save(image, drawable, filename, file_name)
		# закрываем файл
		if (mode == 3):
			pdb.gimp_display_delete(display)
		# закрываем файл
		if (close_files > 0 and mode == 2):
			pdb.gimp_image_delete(image)
		# вывод сообщения
		print("File finished: " + file_name)
		print("mask_radius = " + str(mask_radius_calculated))
	# вывод сообщения
	print("F I N I S H E D")

# запуск функции обработки
photo_to_scan()

