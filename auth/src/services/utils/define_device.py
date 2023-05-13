def define_device(user_agent: str) -> str:
    """Define device type by user agent."""

    if 'TV' in user_agent:
        return 'smart'
    if 'Mobile' in user_agent:
        return 'mobile'

    return 'web'
