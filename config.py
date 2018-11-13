# -*- coding: utf-8 -*-

import os


class Configuracao():

    ws = "C:\\luciano\\arcgis\\data\\ferrari\\Scripts\\" \
                    "exporta_ga_shape\\Banco.gdb"
    fgdb_name = "Banco.gdb"
    fgdb_file = "C:\\luciano\\arcgis\\data\\ferrari\\Scripts\\" \
                "exporta_ga_shape\\Banco.gdb"
    fc_name = "TALHAO"
    fc_file = os.path.join(fgdb_file, fc_name)

    out_path = 'C:\\luciano\\arcgis\\data\\ferrari\\Scripts\\' \
               'exporta_ga_shape\\output'
    fgdb_name_temp = 'BANCO_tmp.gdb'
    fgdb_file_tmp = os.path.join(out_path, fgdb_name_temp)

    fc_name_temp = "TALHAO_tmp"
    fc_file_temp = os.path.join(fgdb_file_tmp, fc_name_temp)

    out_feature_name = 'TALHAO_tmp.shp'
    out_feature_path = os.path.join(out_path, out_feature_name)

    lossless = "Non-lossless compression"