"""
    This module imports GraphQL types from graphql-core, but also defines some
    additional custom types.
"""

import datetime
import json
from typing import Any

import graphql.type
# Had to disable pylint below, because "No name '...' in module '...'"
from graphql.language.ast import ValueNode, StringValueNode # pylint: disable=E0611
from graphql.language.printer import print_ast


__all__ = (
    'Boolean', 'Int', 'String', 'Float',
    'Decimal',
    'DateTime', 'Date', 'Time',
    'Union', 'List', 'NonNull',
    'JSONString'
)

# non-GraphQL wrapper type, to replace NonNull in wrappings
# pylint: disable=R0903 # Too few public methods

class Mandatory:
    """
        Non-GraphQL wrapper type, to replace NonNull in mappings or when using
        "natural" Python types
    """
    def __init__(self, type_):
        self.type_ = type_

# native scalar types

Boolean = graphql.type.GraphQLBoolean
Int = graphql.type.GraphQLInt
Float = graphql.type.GraphQLFloat
Decimal = Float
String = graphql.type.GraphQLString

# native scalar wrappers

Union = graphql.type.GraphQLUnionType
List = graphql.type.GraphQLList
NonNull = graphql.type.GraphQLNonNull

# datetime type

def serialize_datetime(output_value: datetime.datetime) -> str:
    """ Serializes an internal value to include in a response. """
    return output_value.isoformat()

def parse_datetime_value(input_value: Any) -> datetime.datetime:
    """ Parses an externally provided value to use as an input. """
    try:
        return datetime.datetime.fromisoformat(input_value)
    except Exception as error:
        raise ValueError(
            f'Cannot parse DateTime from: {repr(input_value)}, got: {error}') from error

def parse_datetime_literal(value_node: ValueNode, _variables: Any = None) -> datetime.datetime:
    """ Parses an externally provided AST value to use as an input. """
    if not isinstance(value_node, StringValueNode):
        raise ValueError(
            "DateTime should be represented as a string in input: " + print_ast(value_node),
            value_node,
        )
    return parse_datetime_value(value_node.value)

DateTime = graphql.type.GraphQLScalarType(
    name = 'DateTime',
    description = 'A datetime element, serialized in standard "YYYY-MM-DDThh:ii::ss.mmmmmm" format',
    serialize = serialize_datetime,
    parse_value = parse_datetime_value,
    parse_literal = parse_datetime_literal,
)

# date type

def serialize_date(output_value: datetime.date) -> str:
    """ Serializes an internal value to include in a response. """
    return output_value.isoformat()

def parse_date_value(input_value: Any) -> datetime.date:
    """ Parses an externally provided value to use as an input. """
    try:
        return datetime.date.fromisoformat(input_value)
    except Exception as error:
        raise ValueError(f'Cannot parse Date from: {repr(input_value)}, got: {error}') from error

def parse_date_literal(value_node: ValueNode, _variables: Any = None) -> datetime.date:
    """ Parses an externally provided AST value to use as an input. """
    if not isinstance(value_node, StringValueNode):
        raise ValueError(
            "Date should be represented as a string in input: " + print_ast(value_node),
            value_node,
        )
    return parse_date_value(value_node.value)

Date = graphql.type.GraphQLScalarType(
    name = 'Date',
    description = 'A date element, serialized in standard "YYYY-MM-DD" format',
    serialize = serialize_date,
    parse_value = parse_date_value,
    parse_literal = parse_date_literal,
)

# time type

def serialize_time(output_value: datetime.time) -> str:
    """ Serializes an internal value to include in a response. """
    return output_value.isoformat()

def parse_time_value(input_value: Any) -> datetime.time:
    """ Parses an externally provided value to use as an input. """
    try:
        return datetime.time.fromisoformat(input_value)
    except Exception as error:
        raise ValueError(f'Cannot parse Time from: {repr(input_value)}, got: {error}') from error

def parse_time_literal(value_node: ValueNode, _variables: Any = None) -> datetime.time:
    """ Parses an externally provided AST value to use as an input. """
    if not isinstance(value_node, StringValueNode):
        raise ValueError(
            "Time should be represented as a string in input: " + print_ast(value_node),
            value_node,
        )
    return parse_time_value(value_node.value)

Time = graphql.type.GraphQLScalarType(
    name = 'Time',
    description = 'A time element, serialized in standard "hh:ii::ss.mmmmmm" format',
    serialize = serialize_time,
    parse_value = parse_time_value,
    parse_literal = parse_time_literal,
)

# JSON type

def serialize_jsonstring(output_value: datetime.time) -> str:
    """ Serializes an internal value to include in a response. """
    return json.dumps(output_value)

def parse_jsonstring_value(input_value: Any) -> datetime.time:
    """ Parses an externally provided value to use as an input. """
    try:
        return json.loads(input_value)
    except Exception as error:
        raise ValueError(
            f'Cannot parse JSONString from: {repr(input_value)}, got: {error}') from error

def parse_jsonstring_literal(value_node: ValueNode, _variables: Any = None) -> datetime.time:
    """ Parses an externally provided AST value to use as an input. """
    if not isinstance(value_node, StringValueNode):
        raise ValueError(
            "JSONString should be represented as a string in input: " + print_ast(value_node),
            value_node,
        )
    return parse_jsonstring_value(value_node.value)

JSONString = graphql.type.GraphQLScalarType(
    name = 'JSON',
    description = 'JSON in a string',
    serialize = serialize_jsonstring,
    parse_value = parse_jsonstring_value,
    parse_literal = parse_jsonstring_literal,
)
