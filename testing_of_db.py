import data_base

def try_add_field(db, tg_id, login, password):
    try:
        db.add_field(tg_id, login, password)
    except:
        return 1
    else:
        return 0

def if_field_was_added(db, tg_id):
    if db.if_id_exist(tg_id):
        return 0
    else:
        return 1

def if_data_was_added_correctly(db, tg_id, login, password):
    if (login, password) == db.get_login_password(tg_id):
        return 0
    else:
        return 1

def field_is_not_repeated(db, tg_id, login, password):
    db.add_field(tg_id, login, password)
    if db.collection.count_documents({"telegram_id": tg_id}) == 1:
        return 0
    else:
        return 1

def field_is_correctly_deleted(db, tg_id):
    db.delete_field(tg_id)
    if db.if_id_exist(tg_id):
        return 1
    else:
        return 0

def unexisting_field_is_not_found(db, tg_id):
    if db.if_id_exist(tg_id):
        return 1
    else:
        return 0

def testing():
    db = data_base.DataBase()
    tg_id = 12345
    password = "password"
    login = "login"

    errors = 0
    errors += try_add_field(db, tg_id, login, password)
    errors += if_field_was_added(db, tg_id)
    errors += if_data_was_added_correctly(db, tg_id, login, password)
    errors += field_is_not_repeated(db, tg_id, login, password)
    errors += field_is_correctly_deleted(db, tg_id)
    errors += unexisting_field_is_not_found(db, tg_id)
    
    return errors


if __name__ == "__main__":
    errors = testing()
    print("Testing has ended with", errors, "failed tests")