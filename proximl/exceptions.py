import logging


class ProxiMLException(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    def __repr__(self):
        return "ProxiMLException( {self.message!r})".format(self=self)

    def __str__(self):
        return "ProxiMLException({self.message!r})".format(self=self)


class ApiError(ProxiMLException):
    def __init__(self, status, data, *args):
        super().__init__(data, *args)
        self._status = status
        logging.debug(data)
        self._message = data.get("errorMessage") or data.get("message")

    @property
    def status(self) -> int:
        return self._status

    def __repr__(self):
        return "ApiError({self.status}, {self.message!r})".format(self=self)

    def __str__(self):
        return "ApiError({self.status}, {self.message!r})".format(self=self)


class JobError(ProxiMLException):
    def __init__(self, status, data, *args):
        super().__init__(data, *args)
        self._status = status
        self._message = data

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self):
        return "JobError({self.status}, {self.message})".format(self=self)

    def __str__(self):
        return "JobError({self.status}, {self.message})".format(self=self)


class DatasetError(ProxiMLException):
    def __init__(self, status, data, *args):
        super().__init__(data, *args)
        self._status = status
        self._message = data

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self):
        return "DatasetError({self.status}, {self.message})".format(self=self)

    def __str__(self):
        return "DatasetError({self.status}, {self.message})".format(self=self)


class ModelError(ProxiMLException):
    def __init__(self, status, data, *args):
        super().__init__(data, *args)
        self._status = status
        self._message = data

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self):
        return "ModelError({self.status}, {self.message})".format(self=self)

    def __str__(self):
        return "ModelError({self.status}, {self.message})".format(self=self)


class CheckpointError(ProxiMLException):
    def __init__(self, status, data, *args):
        super().__init__(data, *args)
        self._status = status
        self._message = data

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self):
        return "CheckpointError({self.status}, {self.message})".format(self=self)

    def __str__(self):
        return "CheckpointError({self.status}, {self.message})".format(self=self)


class VolumeError(ProxiMLException):
    def __init__(self, status, data, *args):
        super().__init__(data, *args)
        self._status = status
        self._message = data

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self):
        return "VolumeError({self.status}, {self.message})".format(self=self)

    def __str__(self):
        return "VolumeError({self.status}, {self.message})".format(self=self)


class ConnectionError(ProxiMLException):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self._message = message

    def __repr__(self):
        return "ConnectionError({self.message})".format(self=self)

    def __str__(self):
        return "ConnectionError({self.message})".format(self=self)


class SpecificationError(ProxiMLException):
    def __init__(self, attribute, message, *args):
        super().__init__(message, *args)
        self._attribute = attribute
        self._message = message

    @property
    def attribute(self) -> str:
        return self._attribute

    def __repr__(self):
        return "SpecificationError({self.attribute}, {self.message})".format(self=self)

    def __str__(self):
        return "SpecificationError({self.attribute}, {self.message})".format(self=self)
