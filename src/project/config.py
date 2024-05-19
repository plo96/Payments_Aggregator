
"""
	Основные настройки проекта. Получение из файла .env.
"""
from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

HOME_DIR = Path(__file__).parent.parent.parent.absolute()


@dataclass
class Settings:
	"""Класс, содержащий основные настройки приложения."""
	bot_token: str
	home_dir: Path

	_mongo_user: str
	_mongo_pwd: str
	_mongo_host: str
	_mongo_port: int

	def __post_init__(self):
		"""
			'Cборка' url для подключения к mongodb после основной инициализации объекта класса.
		"""
		self.db_url_mongodb: str = f"mongodb://{self._mongo_user}:{self._mongo_pwd}@{self._mongo_host}:{self._mongo_port}"
		self.path_to_db_file = f'{self.home_dir}/sample_files/sample_collection.bson'


settings = Settings(
	bot_token=os.getenv("BOT_TOKEN"),
	home_dir=HOME_DIR,
	_mongo_user=os.getenv("MONGO_USER"),
	_mongo_pwd=os.getenv("MONGO_PWD"),
	_mongo_host=os.getenv("MONGO_HOST"),
	_mongo_port=int(os.getenv("MONGO_PORT")),
)
