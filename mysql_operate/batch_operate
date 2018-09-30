# -*- coding:utf-8 -*-
import pymysql
import json


def sql_operate(config):
    db = pymysql.connect(
        host='192.168.0.102',
        database='zcb_jz',
        user='root',
        passwd='root!local@1305')

    cursor = db.cursor()
    sql = "SELECT a.id,	a.tel,a.NAME FROM system_account a"
    cursor.execute(sql)
    list = cursor.fetchall()
    update_sql = "UPDATE system_account SET tel = '#tel', password = '670B14728AD9902AECBA32E22FA4F6BD' WHERE id = '#id'"

    try:
        for index, data in enumerate(list):
            id = data[0]
            tel = '1' + str(index).rjust(10, '0')
            up_sql = update_sql.replace('#tel', tel).replace('#id', id)
            # cursor.execute(up_sql)
        db.commit()
    except :
        db.rollback()
        print('更新发生了异常')

    print('共计', len(list), '条数据')

    cursor.close()
    db.close()

def read_json(path):
    with open(path, 'r') as f:
        temp = json.loads(f.read())
        return temp


if __name__ == '__main__':
    config = read_json('config.json')
    sql_operate(config)
    read_json('config.json')
