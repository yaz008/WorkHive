from dataclasses import dataclass, field

from project.libs.cached import CachedFileReader


@dataclass(slots=True)
class MultilingualFileReader:
    texts: str
    __reader: CachedFileReader = field(default_factory=CachedFileReader)

    def read(self, language: str, state: str) -> str:
        return self.__reader.read(
            path=f'{self.texts}\\{language}\\{state}.txt', mode='r'
        )
