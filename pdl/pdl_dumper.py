import json
from typing import Any, Sequence

import yaml

from . import pdl_ast
from .pdl_ast import (
    ApiBlock,
    ArrayBlock,
    BamModelBlock,
    BamTextGenerationParameters,
    Block,
    BlocksType,
    CallBlock,
    CodeBlock,
    ContributeTarget,
    DataBlock,
    DocumentBlock,
    ErrorBlock,
    ForBlock,
    FunctionBlock,
    GetBlock,
    IfBlock,
    IncludeBlock,
    LitellmModelBlock,
    LitellmParameters,
    LocationType,
    MessageBlock,
    ObjectBlock,
    ParserType,
    PdlParser,
    ReadBlock,
    RegexParser,
    RepeatBlock,
    RepeatUntilBlock,
    SequenceBlock,
)

yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str  # type: ignore


def repr_str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.org_represent_str(data)


yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)


def dump_yaml(data, **kwargs):
    return yaml.safe_dump(
        data,
        default_flow_style=False,
        allow_unicode=True,
        width=1000000000,
        sort_keys=False,
        **kwargs,
    )


def dumps_json(data, **kwargs):
    return json.dumps(data, **kwargs)


def program_to_dict(prog: pdl_ast.Program) -> int | float | str | dict[str, Any]:
    return block_to_dict(prog.root)


def block_to_dict(block: pdl_ast.BlockType) -> int | float | str | dict[str, Any]:
    if not isinstance(block, Block):
        return block
    d: dict[str, Any] = {}
    d["kind"] = block.kind
    if block.description is not None:
        d["description"] = block.description
    if block.spec is not None:
        d["spec"] = block.spec
    if block.defs is not None:
        d["defs"] = {x: blocks_to_dict(b) for x, b in block.defs.items()}
    match block:
        case BamModelBlock():
            d["platform"] = block.platform
            d["model"] = block.model
            if block.input is not None:
                d["input"] = blocks_to_dict(block.input)
            if block.prompt_id is not None:
                d["prompt_id"] = block.prompt_id
            if block.parameters is not None:
                if isinstance(block.parameters, BamTextGenerationParameters):
                    d["parameters"] = block.parameters.model_dump()
                else:
                    d["parameters"] = block.parameters
            if block.moderations is not None:
                d["moderations"] = block.moderations
            if block.data is True:
                d["data"] = block.data
            if block.constraints is not None:
                d["constraints"] = block.constraints
        case LitellmModelBlock():
            d["platform"] = block.platform
            d["model"] = block.model
            if block.input is not None:
                d["input"] = blocks_to_dict(block.input)
            if block.parameters is not None:
                if isinstance(block.parameters, LitellmParameters):
                    d["parameters"] = block.parameters.model_dump(
                        exclude_unset=True, exclude_defaults=True
                    )
                else:
                    d["parameters"] = block.parameters
        case CodeBlock():
            d["lan"] = block.lan
            d["code"] = blocks_to_dict(block.code)
        case GetBlock():
            d["get"] = block.get
        case DataBlock():
            d["data"] = block.data
            if block.raw:
                d["raw"] = block.raw
        case ApiBlock():
            d["api"] = block.api
            d["url"] = block.url
            if block.input is not None:
                d["input"] = blocks_to_dict(block.input)
        case DocumentBlock():
            d["document"] = blocks_to_dict(block.document)
        case SequenceBlock():
            d["sequence"] = blocks_to_dict(block.sequence)
        case ArrayBlock():
            d["array"] = blocks_to_dict(block.array)
        case ObjectBlock():
            if isinstance(block.object, dict):
                d["object"] = {k: blocks_to_dict(b) for k, b in block.object.items()}
            else:
                d["object"] = [blocks_to_dict(b) for b in block.object]
        case MessageBlock():
            d["content"] = blocks_to_dict(block.content)
        case ReadBlock():
            d["read"] = block.read
            d["message"] = block.message
            d["multiline"] = block.multiline
        case IncludeBlock():
            d["include"] = block.include
        case IfBlock():
            d["if"] = block.condition
            d["then"] = blocks_to_dict(block.then)
            if block.elses is not None:
                d["else"] = blocks_to_dict(block.elses)
            if block.if_result is not None:
                d["if_result"] = block.if_result
        case RepeatBlock():
            d["repeat"] = blocks_to_dict(block.repeat)
            d["num_iterations"] = block.num_iterations
            d["as"] = block.iteration_type
            if block.trace is not None:
                d["trace"] = [blocks_to_dict(blocks) for blocks in block.trace]
        case RepeatUntilBlock():
            d["repeat"] = blocks_to_dict(block.repeat)
            d["until"] = block.until
            d["as"] = block.iteration_type
            if block.trace is not None:
                d["trace"] = [blocks_to_dict(blocks) for blocks in block.trace]
        case ForBlock():
            d["for"] = block.fors
            d["repeat"] = blocks_to_dict(block.repeat)
            d["as"] = block.iteration_type
            if block.trace is not None:
                d["trace"] = [blocks_to_dict(blocks) for blocks in block.trace]
        case FunctionBlock():
            d["function"] = block.function
            d["return"] = blocks_to_dict(block.returns)
            # if block.scope is not None:
            #     d["scope"] = scope_to_dict(block.scope)
        case CallBlock():
            d["call"] = block.call
            d["args"] = block.args
            if block.trace is not None:
                d["trace"] = blocks_to_dict(block.trace)  # pyright: ignore
        case ErrorBlock():
            d["program"] = blocks_to_dict(block.program)
            d["msg"] = block.msg
    if block.assign is not None:
        d["def"] = block.assign
    if set(block.contribute) != {ContributeTarget.RESULT, ContributeTarget.CONTEXT}:
        d["contribute"] = block.contribute
    if block.result is not None:
        if isinstance(block.result, FunctionBlock):
            d["result"] = ""
        else:
            d["result"] = block.result
    if block.parser is not None:
        d["parser"] = parser_to_dict(block.parser)
    if block.location is not None:
        d["location"] = location_to_dict(block.location)
    if block.has_error:
        d["has_error"] = block.has_error
    if block.fallback is not None:
        d["fallback"] = blocks_to_dict(block.fallback)
    return d


def blocks_to_dict(
    blocks: BlocksType,
) -> int | float | str | dict[str, Any] | list[int | float | str | dict[str, Any]]:
    result: int | float | str | dict[str, Any] | list[
        int | float | str | dict[str, Any]
    ]
    if not isinstance(blocks, str) and isinstance(blocks, Sequence):
        result = [block_to_dict(block) for block in blocks]
    else:
        result = block_to_dict(blocks)
    return result


def parser_to_dict(parser: ParserType) -> str | dict[str, Any]:
    p: str | dict[str, Any]
    match parser:
        case "json" | "yaml":
            p = parser
        case RegexParser():
            p = parser.model_dump()
        case PdlParser():
            p = {}
            p["description"] = parser.description
            p["spec"] = parser.spec
            p["pdl"] = blocks_to_dict(parser.pdl)
        case _:
            assert False
    return p


def location_to_dict(location: LocationType) -> dict[str, Any]:
    return {"path": location.path, "file": location.file, "table": location.table}


# def scope_to_dict(scope: ScopeType) -> dict[str, Any]:
#     d = {}
#     for x, v in scope.items():
#         if isinstance(v, Block):
#             d[x] = block_to_dict(v)  # type: ignore
#         else:
#             d[x] = v
#     return d
