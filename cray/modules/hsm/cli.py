"""hsm"""
# pylint: disable=invalid-name
import os
from cray.generator import generate

SWAGGER_OPTS = {
    'vocabulary': {
        'put': 'replace',
        'deleteall': 'clear'
    }
}

HSM_API_VERSION = os.environ.get("CRAY_HSM_API_VERSION", "v2")

if HSM_API_VERSION == 'v1':
    cli = generate(__file__, filename='swagger3_v1.json', swagger_opts=SWAGGER_OPTS)
else:
    cli = generate(__file__, filename='swagger3_v2.json', swagger_opts=SWAGGER_OPTS)
