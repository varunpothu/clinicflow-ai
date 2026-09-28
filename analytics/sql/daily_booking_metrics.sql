WITH bookings AS (
    SELECT
        date(from_iso8601_timestamp(occurred_at)) AS booking_date,
        event_type,
        count(*) AS event_count
    FROM appointment_events
    WHERE event_type IN (
        'APPOINTMENT_CONFIRMED',
        'APPOINTMENT_CANCELLED',
        'APPOINTMENT_RESCHEDULED',
        'BOOKING_CONFLICT'
    )
    GROUP BY 1, 2
)
SELECT
    booking_date,
    sum(CASE WHEN event_type = 'APPOINTMENT_CONFIRMED' THEN event_count ELSE 0 END) AS confirmed,
    sum(CASE WHEN event_type = 'APPOINTMENT_CANCELLED' THEN event_count ELSE 0 END) AS cancelled,
    sum(CASE WHEN event_type = 'APPOINTMENT_RESCHEDULED' THEN event_count ELSE 0 END) AS rescheduled,
    sum(CASE WHEN event_type = 'BOOKING_CONFLICT' THEN event_count ELSE 0 END) AS conflicts
FROM bookings
GROUP BY booking_date
ORDER BY booking_date;
