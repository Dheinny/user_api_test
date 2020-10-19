from mongoengine.errors import NotUniqueError, ValidationError

from apps.responses import(
    resp_already_exists,
    resp_resource_not_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok,
    resp_ok_no_content
)


def check_password_in_signup(password, confirm_password):
    return password == confirm_password


def save_model(model, resource="Resource", desc="Recurso"):
    try:
        return model.save()

    except NotUniqueError as e:
        return resp_already_exists(resource, desc)

    except ValidationError as e:
        return resp_data_invalid(resource, msg=MSG_INVALID_DATA, description=e.__str__())

    except Exception as e:
        return resp_exception(resource, description=e)

    
