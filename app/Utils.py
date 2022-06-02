
import sqlite3

def package_license(ls):
    if len(ls) == 0:
        return None
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    res = []
    for i in range(len(ls)):
        info = ls[i]
        pac = info[0]
        ver = info[1]
        
        cursor = c.execute("SELECT license_expression,licenses_summary,version,name FROM package where name like '%"+pac+"%'")
        dic = {}
        tmp = []
        for row in cursor:
            dic['name'] = row[-1]
            dic['version'] = row[-2]
            dic['license_expression'] = row[0]
            dic['licenses_summary'] = row[1]

            tmp.append(dic)

        res.append(tmp)
    conn.close()
    return res

def license_detail(ls):
    if len(ls) == 0:
        return None
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    res = []

    for i in range(len(ls)):
        lic = ls[i]
        dic = {}

        cursor = c.execute("SELECT display_name,key,name,short_name,category,license_style,full_text,tags FROM license where key = '"+lic+"'")
        for row in cursor:
            dic["display_name"] = row[0]
            dic["key"] = row[1]
            dic["name"] = row[2]
            dic["short_name"] = row[3]
            dic["category"] = row[4]
            dic["license_style"] = row[5]
            dic["full_text"] = row[6]
            dic["tags"] = row[7]
            break

        res.append(dic)
    # cursor = c.execute("SELECT display_name,short_name,key FROM license LIMIT 10")
    # for row in cursor:
    #     res.append(row)

    conn.close()
    return res

if __name__ == "__main__":
    # for i in package_license([("torch",None),("numpy",None)]):
    #     print(i,'\n\n')
    for i in license_detail(['apache-2.0','bsd-new']):
        print(i['tags'],'\n\n')
        
    