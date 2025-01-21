import xmlrpc.client
import csv

url = 'http://localhost:8069'
db = 'odoo17_developement'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid=common.authenticate(db,username,password,{})

if uid:
    print("Authenticate Success")
else:
    print("Authenticate Failed")
    
    
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# partners= models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'john@gamil.com']]])

# partners_count= models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])

# partners_rec= models.execute_kw(db, uid, password, 'res.partner', 'read',[partners], {'fields':['id','name']})

# s_read= models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[]],{'fields':['id','name']})


# create a user
# vals={
#     'name':'DanteVergil',
#     'email':'dante@gmail.com'
# }
# create_id=models.execute_kw(db,uid,password,'res.partner','create',[vals])
# print(create_id)

#write user
# write_id=models.execute_kw(db,uid,password,'res.partner','write',[[10],{'mobile':'9870054321','function':'Developer'}])
# print(write_id)


#delete user
# del_id=models.execute_kw(db,uid,password,'res.partner','unlink',[[10]])
# print(del_id)



#creating csv
header=['Id','Name']
patient_list=[]

s_read= models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[]],{'fields':['id','name']})

for x in s_read:
    vals=[x['id'],x['name']]
    patient_list.append(vals)
    
print(patient_list)  
with open('exp.csv','w') as f:
    writer=csv.writer(f)
    writer.writerow(header)
    writer.writerows(patient_list)
    


# print(partners)
# print(partners_count)
# print(partners_rec)
# print(s_read)