import configparser


def generate_config():
    config_file = configparser.ConfigParser()
    config_file.add_section("ConexionDB")
    config_file.set("ConexionDB", "db_url", "127.0.0.1")
    config_file.set("ConexionDB", "db_user", "root")
    config_file.set("ConexionDB", "db_password", "")
    config_file.set("ConexionDB", "db_port", "3306")
    with open(r"settings.ini", 'w') as configFileObj:
        config_file.write(configFileObj)
        configFileObj.flush()
        configFileObj.close()
        print("archivo de configuración generado.")


def read_config():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config
