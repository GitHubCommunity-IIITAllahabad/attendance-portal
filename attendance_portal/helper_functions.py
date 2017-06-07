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
            "students": str(no_of_students)
        }
        token_list.append(d)

    return token_list
