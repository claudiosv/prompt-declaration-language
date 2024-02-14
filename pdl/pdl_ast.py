from typing import Any, Optional, TypeAlias

from pydantic import BaseModel, ConfigDict, RootModel

ScopeType: TypeAlias = dict[str, Any]


class ConditionExpr(BaseModel):
    result: Optional[bool] = None


class EndsWithArgs(BaseModel):
    arg0: "PromptType"
    arg1: str


class EndsWithCondition(ConditionExpr):
    ends_with: EndsWithArgs


class ContainsArgs(BaseModel):
    arg0: "PromptType"
    arg1: str


class ContainsCondition(ConditionExpr):
    contains: ContainsArgs


ConditionType: TypeAlias = str | EndsWithCondition | ContainsCondition


class Block(BaseModel):
    """PDL program block"""

    description: Optional[str] = None
    assign: Optional[str] = None
    show_result: bool = True
    result: Optional[Any] = None


class FunctionBlock(Block):
    model_config = ConfigDict(extra="allow")
    show_result: bool = False
    function: str
    params: dict[str, Any] = {}
    scope: Optional[ScopeType] = None

    _body: Optional["BlockType"] = None

    @property
    def body(self) -> Optional["BlockType"]:
        if self._body is None and self.model_extra is not None:
            self._body = Program.model_validate(
                {"description": f"function {self.function} body"} | self.model_extra
            ).root
        return self._body


class CallBlock(Block):
    call: str
    args: dict[str, Any] = {}


class ModelBlock(Block):
    model: str
    input: Optional["PromptType"] = None
    decoding: Optional[str] = None
    stop_sequences: Optional[list[str]] = None
    include_stop_sequences: bool = False
    params: Optional[Any] = None


class CodeBlock(Block):
    lan: str
    code: "PromptsType"


class ApiBlock(Block):
    api: str
    url: str
    input: "PromptType"


class GetBlock(Block):
    get: str


class ValueBlock(Block):
    value: Any


class SequenceBlock(Block):
    prompts: "PromptsType"


class IfBlock(Block):
    prompts: "PromptsType"
    condition: ConditionType


class RepeatsBlock(Block):
    prompts: "PromptsType"
    repeats: int
    trace: list["PromptsType"] = []


class RepeatsUntilBlock(Block):
    prompts: "PromptsType"
    repeats_until: ConditionType
    trace: list["PromptsType"] = []


class ErrorBlock(Block):
    msg: str
    block: "BlockType"


class InputBlock(Block):
    filename: Optional[str] = None
    stdin: bool = False
    message: Optional[str] = None
    multiline: bool = False
    json_content: bool = False


BlockType: TypeAlias = (
    FunctionBlock
    | CallBlock
    | ModelBlock
    | CodeBlock
    | ApiBlock
    | GetBlock
    | ValueBlock
    | IfBlock
    | RepeatsBlock
    | RepeatsUntilBlock
    | SequenceBlock
    | ErrorBlock
    | InputBlock
    | Block
)
PromptType: TypeAlias = str | BlockType  # pyright: ignore
PromptsType: TypeAlias = list[PromptType]


class Program(RootModel):
    """
    Prompt Description Program (PDL)
    """

    # root: dict[str, BlockType]
    root: BlockType
