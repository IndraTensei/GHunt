class gkiaKnowledgeError(BaseException):
    pass

class gkiaCorruptedHeadersError(BaseException):
    pass

class gkiaUnknownVerbError(BaseException):
    pass

class gkiaUnknownRequestDataTypeError(BaseException):
    pass

class gkiaInsufficientCreds(BaseException):
    pass

class gkiaParamsTemplateError(BaseException):
    pass

class gkiaParamsInputError(BaseException):
    pass

class gkiaAPIResponseParsingError(BaseException):
    pass

class gkiaObjectsMergingError(BaseException):
    pass

class gkiaAndroidMasterAuthError(BaseException):
    pass

class gkiaAndroidAppOAuth2Error(BaseException):
    pass

class gkiaOSIDAuthError(BaseException):
    pass

class gkiaCredsNotLoaded(BaseException):
    pass

class gkiaNotAuthenticated(BaseException):
    pass

class gkiaInvalidTarget(BaseException):
    pass