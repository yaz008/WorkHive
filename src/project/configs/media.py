from project.core.config import config


@config(filename='media')
class MediaConfig:
    AnimationFolder: str = 'assets\\media\\docs'
    DocumentFolder: str = 'assets\\media\\docs'
    AudioFolder: str = 'assets\\media\\docs'
    PhotoFolder: str = 'assets\\media\\docs'
    VideoFolder: str = 'assets\\media\\docs'


@config(filename='document-names')
class WorkHiveDocument:
    PrivacyPolicy: str = 'privacy-policy'
    AdAgreement: str = 'ad-agreement'
    OfferAgreement: str = 'affer-agreement'
