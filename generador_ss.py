import configparser
from datetime import date

import pandas
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy import create_engine

from utilerias import concatenar_formato_bd, generar_archivo

headers = ['No.', 'FOLIO', 'rfc', 'nombre', 'plaza', 'Sindicato', 'QNA DE INI'
           ]


class FormatoLayoutExcelException(Exception):
    """Excepción lanzada cuando el formato del excel introducido es diferente al que se debe usar.

    Attributes:
        formato_recibido — columnas que se recibieron en el archivo
        message — explicación del error
    """

    def campos_a_texto(self, headers):
        campos = ''
        for i in headers:
            if i == len(headers):
                campos += f"'{i}'"
            else:
                campos += f"'{i}',"
        return campos

    def __init__(self, formato_recibido):
        self.formato_recibido = formato_recibido
        self.message = f'El layout recibido es incorrecto se introdujo las columnas: ' \
                       f'{self.campos_a_texto(self.formato_recibido)}\n' \
                       f'las columnas correctas son: {self.campos_a_texto(headers)}'

    def __str__(self):
        return self.message

    pass


def generar_archivos_ss(qna, archivo):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    qna_proceso = qna
    # lee la relación a cargar
    relacion_ss = pandas.read_excel(archivo)
    # genera la conexión a la base de datos.
    if not relacion_ss.columns.tolist() == headers:
        raise FormatoLayoutExcelException(relacion_ss.columns)

    try:
        engine = create_engine(f"mysql+pymysql://{config['ConexionDB']['db_user']}"
                               f":{config['ConexionDB']['db_password']}"
                               f"@{config['ConexionDB']['db_url']}"
                               f":{config['ConexionDB']['db_port']}/a713ap00")
        # genera la cadena de texto con rfcs para buscar si no existe un ss activo.
        rfc_ss = concatenar_formato_bd(relacion_ss, 'rfc')
        # busca los empleados en la tabla de conceptos para ver si ya cuentan con el concepto SS.
        encontrados = pandas.read_sql(f"select * from emp_plaza_cpto where concepto = 'SS'"
                                      f" and rfc in ({rfc_ss}) and qna_fin >={qna_proceso}", engine)
    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(f'ocurrió un error al conectarse a la base de datos: {e}\n'
                               f'favor de revisar su conexión a la base de datos.')
        msg.setWindowTitle("Error")
        msg.exec_()
    else:
        # genera outer join buscando los valores nulos en la columna de concepto.
        pendientes = relacion_ss.merge(encontrados, on='rfc', how='outer').query("importe != 0 and concepto != 'SS'")
        pendientes['u_version'] = ''
        pendientes['cod_pago'] = 0
        pendientes['unidad'] = 0
        pendientes['subunidad'] = 0
        pendientes['cat_puesto'] = 0
        pendientes['horas'] = 0
        pendientes['cons_plaza'] = 0
        pendientes['perc_ded'] = 'D'
        pendientes['concepto'] = 'SS'
        pendientes['qna_fin'] = 999999
        pendientes['qna_ini'] = pendientes['QNA DE INI']
        pendientes['importe'] = 0
        pendientes['num_doc'] = pendientes['FOLIO']
        pendientes['fec_doc'] = date.today().strftime('%Y-%m-%d %H:%M:%S')
        pendientes['ban_ins_cpto'] = 'M'
        pendientes['ban_tipo_cpto_ep'] = 0
        pendientes['num_aplic'] = 1

        texto_carga = ''
        for i, x in pendientes.iterrows():
            texto_carga += "|".join(map(str, x[7:24].values.tolist())) + '\n'

        try:
            pendientes.to_excel(f'salidas/reporte_ss_{qna_proceso}_salida.xlsx', index=False)
        except PermissionError:
            print(
                f"no se pudo generar el archivo 'reporte_ss_{qna_proceso}_salida.xlsx, "
                f"posiblemente el archivo se encuentre abierto")
        generar_archivo(f'salidas/carga_ss_{qna_proceso}.txt', texto_carga)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Registros generados")
        msg.setInformativeText(
            f'generados {len(pendientes)} registros para cargar en el sistema\n Lo puedes consultar el archivo'
            f' salidas/carga_ss_{qna_proceso}.txt')
        msg.setWindowTitle("Acción Exitosa!")
        msg.exec_()
