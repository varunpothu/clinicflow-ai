# Production Operations Baseline

## Autoscaling

The API service uses ECS target tracking on average service CPU, with a one-task floor and four-task ceiling for the portfolio environment.

## Alarms

- ECS CPU sustained above 80 percent
- ALB unhealthy target count above zero
- booking dead-letter queue has visible messages

The alarms intentionally have no hard-coded notification destination. A real customer environment should connect them to its incident-management or on-call channel.

## Operational response

1. Check the alarm and correlation IDs.
2. Inspect ECS task health and CloudWatch logs.
3. Check SQS backlog and DLQ.
4. Review recent deployment and workflow exceptions.
5. Roll back the ECS task definition when the deployment is the likely cause.