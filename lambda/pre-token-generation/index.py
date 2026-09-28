def handler(event: dict, _context: object) -> dict:
    attributes = event.get('request', {}).get('userAttributes', {})
    clinic_id = attributes.get('custom:clinic_id') or attributes.get('clinic_id')

    if not clinic_id:
        raise ValueError('clinic_id is required for ClinicFlow identity')

    event.setdefault('response', {})
    event['response']['claimsAndScopeOverrideDetails'] = {
        'accessTokenGeneration': {
            'claimsToAddOrOverride': {
                'clinic_id': str(clinic_id),
            }
        }
    }
    return event