from tools import TesterClinet
from time import sleep
import pytest
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def base_path():
    return Path(__file__).parent

@pytest.mark.asyncio
async def test_bot(base_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(base_path)
    channel = os.environ.get('TESTER_BOT_CHANNEL')
    async with TesterClinet.init(base_path) as app:
        msg = await app.send_message(channel, '/hello')
        usr = msg.from_user.first_name
        sleep(1)
        msg = await app.get_messages(channel, msg.id + 1)
        assert msg.text == f'Hello {usr}'