# -*- coding: utf-8 -*-
"""
Demo script for Dynamic Entries (see RFC 2589)

This needs the following software:
Python
pyasn1
pyasn1-modules
python-ldap 2.4+
"""
from __future__ import print_function

from pyldap.extop.dds import RefreshRequest,RefreshResponse

import sys,pyldap,ldapurl,getpass

try:
  ldap_url = ldapurl.LDAPUrl(sys.argv[1])
  request_ttl = int(sys.argv[2])
except (IndexError, ValueError):
  print('Usage: dds.py <LDAP URL> <TTL>')
  sys.exit(1)

# Set debugging level
#pyldap.set_option(pyldap.OPT_DEBUG_LEVEL,255)
ldapmodule_trace_level = 2
ldapmodule_trace_file = sys.stderr

ldap_conn = pyldap.ldapobject.LDAPObject(
  ldap_url.initializeUrl(),
  trace_level=ldapmodule_trace_level,
  trace_file=ldapmodule_trace_file
)

if ldap_url.cred is None:
  print('Password for %s:' % (repr(ldap_url.who)))
  ldap_url.cred = getpass.getpass()

try:
  ldap_conn.simple_bind_s(ldap_url.who or '',ldap_url.cred or '')

except pyldap.INVALID_CREDENTIALS as e:
  print('Simple bind failed:',str(e))
  sys.exit(1)

else:
  extreq = RefreshRequest(entryName=ldap_url.dn,requestTtl=request_ttl)
  try:
    extop_resp_obj = ldap_conn.extop_s(extreq,extop_resp_class=RefreshResponse)
  except pyldap.LDAPError as e:
    print(str(e))
  else:
    if extop_resp_obj.responseTtl!=request_ttl:
      print('Different response TTL:',extop_resp_obj.responseTtl)
    else:
      print('Response TTL:',extop_resp_obj.responseTtl)
