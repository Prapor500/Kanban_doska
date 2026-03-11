from jam import Jam
from settings import settings

jam = Jam(auth_type="jwt", config=settings.JAM_SETTINGS)
