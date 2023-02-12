import os
import sys
import logging

from stem.control import Controller


class HiddenService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger('hidden-service')
        self._service = None
        self._controller: Controller = None

    def start(self, service_name, control_ip, control_port, port_routing, password='', key_file=None):
        self._logger.info('Connecting to TOR')
        controller = Controller.from_port(control_ip, control_port)
        self._logger.info('Authenticating')
        controller.authenticate(password=password)
        self._logger.info('Deploying hidden service')
        dir_path = os.path.join(sys.path[0], 'keys')
        if not key_file:
            key_file = os.path.join(dir_path, service_name + '_key')
        if not os.path.exists(key_file):
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            service = controller.create_ephemeral_hidden_service(port_routing, await_publication=True)
            self._logger.info('Started a new hidden service')
            with open(key_file, 'w', encoding='utf-8') as file:
                file.write(f'{service.private_key_type}:{service.private_key}')
        else:
            with open(key_file, 'r', encoding='utf-8') as file:
                key_type, key_content = file.read().split(':', 1)
            service = controller.create_ephemeral_hidden_service(port_routing, key_type=key_type, key_content=key_content, await_publication=True)
            self._logger.info('Resumed existed hidden service')
        self._service = service
        self._controller = controller

    def stop(self):
        if self._controller is None:
            self._logger.warning('Peer controller is not started')
            return
        self._controller.remove_ephemeral_hidden_service(self._service.service_id)
        self._controller = None
        self._service = None
        self._logger.info('Stopped hidden service')

    def get_id(self):
        if self._service:
            return self._service.service_id
        return None

    def get_address(self):
        if self._service:
            return self.get_id() + '.onion'
        return None
