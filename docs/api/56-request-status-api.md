# Appointment Request Status API

GET /api/v1/appointment-requests/{request_id}

Returns the durable request state. Patients can only read their own request; staff identities can use the endpoint within the clinic context.

The durable record allows the UI to poll or subscribe to workflow progress without keeping an HTTP request open.