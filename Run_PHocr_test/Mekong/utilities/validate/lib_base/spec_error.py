# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      22/02/2019

class SpecError(object):
    """
    Present error when validate spec.json file.
    """
    def __init__(self, message):
        self.fields = list()
        self.message = message

    def to_dict(self):
        """
        Get error in dictionary type
        :return:
        dict
            error in dict
        """
        return {
            "error_field": " > ".join(self.fields),
            "message": self.message
        }

    def to_tuple(self):
        """
        Get error in tuple type
        :return:
        dict
            error in tuple
        """
        return (" > ".join(self.fields), self.message)

    def append_field(self, field):
        """
        Add meta field to present root of the field has the error.
        This function must be call correct order to make a right path to field.
        Example:
        spec.json > tags > Language
        :param field: name of field/root field
        :return:
        None
        """
        self.fields.insert(0, field)
