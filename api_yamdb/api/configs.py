

CONFIG = {
    'name_max_length': 256,
    'slug_max_length': 50,
    'title_name_max_length': 256,
    'score_min_value': 1,
    'score_max_value': 10
}


USER_CONFIG = {
    'username_max_length': 150,
    'email_max_length': 254,
    'first_name_max_length': 150,
    'last_name_max_length': 150,
    'role_max_length': 154,
    'confirmation_code_max_length': 254
}

MAIL_CONFIG = {
    'new_user_mail_subject': 'Подтверждение регистрации на YaMDb',
    'new_user_message': ('{username}! Приветствуем вас на YaMDb. '
                         'Ваш код подтверждения - {code}'),
    'user_mail_subject': 'Запрос кода подтверждения YaMDb',
    'user_mail_message': ('Доброго времени суток, {username}! '
                          'Ваш код подтверждения - {code}')
}
