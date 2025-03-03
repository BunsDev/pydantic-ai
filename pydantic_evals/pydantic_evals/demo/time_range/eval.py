from pydantic_evals.demo.time_range import TimeRangeAgentResponse, infer_time_range
from pydantic_evals.demo.time_range.models import TimeRangeDataset, TimeRangeInputs
from pydantic_evals.evals import Evaluation, ScoringContext
from pydantic_evals.llm_as_a_judge import GradingOutput, judge_input_output


async def judge_time_range_case(inputs: TimeRangeInputs, output: TimeRangeAgentResponse) -> GradingOutput:
    """Judge the output of a time range inference agent based on a rubric."""
    rubric = 'The output should be a reasonable time range to select for the given inputs.'
    return await judge_input_output(inputs, output, rubric)


async def main():
    """TODO: Move the pydantic_evals.demo package before merging."""
    import logfire

    logfire.configure(send_to_logfire='if-token-present', console=logfire.ConsoleOptions(verbose=True))

    dataset = TimeRangeDataset.from_yaml()

    async def handler(ctx: ScoringContext[TimeRangeInputs, TimeRangeAgentResponse]):
        result = await judge_time_range_case(inputs=ctx.inputs, output=ctx.output)
        ctx.record_label('reasonable', 'yes' if result else 'no')

    evaluation = Evaluation(infer_time_range, scoring=handler, cases=dataset.rows)

    report = await evaluation.run(max_concurrency=10)

    report.print(include_input=True, include_output=True)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
