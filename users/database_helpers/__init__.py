from .user import UsersKeeper


def accept_message(message):
    users_conn = UsersKeeper()
    user = message.from_user
    users_conn.update(user.id, user.username,
                         user.first_name, user.last_name)
