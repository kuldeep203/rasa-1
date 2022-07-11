import ldap
from flask_simpleldap import LDAP

username = "11964@tcplcoe.com"
# logger = logging.getLogger(__name__)
# app.config['LDAP_HOST'] = '172.16.19.20'
# app.config['LDAP_BASE_DN'] = 'CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_USERNAME'] = 'CN=Administrator,CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_PASSWORD'] = 'Xanadu@@12345'

dn = "cn=11964,dc=tcploe,dc=com"


def authenticate(address, username, password):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn.simple_bind_s(username, password)
#
#
# y = authenticate("172.16.19.20", "CN=Administrator,CN=Users,DC=tcplcoe,DC=com","Xanadu@@12345")
#
# y = authenticate("172.16.19.20",username,'Newton&123')
#
# for i in y:
#     print(i)

#
#
# def authenticate(address, username, password):
#     conn = ldap.initialize('ldap://' + address)
#     conn.protocol_version = 3
#     conn.set_option(ldap.OPT_REFERRALS, 0)
#     try:
#         result = conn.simple_bind_s(username, password)
#     except ldap.INVALID_CREDENTIALS:
#         return "Invalid credentials"
#     except ldap.SERVER_DOWN:
#         return "Server down"
#     except ldap.LDAPError as \
#             e:
#         if type(e.message) == dict and e.message.has_key('desc'):
#             return "Other LDAP error: " + e.message['desc']
#         else:
#             return "Other LDAP error: " + e
#     finally:
#         conn.unbind_s()
#     return "Succesfully authenticated"
#
#
# y = authenticate("172.16.19.20", "CN=Administrator,CN=Users,DC=tcplcoe,DC=com", "Xanadu@@12345")
# y = authenticate("172.16.19.20", "CN=11964,CN=Users,DC=tcplcoe,DC=com", "Newton&123")
# print(y)




y  = "11964@tcplcoe.com"
x  = y.split("@")
print(x)

