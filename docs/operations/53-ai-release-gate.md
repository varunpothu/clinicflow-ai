# AI Release Gate

The repository has a deterministic synthetic regression suite before cloud model evaluation is introduced.

## Gate

A change must maintain:
- >= 80% intent accuracy on the synthetic fixture
- >= 80% clarification accuracy
- structured output/schema tests
- prompt-injection negative tests

This is a portfolio engineering gate, not a clinical safety certification.

## Production extension

For a Bedrock model change, run the same cases against the candidate model, store the model/prompt version with results, compare against the baseline and fail promotion on agreed regression thresholds.
