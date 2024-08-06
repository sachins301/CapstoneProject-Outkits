"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*!
Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Code(google.protobuf.message.Message):
    """st.code"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_TEXT_FIELD_NUMBER: builtins.int
    LANGUAGE_FIELD_NUMBER: builtins.int
    SHOW_LINE_NUMBERS_FIELD_NUMBER: builtins.int
    code_text: builtins.str
    """Content to display."""
    language: builtins.str
    show_line_numbers: builtins.bool
    def __init__(
        self,
        *,
        code_text: builtins.str = ...,
        language: builtins.str = ...,
        show_line_numbers: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["code_text", b"code_text", "language", b"language", "show_line_numbers", b"show_line_numbers"]) -> None: ...

global___Code = Code
