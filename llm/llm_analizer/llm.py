import transformers
from transformers import AutoTokenizer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.pipelines import Pipeline
from typing import ClassVar
import torch
from torch import dtype

from config import settings


class LLMQwen:
    """
    Класс LLM модели Qwen
    """
    model: ClassVar[str] = settings.LLM.MODEL
    t_dtype: ClassVar[dtype] = torch.bfloat16
    tokenizer: ClassVar[PreTrainedTokenizerBase | None] = None
    pipeline: ClassVar[Pipeline | None] = None

    def _get_tokenizer(self,
                       model: str,
                       ) -> PreTrainedTokenizerBase:
        return AutoTokenizer.from_pretrained(model)

    @classmethod
    def load_pipline(cls) -> Pipeline:
        cls.tokenizer = cls._get_tokenizer(cls, cls.model)
        pipeline = transformers.pipeline(
            'text-generation',
            model=cls.model,
            tokenizer=cls.tokenizer,
            torch_dtype=cls.t_dtype,
            trust_remote_code=True,
        )
        cls.pipeline = pipeline
        return pipeline

    @classmethod
    def make_question(cls, question: str) -> list[dict[str, str]]:
        if not cls.pipeline:
            cls.load_pipline()
        sequences = cls.pipeline(
            question,
            max_length=512,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=cls.tokenizer.eos_token_id,
        )
        return sequences


Qwen = LLMQwen()
