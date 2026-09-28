from app.integrations.messaging import InMemoryMessageBus, MessageEnvelope


def test_message_bus_keeps_domain_provider_independent() -> None:
    bus = InMemoryMessageBus()
    message = MessageEnvelope(
        message_id="msg-1",
        event_type="APPOINTMENT_CONFIRMED",
        payload="{\"appointment_id\":\"a-1\"}",
        correlation_id="corr-1",
    )
    assert bus.publish(message) == "PUBLISHED"
    assert bus.messages == [message]