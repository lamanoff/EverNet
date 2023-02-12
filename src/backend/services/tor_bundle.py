from stem.process import launch_tor_with_config
import logging


class TorBundle:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger('tor-bundle')
        self._service = None

    def start(self, tor_path_or_command, control_port, proxy_port):
        if self._service is not None:
            self._logger.warning('Tor process is already started')
            return
        conf = {
            'ControlPort': str(control_port),
            'SocksPort': str(proxy_port)
        }
        self._logger.info(f'Creating TOR process on port {control_port}...')
        self._service = launch_tor_with_config(tor_cmd=tor_path_or_command, config=conf, take_ownership=True)
        self._logger.info('TOR process created')

    def stop(self):
        if self._service is None:
            self._logger.warning('TOR process is already closed')
            return
        self._logger.info('Closing TOR process...')
        self._service.kill()
        self._service = None
        self._logger.info('TOR process closed')
