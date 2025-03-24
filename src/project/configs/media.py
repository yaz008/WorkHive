from project.core.config import config


@config(filename='media')
class MediaConfig:
    AnimationFolder: str = 'assets\\media\\animations'
    DocumentFolder: str = 'assets\\media\\documents'
    AudioFolder: str = 'assets\\media\\audios'
    PhotoFolder: str = 'assets\\media\\photos'
    VideoFolder: str = 'assets\\media\\videos'


@config(filename='document-names')
class WorkHiveDocument:
    PrivacyPolicy: str = 'privacy-policy'
    AdvertisingConsent: str = 'advertising-consent'
    Offer: str = 'offer'
