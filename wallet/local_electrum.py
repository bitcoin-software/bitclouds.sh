from electrum.daemon import Daemon
from electrum.simple_config import SimpleConfig
from electrum.commands import Commands
from electrum.util import create_and_start_event_loop
loop, stop_loop, loop_thread = create_and_start_event_loop()
config = SimpleConfig()
daemon = Daemon(config, listen_jsonrpc=False)
network = daemon.network
commands = Commands(config=config, network=network, daemon=daemon)


async def main():
    print(await commands.help())
loop.create_task(main())