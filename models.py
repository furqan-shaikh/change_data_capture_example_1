import json
from dataclasses import dataclass
from typing import List, Any, Dict


class PhotoJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Photo):
            return obj.to_dict()
        return super().default(obj)


@dataclass
class Photo:
    id: str
    width: int
    height: int
    description: str
    city: str
    country: str
    latitude: float
    longitude: float
    exif_make: str
    exif_model: str
    exif_exposure_time: str
    urls: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "width": self.width,
            "height": self.height,
            "description": self.description,
            "city": self.city,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "exif_make": self.exif_make,
            "exif_model": self.exif_model,
            "exif_exposure_time": self.exif_exposure_time,
            "urls": self.urls
        }
