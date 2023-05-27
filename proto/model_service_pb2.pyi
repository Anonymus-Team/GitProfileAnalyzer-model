from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Grade(_message.Message):
    __slots__ = ["nickname", "salary"]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    SALARY_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    salary: int
    def __init__(self, salary: _Optional[int] = ..., nickname: _Optional[str] = ...) -> None: ...

class Grades(_message.Message):
    __slots__ = ["grade"]
    GRADE_FIELD_NUMBER: _ClassVar[int]
    grade: _containers.RepeatedCompositeFieldContainer[Grade]
    def __init__(self, grade: _Optional[_Iterable[_Union[Grade, _Mapping]]] = ...) -> None: ...

class GradesRequest(_message.Message):
    __slots__ = ["repLink"]
    REPLINK_FIELD_NUMBER: _ClassVar[int]
    repLink: str
    def __init__(self, repLink: _Optional[str] = ...) -> None: ...
