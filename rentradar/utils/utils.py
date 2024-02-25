import uuid


def string_to_uuid(input_string):
    namespace = uuid.NAMESPACE_DNS
    result_uuid = uuid.uuid5(namespace, input_string)
    return result_uuid
