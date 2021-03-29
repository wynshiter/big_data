#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   apolo -- load_datafile_to_elasticsearch_settings
@Time    :   2019/12/6 15:46
@Desc    :

'''
#-------------------------------------------------------------------------------

es_ip = '52.82.33.89'
es_port = '9200'
ES_INDEX = 'disease'
ES_TYPE = 'doc'
BULK_SZIE = 500

# DISEASE_CHINESE_NAME = ["疾病名称","主要编码","附加编码","一级编码","二级编码","三级编码","四级编码","一级描述","二级描述","三级描述","四级描述"]
#
#
# DISEASE_ENGLISH_NAME = ["iz_disease_code","disease_name", "main_code", "additional_code", "code_level1", "code_level2", "code_level3", "code_level4",
#            "description_level1", "description_level2", "description_level3", "description_level4"]

DISEASE_ENGLISH_NAME = ['code','main_code','add_code','name']

create_disease_body = {
    "properties": {
        "code": {
            "type": "keyword"
        },
        "main_code": {
            "type": "keyword"
        },
        "add_code": {
            "type": "keyword"
        },
        "name": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        }


    }
}

# MEDICINES_CHINESE_COLUMN=[
#     "批准文号","产品名称","英文名称","商品名称","剂型","规格","生产单位","生产地址","产品类型","原批准文号","批准日期","药品本位码","药品本位码备注"]
#
#
# MEDICINES_ENGLISH_COLUMN=[
# "approval_number","medical_product_name","english_name","general_product_name","formula","specification","manufacturing_unit",
#     "production_address","product_type","original_approval_number","approval_date","drug_standard_number", "drug_standard_number_remark"]

# HOSPITAL_CHINESE_COLUMN=[]
#
# HOSPITAL_ENGLISH_COLUMN=["id_hospital_library","hospital_name","hospital_grade","address","zipcode","phone_number","fax",
# "contact_person_name","url","roadline","special_info","introduction","area_code","country_code","province_code","city_code",
#                          "area_district","is_valid","english_full_name","english_abbr_name","english_address","general_code",
#                          "remark","registered_capital","bed_num","employees_num","patient_departments_num","year_business_income"]

HOSPITAL_CHINESE_COLUMN=[]
HOSPITAL_ENGLISH_COLUMN=['code','circ_code','name','alias','province','city','county','address','phone','zipcode','home_url','type','grade']
create_hospital_body = {
    "properties": {
        "code": {
            "type": "keyword"
        },
        "circ_code": {
            "type": "keyword"
        },
        "name": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        },
        "alias": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        },
        "province": {
            "type": "keyword"
        },
        "city": {
            "type": "keyword"
        },
        "county": {
            "type": "keyword"
        },
        "address": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        },
        "phone": {
            "type": "keyword"
        },
        "zipcode": {
            "type": "keyword"
        },
        "home_url": {
            "type": "keyword"
        },
        "type": {
            "type": "keyword"
        },
        "grade": {
            "type": "keyword"
        }
    }
}

# create_disease_body = {
#     "properties": {
#         "disease_name": {
#             "type": "text",
#             "analyzer": "hanlp_standard",
#             "search_analyzer": "hanlp_speed"
#         },
#         "main_code": {
#             "type": "keyword"
#         },
#         "additional_code": {
#             "type": "keyword"
#         },
#         "code_level1": {
#             "type": "keyword"
#         },
#         "code_level2": {
#             "type": "keyword"
#         },
#         "code_level3": {
#             "type": "keyword"
#         },
#         "code_level4": {
#             "type": "keyword"
#         },
#         "description_level1": {
#             "type": "text",
#             "analyzer": "hanlp_standard",
#             "search_analyzer": "hanlp_speed"
#         },
#         "description_level2": {
#             "type": "text",
#             "analyzer": "hanlp_standard",
#             "search_analyzer": "hanlp_speed"
#         },
#         "description_level3": {
#             "type": "text",
#             "analyzer": "hanlp_standard",
#             "search_analyzer": "hanlp_speed"
#         },
#         "description_level4": {
#             "type": "text",
#             "analyzer": "hanlp_standard",
#             "search_analyzer": "hanlp_speed"
#         }
#     }
# }


# create_medicine_body = {
#     "properties": {
#         "medicine": {
#             "type": "text",
#             "analyzer": "hanlp_standard",
#             "search_analyzer": "hanlp_speed"
#         },
#         "approval_number": {
#             "type": "keyword"
#         },
#         "medical_product_name": {
#             "type": "text"
#         },
#         "english_name": {
#             "type": "keyword"
#         },
#         "general_product_name": {
#             "type": "keyword"
#         },
#         "formula": {
#             "type": "keyword"
#         },
#         "specification": {
#             "type": "keyword"
#         },
#         "manufacturing_unit": {
#             "type": "text"
#         },
#         "production_address": {
#             "type": "text"
#         },
#         "product_type": {
#             "type": "keyword"
#         },
#         "original_approval_number": {
#             "type": "keyword"
#         },
#         "approval_date": {
#             "type": "date"
#         },
#         "drug_standard_number": {
#             "type": "keyword"
#         },
#         "drug_standard_number_remark": {
#             "type": "keyword"
#         }
#     }
# }


body = {
    "properties": {
        "name": {
            "type": "text",
            "analyzer": "hanlp_standard",
            "search_analyzer": "hanlp_speed"
        }
    }
}
