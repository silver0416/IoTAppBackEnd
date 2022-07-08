import pymysql
from pymysql import cursors
import dns.resolver
import yaml
with open('secret.yml', 'r') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)

def connectMySQL():
    try:
        domain = secret['account']['domain']
        srvInfo = {}
        srv_records=dns.resolver.resolve('_sql._tcp.'+domain, 'SRV')
        for srv in srv_records:
            srvInfo['port']= srv.port
        port = srvInfo['port']
        setting = {
            "host": domain,"port":port, "user": secret['account']['username'], "password": secret['account']['password'], "charset": "utf8" 
        }
        sql = pymysql.connect(**setting)
        return sql

    except Exception as e:
        print(e)
