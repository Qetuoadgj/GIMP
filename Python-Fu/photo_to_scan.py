>>> ## https://github.com/Qetuoadgj/GIMP/blob/master/Python-Fu/photo_to_scan.py | v 1.0.6
>>>
# подключение библиотек
import os
import glob
import re
>>>
# назначение параметров обработки
mode			= 3
# путь и маска для обрабатываемых файлов (mode == 3)
directory		= "D:\\Downloads\\GIMP_test\\test\\"
pattern			= "*.jpg"
# закрывать обработанный файл (mode == 2)
close_files		= 1
# фильтр резкости
sharpen			= [40, 40]
# осветление для затемнённых областей
brightness		= [15, 20]
contrast		= [-25, -10]
# эффект "Фотокопия"
mask_radius		= [8, 20]
pct_white		= [0.16, 0.16]
dimensions		= [1920, 2560]
# эффект "Порог"
low_threshold	= [243, 220]
# фильтры / эффекты
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
>>>
# смена кодировки путей для обработки
directory = directory.encode('cp1251')
pattern = pattern.encode('cp1251')
>>>
# функция обработки файлов
def photo_to_scan():
	global enable_undo
	# создание списка обрабатываемых файлов
	file_list = []
	# создание списка обработанных файлов
	files_processed = []
	# создание списка пропущенных файлов
	files_skipped = []
	# создание списка файлов для обработки
	if (mode == 1):
		# включить в список обработки только текущий открытый файл
		file_list = [gimp.image_list()[0]]
	if (mode == 2):
		# включить в список обработки все открытые в редакторе файлы
		file_list = gimp.image_list()
		# отключить запись истории
		enable_undo	= 0
	if (mode == 3):
		# включить в список обработки все файлы из указанной папки, подходящие по по маске
		base = os.path.splitext(os.path.basename(pattern))
		mask = base[0]
		extension = base[1]
		file_list = glob.glob(directory + mask + extension)
		# отключить запись истории
		enable_undo	= 0
	for file in file_list:
		# пропуск ранее обработанных файлов
		if (re.match(".* - GIMP", file)):
			# добавляем файл список пропущенных файлов
			files_skipped.append(file)
			# пропускаем обработку файла
			continue
		if (mode == 1):
			# назначаем файл для обработки
			image = file
		if (mode == 2):
			# назначаем файл для обработки
			image = file
			# создаём копию обрабатываемого файла
			new_image = pdb.gimp_image_duplicate(image)
			# назначаем копию как файл для обработки
			image = new_image
			# если включено закрывание обработанных файлов
			if (close_files < 1):
				# отображаем копию в редакторе
				display = pdb.gimp_display_new(image)
		if (mode == 3):
			# загружаем файл в редактор
			image = pdb.gimp_file_load(file, "File Name")
			# отображаем загруженный файл в редакторе
			display = pdb.gimp_display_new(image)
		# назначаем рабочий слой
		drawable = pdb.gimp_image_get_active_drawable(image)
		# получаем полный путь к файлу
		if (mode == 3):
			# из открытого в редакторе файла
			filename = pdb.gimp_image_get_filename(image)
		else:
			# из списка обрабатываемых файлов
			filename = pdb.gimp_image_get_filename(file)
		# получаем полный путь к папке файла
		file_directory = os.path.dirname(filename)
		# получаем имя файла (без расширения)
		file_name = os.path.splitext(os.path.basename(filename))[0]
		# получаем расширение файла
		file_ext = os.path.splitext(os.path.basename(filename))[1]
		# определяем полный путь для сохраняемого файла
		filename = file_directory + "\\" + file_name + " - GIMP" + file_ext
		# запоминаем "основной" рабочий слой для последующего копирования
		original = drawable
		# если включена остановка записи истории (для экономии ресурсов)
		if (enable_undo < 1):
			# на время отключаем запись истории изменений
			disabled = pdb.gimp_image_undo_disable(image)
		# создание новых слоёв, их обработка и сведение
		for i in range(0, 2):
			# полностью снимаем выделение
			pdb.gimp_selection_none(image)
			# создаём копию основного слоя
			layer = pdb.gimp_layer_copy(original, 0)
			# добавляем копию основного слоя к изображению
			pdb.gimp_image_add_layer(image, layer, 0)
			# назначаем drawable (текущий рабочий слой)
			drawable = layer
			# если включён фильтр резкости
			if (use_sharpen > 0):
				# применяем фильтр резкости
				pdb.plug_in_sharpen(image, drawable, sharpen[i])
			# если включён эффект "яркость / контрастность"
			if (use_contrast > 0):
				# если включена обработка изображения по "Красному" каналу
				if (channel_R > 0):
					# создаём копию канала (Красный)
					R = pdb.gimp_channel_new_from_component(image, 2, "R")
					pdb.gimp_image_add_channel(image, R, 0)
					# переводим канал в выделение
					pdb.gimp_image_select_item(image, 2, R)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# удаляем копию канала
					pdb.gimp_image_remove_channel(image, R)
				# если включена обработка изображения по "Зелёному" каналу
				if (channel_G > 0):
					# создаём копию канала (Зелёный)
					G = pdb.gimp_channel_new_from_component(image, 2, "G")
					pdb.gimp_image_add_channel(image, G, 0)
					# переводим канал в выделение
					pdb.gimp_image_select_item(image, 2, G)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# удаляем копию канала
					pdb.gimp_image_remove_channel(image, G)
				# если включена обработка изображения по "Синему" каналу
				if (channel_B > 0):
					# создаём копию канала (Синий)
					B = pdb.gimp_channel_new_from_component(image, 2, "B")
					pdb.gimp_image_add_channel(image, B, 0)
					# переводим канал в выделение
					pdb.gimp_image_select_item(image, 2, B)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# удаляем копию канала
					pdb.gimp_image_remove_channel(image, B)
			# полностью снимаем выделение
			pdb.gimp_selection_none(image)
			# эффект фотокопии
			mask_radius_calculated = 8
			# если включён эффект "Фотокопия"
			if (use_photocopy > 0):
				# определяем ширину изображения
				width = pdb.gimp_image_width(image)
				# определяем высоту изображения
				height = pdb.gimp_image_height(image)
				# определяем радиус маски эффекта из нашей таблицы значений
				mask_radius_calculated = mask_radius[i]
				# если включена авто коррекция радиуса маски
				if (dimensions > 0):
					# вычисляем радиус маски исходя из размеров изображения
					mask_radius_calculated = mask_radius[i] * pow(float(width*height) / float(dimensions[0]*dimensions[1]), 0.5)
				# устанавливаем верхнее граничное значение радиуса маски равным 50
				mask_radius_calculated = min(mask_radius_calculated, 50.0)
				# устанавливаем нижнее граничное значение радиуса маски равным 3
				mask_radius_calculated = max(mask_radius_calculated, 3.0)
				# применяем эффект "Фотокопия"
				pdb.plug_in_photocopy(image, drawable, mask_radius_calculated, 0.75, 0.50, pct_white[i])
			# если включён эффект "Порог"
			if (use_threshold > 0):
				# применяем эффект "Порог" (придаём изображению максимальную контрастность)
				pdb.gimp_threshold(drawable, low_threshold[i], 255)
			# если обработаны оба слоя
			if (i > 0):
				# устанавливаем прозрачность верхнего слоя равной 50%
				pdb.gimp_layer_set_opacity(layer, 50)
				# если обрабатывается только текущий открытый файл
				if (mode == 1):
					# сводим оба верхних (обработанных) слоя
					layer = pdb.gimp_image_merge_down(image, layer, 1)
				# если обрабатываются все открытые в редакторе файлы
				if (mode == 2):
					# сводим оба верхних (обработанных) слоя
					layer = pdb.gimp_image_merge_down(image, layer, 1)
				# если обрабатываются все файлы из указанной папки, подходящие по по маске
				if (mode == 3):
					# сводим оба верхних (обработанных) слоя
					layer = pdb.gimp_image_merge_down(image, layer, 1)
				# если включён эффект "Порог"
				if (use_threshold > 0):
					# применяем эффект "Порог" (придаём изображению черно-белый вид)
					pdb.gimp_threshold(layer, 254, 255)
				# переопределяем drawable (текущий рабочий слой)
				drawable = layer
				# если включён дополнительный проход
				if (extra_pass > 0):
					# полностью снимаем выделение
					pdb.gimp_selection_none(image)
					# создаём копию основного слоя
					layer = pdb.gimp_layer_copy(original, 0)
					# добавляем копию основного слоя к изображению
					pdb.gimp_image_add_layer(image, layer, 0)
					# устанавливаем прозрачность для верхнего слоя равной extra_mix
					pdb.gimp_layer_set_opacity(layer, extra_mix)
					# если обрабатывается только текущий открытый файл
					if (mode == 1):
						# сводим оба верхних (обработанных) слоя
						layer = pdb.gimp_image_merge_down(image, layer, 1)
					# если обрабатываются все открытые в редакторе файлы
					if (mode == 2):
						# сводим оба верхних (обработанных) слоя
						layer = pdb.gimp_image_merge_down(image, layer, 1)
					# если обрабатываются все файлы из указанной папки, подходящие по по маске
					if (mode == 3):
						# сводим оба верхних (обработанных) слоя
						layer = pdb.gimp_image_merge_down(image, layer, 1)
					# если включён эффект "Порог"
					if (use_threshold > 0):
						# применяем эффект "Порог" (придаём изображению черно-белый вид)
						pdb.gimp_threshold(layer, 128, 255)
					# переопределяем drawable (текущий рабочий слой)
					drawable = layer
		# если была включена остановка записи истории
		if (enable_undo < 1):
			# обратно включаем запись истории
			enabled = pdb.gimp_image_undo_enable(image)
		# сохраняем файл на диск
		pdb.gimp_file_save(image, drawable, filename, file_name)
		# если обрабатываются все файлы из указанной папки, подходящие по по маске
		if (mode == 3):
			# закрываем файл в редакторе
			pdb.gimp_display_delete(display)
		# если включено закрывание файлов и обрабатываются все открытые в редакторе файлы
		if (close_files > 0 and mode == 2):
			# закрываем файл
			pdb.gimp_image_delete(image)
		# добавляем файл в список обработанных файлов
		files_processed.append(file)
		# выводим сообщение о завершении обработки текущего файла
		print("\nФайл обработан: " + file_name)
		# выводим значение радиуса маски (debug)
		print("mask_radius = " + str(mask_radius_calculated))
	# выводим сообщение о завершении обработки всех файлов
	print("\nОбработка файлов завершена.")
	# выводим список обработанных
	print("\nОбработано:")
	for file in files_processed:
		print(file)
	# выводим список пропущенных
	print("\nПропущено:")
	for file in files_skipped:
		print(file)
>>>
# запускаем обработку файлов
photo_to_scan()
>>>
