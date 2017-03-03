
## https://github.com/Qetuoadgj/GIMP/blob/master/Python-Fu/photo_to_scan.py | v 1.1.0

# подключение библиотек
import os
import glob
import re

# назначение параметров обработки
mode			= 3
# путь и маска для обрабатываемых файлов (mode == 3)
directory		= "D:\\Downloads\\GIMP_test\\test\\"
pattern			= "*.jpg"
# закрывать обработанный файл (mode == 2)
close_files		= 1
# фильтр резкости
sharpen			= [40, 20]
# осветление для затемнённых областей
brightness		= [45, 60]
contrast		= [-75, -30]
# эффект "Фотокопия"
mask_radius		= [8, 16]
pct_white		= [0.16, 0.16]
dimensions		= [1920, 2560]
# эффект "Порог"
low_threshold	= [243, 220]
# фильтры / эффекты
use_sharpen		= 1
use_contrast	= 1
use_photocopy	= 1
use_threshold	= 1
# дополнительный проход
extra_pass		= 1
extra_mix		= 50
# запись истории
enable_undo		= 0
# конвертация изображения в черно-белое (1 bit), файл будет сохранен в формате *.png
index_to_1bit	= 1

# смена кодировки путей для обработки
directory = directory.encode('cp1251')
pattern = pattern.encode('cp1251')

