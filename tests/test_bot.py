from time import sleep
from tools import TesterClinet
from time import sleep
import pytest
from pathlib import Path

@pytest.fixture
def base_path():
    return Path(__file__).parent

@pytest.mark.asyncio
async def test_bot(base_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(base_path)
    async with TesterClinet.init() as app:
        msg = await app.send_message("@richard_test_bot", '/hello')
        usr = msg.from_user.first_name
        sleep(1)
        msg = await app.get_messages("@richard_test_bot", msg.id + 1)
        assert msg.text == f'Hello {usr}'