import os


# Genera los archivos necesarios según los parámetros pasados a la función
def generar_archivo(nombre, archivo):
    # Si no existe el archivo en la carpeta, lo crea.
    if os.path.exists(nombre):
        file = open(nombre, 'w')
        file.write(archivo)
        file.close()
    # En caso contrario, solamente agrega los nuevos contenidos.
    else:
        file = open(nombre, 'a')
        file.write(archivo)
        file.close()


def generar_archivo_por_lineas(nombre, lineas):
    if os.path.exists(nombre):
        file = open(nombre, 'w')
        file.writelines(lineas)
        file.close()
        # En caso contrario, solamente agrega los nuevos contenidos
    else:
        file = open(nombre, 'a')
        file.writelines(lineas)
        file.close()


# Equivalente a la función left de excel.
def left(s, amount):
    return s[:amount]


# Equivalente a la función right de excel.
def right(s, amount):
    return s[-amount:]


# Equivalente a la función mid de excel.
def mid(s, offset, amount):
    return s[offset:offset + amount]


# Equivalente a xlookup de excel, perfecto para realizar cruces
def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = ''):
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return f'"{lookup_value}" not found!' if if_not_found == '' else if_not_found

    else:
        return match_value.tolist()[0]


# Genera una concatenación en formato de base de datos para consulta de tipo
# "in" de un campo establecido en el dataframe
# y lo retorna en forma de texto.
def concatenar_formato_bd(pandas_df, campo) -> str:
    cadena_formatear = ''
    for i, row in pandas_df.iterrows():
        if i == len(pandas_df) - 1:
            cadena_formatear += f"'{row[campo]}'"
        else:
            cadena_formatear += f"'{row[campo]}',"
    return cadena_formatear


# obtiene la quincena de baja en función de la qna introducida, generalmente una quincena abajo, sin embargo,
# calcula cuando es la primera quincena del año.
def obtener_qna_baja(qna):
    return qna - 1 if int(right(str(qna), 2)) > 1 else int(
        str(int(left(
            str(qna), 4)) - 1) + '24')
