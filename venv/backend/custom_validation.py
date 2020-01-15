import re


class validate_coupon_UID(object):
    """
    Validates whether coupon UID is unique
    """

    def __init__(self, message=None):
        self.__message = message

    def __call__(self, form, field):
        if not field.raw_data or not field.raw_data[0]:
            if self.__message is None:
                message = field.gettext("Coupon UID is not unique")
            else:
                message = self.__message

            field.errors[:] = []
            raise StopValidation(message)
