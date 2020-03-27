import logging
from hashlib import md5

logger = logging.getLogger(__name__)


class Anonymizer(object):
    """Anonymize string names in an optionally-consistent way."""
    def __init__(self, salt=None):
        if salt is not None and not isinstance(salt, str):
            logger.error("invalid salt: must provide a string. Setting a random salt.")
            salt = None
        if salt is None:
            import secrets
            self._salt = secrets.token_hex(8)
        else:
            self._salt = salt

    @property
    def salt(self):
        return self._salt

    def anonymize(self, string_):
        salted = self._salt + string_
        return md5(salted.encode('utf-8')).hexdigest()

    def anonymize_object_info(self, object_, anonymized_info_dict, ge_classes):
        object_class = object_.__class__
        object_class_name = object_class.__name__

        for ge_class in ge_classes:
            if issubclass(object_class, ge_class):
                anonymized_info_dict["parent_class"] = ge_class.__name__
                if not object_class == ge_class:
                    anonymized_info_dict["anonymized_class"] = self.anonymize(object_class_name)
                break

        if not anonymized_info_dict.get("parent_class"):
            anonymized_info_dict["parent_class"] = "__not_recognized__"
            anonymized_info_dict["anonymized_class"] = self.anonymize(object_class_name)

        return anonymized_info_dict