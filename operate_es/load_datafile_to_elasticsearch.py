#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   apolo -- load_datafile_to_elastic_search
@Time    :   2019/12/4 16:42
@Desc    :
读取 csv 或者excel 录入elastic search

查询可用：python DSL (Domain Specific Languages)
https://elasticsearch-dsl.readthedocs.io/en/latest/
'''
#-------------------------------------------------------------------------------
import os
import csv
import datetime
from itertools import islice

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match

import xlrd

import logging
from elasticsearch.helpers import bulk

from apolo_tools.operate_elastic_search import load_datafile_to_elasticsearch_settings as es_settings
from apolo_tools.operate_elastic_search import tool_log

from apolo_common import logger

# log = myLog.Logger('./log/all.log', level='debug')
#
# myLog.Logger('./log/error.log', level='error').logger.error('error')
# log.logger.debug('starting !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')




def delete_es_index(es_instance,index_name):
    '''
    :param index_name: index name
    :return:
    '''
    try:
        #log.logger.info('start to delete index' + index_name)

        #es.index.delete()
        es_instance.indices.delete(index = index_name)
    except Exception as exception:
        pass

        #log.logger.exception(exception)


def add_to_es(es_instance,docs):
    """ add the record to the ES """
    try:

        success, es_res = bulk(es_instance, docs)
        print("performed {0} actions".format(success))
        #LOGGER.info(es_res)
        # print(docs)
    except Exception as exception:
        pass
        #LOGGER.exception(exception)


def insert_excel_data(excel_file_name,index_name,es_type,es_instance,column_name):
    '''
    暂时理解为全部用str 类型
    '''
    try:
        data = xlrd.open_workbook(excel_file_name)
        tables = data.sheets()
        for table in tables:
            nrows = table.nrows
            print(nrows)
            dataset = []
            for i in range(nrows - 1):
                line = table.row_values(i + 1)
                line = [str(field).strip().replace("\t", "") for field in line]

                record = dict(zip(column_name, line))
                doc = {'_index': index_name,'_type': es_type,"_source": record}
                dataset.append(doc)
                if len(dataset) == es_settings.BULK_SZIE:
                    add_to_es(es_instance,dataset)
                    dataset = []
            if dataset:
                add_to_es(es_instance,dataset)

    except Exception as exception:
        pass


def insert_csv_data(csv_file_name,index_name,es_type,es_instance,column_name):
    try:
        csv_reader = csv.reader(open(csv_file_name, encoding='utf-8'))
        dataset = []
        for line in islice(csv_reader, 1, None):

            line = [field.strip() for field in line]

            record = dict(zip(column_name, line))
            doc = {'_index': index_name,'_type': es_type,"_source": record}
            dataset.append(doc)

            if len(dataset) == es_settings.BULK_SZIE:
                add_to_es(es_instance,dataset)
                dataset = []

        if dataset:
            add_to_es(es_instance,dataset)

    except Exception as exception:
        pass

def create_index(es_instance,index_name,index_body,doc_type):
    try:
        # 创建之前先删除索引
        res = delete_es_index(es_instance, index_name)

        res = es_instance.indices.create(index=index_name)
        res = es_instance.indices.put_mapping(index=index_name, body=index_body, doc_type=doc_type, include_type_name=True)
        #log ...
        return  res

    except Exception as exception:
        pass
        #LOGGER.exception(exception)

# def check(*args):
#     print(type(args))
#     for i in args:
#         if (i is None):
#             flag = True
#         else:
#             return False
#     return flag


def create_and_init_index(es_instance,index_name,index_file_name,index_mapper,column_name):
    '''

    :param es_instance: index name
    :param index_name: index name
    :param index_file_name: index name
    :param index_mapper:
    :param column_name: list of column english name
    :return:

    '''

    try:
        res = create_index(es_instance, index_name,index_mapper , 'doc')
        if index_file_name.endswith('.csv'):
            dataset = insert_csv_data(index_file_name, index_name, 'doc', es_instance,column_name)
        if index_file_name.endswith('.xlsx') or index_file_name.endswith('.xls'):
            dataset = insert_excel_data(index_file_name, index_name, 'doc', es_instance,column_name)

    except Exception as exception:
        pass


def query_top_n_disease(es_instance,index_name, query_string,fields_list,size):
    '''

    :param query_string: 查询字符串
    :param fields_list: 需要查询的 字段列表 eg：['add_code','main_code']
    :param size: 返回匹配条目数，默认为 1
    :return: 结果的 dict 格式

    '''
    try:

        multi_match = MultiMatch(query=query_string, fields=fields_list)
        s = Search(using=es_instance, index=index_name).query(multi_match)[0:size]
        s = s.execute()

        return s.to_dict()

    except Exception as exception:
        pass


def unit_test(es_instance,index_name):
    try:
    ## 查询 索引名称为'disease'  疾病名称'name',为 '自行车脚踏车' 相关，的 最相似的第一条记录
        temp = query_top_n_disease(es_instance, index_name, '自行车脚踏车', ['name'], 1)
        result1 = '''{'code': 'V11', 'main_code': 'V11', 'add_code': '', 'name': '骑脚踏车人员在脚踏车与其他脚踏车碰撞中的损伤'}'''
        print(result1)
        print(temp["hits"]['hits'][0]['_source'])
        print(str(temp["hits"]['hits'][0]['_source']) == result1)

    ## 查询 索引名称为'disease'  疾病主编码及辅助编码'add_code', 'main_code',为 'P04' ，的 最相似的第一条记录
        temp = query_top_n_disease(es_instance, index_name, 'P04', ['add_code', 'main_code'], 1)
        result2 = '''{'code': 'P04', 'main_code': 'P04', 'add_code': '', 'name': '胎儿和新生儿受经胎盘或母乳传播的有害物质的影响'}'''
        print(result2)
        print(temp["hits"]['hits'][0]['_source'])
        print(str(temp["hits"]['hits'][0]['_source']) == result2)

    except Exception as exception:
        logger.exception("Exception occurred")
        logger.error("Exception occurred", exc_info=True)
        logger.log(level=logging.DEBUG, msg="Exception occurred", exc_info=True)



def main():
    now_time = datetime.datetime.now()

    # log_name = now_time.strftime('%Y-%m-%d %H-%M-%S') + '.log'
    #
    # log = mylog.Logger(log_name, level='debug')


    es_instance = Elasticsearch(es_settings.es_ip + ':' + es_settings.es_port)

    # index_name = 'disease'
    # index_file_name = r'ICD10_2011_hc.csv'

    index_name = 'hospital'
    index_file_name = '../../db/data/hospital_info.xls'

    #create_and_init_index(es_instance,index_name,index_file_name,es_settings.create_hospital_body,es_settings.HOSPITAL_ENGLISH_COLUMN)

    unit_test(es_instance,index_name)

    logger.error('test tool 20191217')
    logger.error('test tool 20191217=====')
    logger.warning('')

if __name__ == '__main__':
    main()