# функция обработки файлов
def photo_to_scan():
	global enable_undo
	# создание списка обрабатываемых файлов
	file_list = []
	# создание списка обработанных файлов
	files_processed = []
	# создание списка пропущенных файлов
	files_skipped = []
	# если обрабатывается только текущий открытый файл
	if (mode == 1):
		# включить в список обработки только текущий открытый файл
		file_list = [gimp.image_list()[0]]
	# если обрабатываются все открытые в редакторе файлы
	if (mode == 2):
		# включить в список обработки все открытые в редакторе файлы
		file_list = gimp.image_list()
	# если обрабатываются все файлы из указанной папки, подходящие по маске
	if (mode == 3):
		# включить в список обработки все файлы из указанной папки, подходящие по маске
		base = os.path.splitext(os.path.basename(pattern))
		mask = base[0]
		extension = base[1]
		file_list = glob.glob(directory + mask + extension)
	# обработка списка обработки файлов
	for file in file_list:
		# пропуск ранее обработанных файлов
		if (re.match(".* - GIMP", file)):
			# добавляем файл список пропущенных файлов
			files_skipped.append(file)
			# пропускаем обработку файла
			continue
		# если обрабатывается только текущий открытый файл
		if (mode == 1):
			# назначаем файл для обработки
			image = file
		# если обрабатываются все открытые в редакторе файлы
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
		# если обрабатываются все файлы из указанной папки, подходящие по маске
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
		filename = file_directory + "\\" + file_name + " - GIMP - 00" + file_ext
		# запоминаем "основной" рабочий слой для последующего копирования
		original = drawable
		# если включена остановка записи истории (для экономии ресурсов)
		if (enable_undo < 1):
			# на время отключаем запись истории изменений
			disabled = pdb.gimp_image_undo_disable(image)
		
		# переводим изображение в серое
		pdb.gimp_image_convert_grayscale(image)
		is_gray = pdb.gimp_drawable_is_gray(drawable)
		
		if (is_gray):
			# определяем полный путь для сохраняемого файла
			filename = file_directory + "\\" + file_name + " - GIMP - 01" + file_ext
			# сохраняем файл на диск
			pdb.gimp_file_save(image, drawable, filename, file_name)
			
			# создаём копию основного слоя
			layer = pdb.gimp_layer_copy(original, 0)
			# добавляем копию основного слоя к изображению
			pdb.gimp_image_add_layer(image, layer, 0)
			# назначаем drawable (текущий рабочий слой)
			drawable = layer
			
			# создаём копию канала ("Grey")
			channel_grey = pdb.gimp_channel_new_from_component(image, 3, "Grey")
			pdb.gimp_image_add_channel(image, channel_grey, 0)
			# переводим канал в выделение
			pdb.gimp_image_select_item(image, 2, channel_grey)
			# очищаем выделение (осветляем изображение)
			pdb.gimp_edit_clear(drawable)
			# # удаляем копию канала
			# pdb.gimp_image_remove_channel(image, channel_grey)
			
			# полностью снимаем выделение
			pdb.gimp_selection_none(image)
			
			# # определяем полный путь для сохраняемого файла
			# filename = file_directory + "\\" + file_name + " - GIMP - 02" + file_ext
			# # сохраняем файл на диск
			# pdb.gimp_file_save(image, drawable, filename, file_name)
			
			# # применяем эффект "Фотокопия"
			# pdb.plug_in_photocopy(image, drawable, 50, 0.75, 1.0, 0.1)
			
			# применяем контраст
			pdb.gimp_brightness_contrast(drawable, 15, 25)
			
			# определяем полный путь для сохраняемого файла
			filename = file_directory + "\\" + file_name + " - GIMP - 02" + file_ext
			# сохраняем файл на диск
			pdb.gimp_file_save(image, drawable, filename, file_name)
			
			# удаляем более ненужный обработанный и сохранённый слой
			pdb.gimp_image_remove_layer(image, layer)
			
			# создание новых слоёв, их обработка и сведение
			for i in range(0, 2):
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
					# переводим канал "Grey" в выделение
					pdb.gimp_image_select_item(image, 2, channel_grey)
					# обращаем выделение
					pdb.gimp_selection_invert(image)
					# применяем контраст
					pdb.gimp_brightness_contrast(drawable, brightness[i], contrast[i])
					# полностью снимаем выделение
					pdb.gimp_selection_none(image)
				
				# если включён эффект "Фотокопия"
				mask_radius_calculated = 8
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
			
			# устанавливаем прозрачность верхнего слоя равной 50%
			pdb.gimp_layer_set_opacity(layer, 50)
			# сводим оба верхних (обработанных) слоя
			layer = pdb.gimp_image_merge_down(image, layer, 1)
			# переопределяем drawable (текущий рабочий слой)
			drawable = layer
			# если включён эффект "Порог"
			if (use_threshold > 0):
				# применяем эффект "Порог" (придаём изображению черно-белый вид)
				pdb.gimp_threshold(layer, 254, 255)
				
			# # определяем полный путь для сохраняемого файла
			# filename = file_directory + "\\" + file_name + " - GIMP - 04" + file_ext
			# # сохраняем файл на диск
			# pdb.gimp_file_save(image, drawable, filename, file_name)
			
			# если включён дополнительный проход
			if (extra_pass > 0):
				# создаём копию основного слоя
				layer = pdb.gimp_layer_copy(original, 0)
				# добавляем копию основного слоя к изображению
				pdb.gimp_image_add_layer(image, layer, 0)
				# устанавливаем прозрачность для верхнего слоя равной extra_mix
				pdb.gimp_layer_set_opacity(layer, extra_mix)
				# сводим оба верхних (обработанных) слоя
				layer = pdb.gimp_image_merge_down(image, layer, 1)
				# переопределяем drawable (текущий рабочий слой)
				drawable = layer
				# если включён эффект "Порог"
				if (use_threshold > 0):
					# применяем эффект "Порог" (придаём изображению черно-белый вид)
					pdb.gimp_threshold(layer, 128, 255)
				
				# # определяем полный путь для сохраняемого файла
				# filename = file_directory + "\\" + file_name + " - GIMP - 05" + file_ext
				# # сохраняем файл на диск
				# pdb.gimp_file_save(image, drawable, filename, file_name)
			
			# если включена конвертация изображения в черно-белое (1 bit)
			if (index_to_1bit > 0):
				# сводим все слои изображения
				drawable = pdb.gimp_image_flatten(image)
				# установка черно-белой палитры для изображения
				pdb.gimp_image_convert_indexed(image, 0, 3, 2, FALSE, TRUE, "BW")
				# определяем полный путь для сохраняемого файла
				file_ext = ".png"
				filename = file_directory + "\\" + file_name + " - GIMP - 03" + file_ext
				# сохраняем файл на диск
				pdb.gimp_file_save(image, drawable, filename, file_name)	
		
		if (disabled):
			# обратно включаем запись истории (почему-то нужно включать дважды)
			enabled = pdb.gimp_image_undo_enable(image)
			enabled = pdb.gimp_image_undo_enable(image)
		
		# если включено закрывание файлов
		if (close_files > 0):
			# если обрабатываются все открытые в редакторе файлы
			if (mode == 2):
				# закрываем файл
				pdb.gimp_image_delete(image)
			# если обрабатываются все файлы из указанной папки, подходящие по маске
			if (mode == 3):
				# закрываем файл в редакторе
				pdb.gimp_display_delete(display)
		
		# добавляем файл в список обработанных файлов
		files_processed.append(file)
		
		# выводим сообщение о завершении обработки текущего файла
		print("\nФайл обработан: " + file_name)
		
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

# запускаем обработку файлов
photo_to_scan()

