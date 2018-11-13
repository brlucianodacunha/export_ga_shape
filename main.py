# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
import os
import sys
import config


class ShapefileExport:

    def __init__(self, config):
        self.conf = config.Configuracao

    def execute(self):

        env.workspace = self.conf.ws

        fgdb_name = self.conf.fgdb_name
        fgdb_file = self.conf.fgdb_file
        fc_name = self.conf.fc_name
        fc_file = self.conf.fc_file

        out_path = self.conf.out_path
        fgdb_name_temp = self.conf.fgdb_name_temp
        fgdb_file_tmp = self.conf.fgdb_file_tmp

        fc_name_temp = self.conf.fc_name_temp
        fc_file_temp = self.conf.fc_file_temp

        out_feature_name = self.conf.out_feature_name
        out_feature_path = self.conf.out_feature_path

        lossless = self.conf.lossless

        try:
            if arcpy.Exists(fgdb_file_tmp):
                arcpy.CompressFileGeodatabaseData_management(fgdb_file_tmp,
                                                             lossless)
                arcpy.Delete_management(fgdb_file_tmp)

            # Process: Create File GDB
            arcpy.CreateFileGDB_management(out_path, fgdb_name_temp, 'CURRENT')

            # Process: Create Feature Class
            template_name = 'TEMPLATE.shp'
            template_file = os.path.join(out_path, template_name)
            coordinate_system = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984'," \
                                "SPHEROID['WGS_1984',6378137.0,298.257223563]]," \
                                "PRIMEM['Greenwich',0.0],UNIT['Degree'," \
                                "0.0174532925199433]];" \
                                "-400 -400 1000000000;-100000 10000;" \
                                "-100000 10000;" \
                                "8,98315284119522E-09;0,001;0,001;IsHighPrecision "

            arcpy.CreateFeatureclass_management(
                fgdb_file_tmp, fc_name_temp, "POLYGON", template_file, "DISABLED",
                "DISABLED", coordinate_system, "", "0", "0", "0")

            # Process: Append
            field_mappings = arcpy.FieldMappings()
            # Add target dataset
            field_mappings.addTable(os.path.join(fgdb_file_tmp, fc_name_temp))
            # Add append dataset
            field_mappings.addTable(fc_file)

            arcpy.Append_management(
                fc_file, os.path.join(fgdb_file_tmp, fc_name_temp), "NO_TEST",
                "", "")

            # Process: Calculate Field
            field_name = "ZONA"
            exp_value = "valor()"
            block_value = "def valor(): return '01'"
            lang_value = "PYTHON_9.3"

            arcpy.CalculateField_management(
                in_table=fc_file_temp, field=field_name, expression=exp_value,
                expression_type=lang_value, code_block=block_value
            )

            field_name = "ULT_ALTE"
            exp_value = "ts()"
            lang_value = "PYTHON_9.3"
            block_value = "def ts():\\n import time\\n return time.strftime(" \
                          "\"%Y-%m-%d %H:%M:%S\", time.localtime())"

            arcpy.CalculateField_management(
                in_table=fc_file_temp, field=field_name, expression=exp_value,
                expression_type=lang_value, code_block=block_value)

            # Process: Create Feature Class
            if arcpy.Exists(out_feature_path):
                arcpy.Delete_management(out_feature_path)

            arcpy.FeatureClassToFeatureClass_conversion(
                os.path.join(fgdb_file_tmp, fc_name_temp), out_path,
                out_feature_name)

        except Exception:
            arcpy.AddMessage('Erro ao processar.')
            e = sys.exc_info()[1]
            arcpy.AddError(e.args[0])
        else:
            arcpy.AddMessage('Finalizado com sucesso!')


if __name__ == '__main__':
    shapefileExport = ShapefileExport(config)
    shapefileExport.execute()
