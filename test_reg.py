from main import Test
import pytest


@pytest.mark.asyncio
async def test_reg():
	result1 = await Test.registr_test("king","hdahsjdhas")
	result2 = await Test.registr_test("pops","1234567890s")
	assert result1 == False
	assert result2 == True


@pytest.mark.asyncio
async def test_sign():
	result1 = await Test.login_test("test","123456789")
	assert result1 == False

