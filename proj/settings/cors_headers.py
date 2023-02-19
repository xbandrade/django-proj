from utils.environment import get_env_variable, parse_comma_sep_str_to_list

CORS_ALLOWED_ORIGINS = parse_comma_sep_str_to_list(
    get_env_variable('ALLOWED_HOSTS')
)
