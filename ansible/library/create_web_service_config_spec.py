#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: create_web_service_config_spec
short_description: Create validated web service config spec for aggregation
version_added: '1.0.0'
description:
  Validates web service config spec fields and returns a dict ready for list aggregation.
options:
  subdomain:
    description: subdomain for web service
    type: str
    required: true
  port:
    description: Port number.
    type: int
    required: true
  auth:
    description: Environment label (optional).
    type: bool
    required: false
  mtls:
    description: mTLS mode - must be one of allowed values.
    type: str
    required: true
    choices: ['none', 'required', 'optional']
  mtls_cert:
    description: mTLS certificate - required if mtls is 'required' or 'optional'
    type: str
    required: false
author:
  - parasite-lost
'''

EXAMPLES = '''
- name: Create validated service config spec
  create_web_service_config_spec:
    subdomain: 'api-gateway'
    port: 8443
    auth: false
    mtls: 'required'
    mtls_cert: 'my-CA.pem'
  register: result

- ansible.builtin.debug:
    var: result.spec
'''

RETURN = '''
spec:
  description: Validated dict ready to append to web services config list.
  type: dict
  returned: always
  sample:
    subdomain: 'api-gateway'
    port: 8443
    auth: false
    mtls: 'required'
    mtls_cert: 'test-CA.pem'
changed:
  description: Always false.
  type: bool
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            subdomain=dict(type='str', required=True),
            port=dict(type='int', required=True),
            auth=dict(type='bool', required=False, default=True),
            mtls=dict(type='str', required=False,
                      choices=['none', 'required', 'optional'], default='none'),
            mtls_cert=dict(type='str', required=False, default=None)
        ),
        required_if=[
            ['mtls', 'required', ['mtls_cert']],
            ['mtls', 'optional', ['mtls_cert']],
        ],
        supports_check_mode=True
    )

    spec = {
        'subdomain': module.params['subdomain'],
        'port': module.params['port'],
    }

    if module.params['auth'] is not None:
        spec['auth'] = module.params['auth']

    if module.params['mtls'] is not None:
        spec['mtls'] = module.params['mtls']

    if module.params['mtls_cert'] is not None:
        spec['mtls_cert'] = module.params['mtls_cert']

    module.exit_json(changed=False, spec=spec)


if __name__ == '__main__':
    main()
