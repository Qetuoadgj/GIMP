## https://github.com/Qetuoadgj/GIMP/blob/master/Python-Fu/photo_to_scan.py | v 1.0.0

# подключение библиотек
import os
import glob

# назначение параметров обработки
mode			= 1
close_files		= 1
sharpen			= [8, 8]
contrast		= [-80, -25]
mask_radius		= [8, 8]
pct_white		= [0.16, 0.16]
low_threshold	= [243, 220]
dimensions		= [1740, 2463]
# dimensions		= False

directory = "D:\\Downloads\\GIMP_test\\test\\"
pattern = "*.jpg"

# создание списка обрабатываемых файлов
file_list = []

# обрабатывать только текущий открытый файл
if (mode == 1):
	file_list = [gimp.image_list()[0]]

# обрабатывать все открытые файлы
if (mode == 2):
	file_list = gimp.image_list()

# обрабатывать файлы из указанной папки
if (mode == 3):
	base = os.path.splitext(os.path.basename(pattern))
	extension = base[1]
	mask = base[0]
	file_list = glob.glob(directory + mask)

print(file_list)

# ОБРАБОТКА ФАЙЛОВ
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
		pdb.plug_in_sharpen(image, drawable, sharpen[i])
		# создаём копию канала (Синий)
		B = pdb.gimp_channel_new_from_component(image, 2, "B")
		pdb.gimp_image_add_channel(image, B, 0)
		# канал в выделение
		pdb.gimp_image_select_item(image, 2, B)
		# обращаем выделение
		pdb.gimp_selection_invert(image)
		# применяем контраст
		pdb.gimp_brightness_contrast(drawable, 0, contrast[i])
		# удаляем копию канала
		pdb.gimp_image_remove_channel(image, B)
		# убираем выделение
		pdb.gimp_selection_none(image)
		# эффект фотокопии
		width = pdb.gimp_image_width(image)
		height = pdb.gimp_image_height(image)
		# вычисление радиуса маски
		if (dimensions):
			mask_radius_calculated = mask_radius[i] * pow(float(width*height) / float(dimensions[0]*dimensions[1]), 0.5)
		else:
			mask_radius_calculated = mask_radius[i]
		# нормализация параметра mask_radius_calculated между 3.0 и 50.0
		mask_radius_calculated = min(mask_radius_calculated, 50.0)
		mask_radius_calculated = max(mask_radius_calculated, 3.0)
		# применение эффекта
		pdb.plug_in_photocopy(image, drawable, mask_radius_calculated, 0.75, 0.50, pct_white[i])
		# применение эффекта "Порог"
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
			pdb.gimp_threshold(layer, 254, 255)
			# переопределяем переменную drawable
			drawable = layer
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

