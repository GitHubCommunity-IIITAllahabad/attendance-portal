def authenticate_user(username, password, user_authorization):
    import ldap, sys

    server = 'ldap://127.31.1.42:8080'
    connection = ldap.initialize(server)
    connection.protocol_version = ldap.VERSION3
    try:
        connection.start_tls_s()

        if user_authorization == 'professor':
            base_dn = 'ou=Faculty,dc=iiita,dc=ac,dc=in'
        else:
            base_dn = 'ou=Students,dc=iiita,dc=ac,dc=in'

        search_filter = "uid=" + username
        attributes = None

        try:
            result_type, result_data = connection.search_s(base=base_dn, scope=ldap.SCOPE_SUBTREE,
                                                           filterstr=search_filter, attrlist=attributes)
            if len(result_data) == 0:
                return False
            else:
                user_dn = result_data[0][0]

                try:
                    bind_result_id = connection.simple_bind(user_dn, password)
                    bind_result_type, bind_result_data = connection.result(bind_result_id)
                    if bind_result_type == 97:
                        return True
                except ldap.INVALID_CREDENTIALS:
                    print "Invalid Credentials"
                    return False
                finally:
                    connection.unbind()

        except ldap.LDAPError, e:
            print e
            sys.exit()

    except ldap.LDAPError, e:
        print e
        sys.exit()


def get_tokens(total_students, no_of_tokens):
    from django.utils.crypto import get_random_string

    base_token = total_students / no_of_tokens
    a_list = [base_token for _ in range(no_of_tokens)]

    for i in range(total_students % no_of_tokens):
        a_list[i] += 1

    token_list = []

    for no_of_students in a_list:
        token = get_random_string(length=8,
                                  allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        d = {
            "token": token,
            "token_issued": str(no_of_students)
        }
        token_list.append(d)

    return token_list
