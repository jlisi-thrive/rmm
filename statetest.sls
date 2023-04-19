{% set defaultGateway = salt['ip.get_default_gateway']() %}

default_gateway:
  grains.present:
    - value: {{defaultGateway}}
    - fire_event: thrive/grainupdate