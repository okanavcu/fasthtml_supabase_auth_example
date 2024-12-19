from dataclasses import dataclass
import json
from typing import Optional, List
from datetime import datetime

# Kullanıcı bilgilerini temsil eden sınıf
@dataclass
class User:
    id: str
    app_metadata: dict
    user_metadata: dict
    aud: str
    confirmation_sent_at: Optional[datetime]
    recovery_sent_at: Optional[datetime]
    email_change_sent_at: Optional[datetime]
    new_email: Optional[str]
    new_phone: Optional[str]
    invited_at: Optional[datetime]
    action_link: Optional[str]
    email: str
    phone: Optional[str]
    created_at: datetime
    confirmed_at: datetime
    email_confirmed_at: datetime
    phone_confirmed_at: Optional[datetime]
    last_sign_in_at: datetime
    role: str
    updated_at: datetime
    identities: List['UserIdentity']  # UserIdentity sınıfı aşağıda tanımlanacak
    is_anonymous: bool
    factors: Optional[dict]

# Kullanıcı kimlik bilgilerini temsil eden sınıf
@dataclass
class UserIdentity:
    id: str
    identity_id: str
    user_id: str
    identity_data: dict
    provider: str
    created_at: datetime
    last_sign_in_at: datetime
    updated_at: datetime

# Oturum bilgilerini temsil eden sınıf
@dataclass
class Session:
    provider_token: Optional[str]
    provider_refresh_token: Optional[str]
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: int
    token_type: str
    user: User

# AuthResponse sınıfı
@dataclass
class AuthResponse:
    user: Optional[User] = None
    session: Optional[Session] = None



# data.json dosyasını oku
with open('data.json', 'r') as f:
    data = json.load(f)


# Dataclass'ları oluşturma
user = User(
    id=data['user']['id'],
    app_metadata=data['user']['app_metadata'],
    user_metadata=data['user']['user_metadata'],
    aud=data['user']['aud'],
    confirmation_sent_at=datetime.fromisoformat(data['user']['confirmation_sent_at']) if data['user']['confirmation_sent_at'] else None,
    recovery_sent_at=datetime.fromisoformat(data['user']['recovery_sent_at']) if data['user']['recovery_sent_at'] else None,
    email_change_sent_at=datetime.fromisoformat(data['user']['email_change_sent_at']) if data['user']['email_change_sent_at'] else None,
    new_email=data['user']['new_email'],
    new_phone=data['user']['new_phone'],
    invited_at=datetime.fromisoformat(data['user']['invited_at']) if data['user']['invited_at'] else None,
    action_link=data['user']['action_link'],
    email=data['user']['email'],
    phone=data['user']['phone'],
    created_at=datetime.fromisoformat(data['user']['created_at']),
    confirmed_at=datetime.fromisoformat(data['user']['confirmed_at']),
    email_confirmed_at=datetime.fromisoformat(data['user']['email_confirmed_at']),
    phone_confirmed_at=datetime.fromisoformat(data['user']['phone_confirmed_at']) if data['user']['phone_confirmed_at'] else None,
    last_sign_in_at=datetime.fromisoformat(data['user']['last_sign_in_at']),
    role=data['user']['role'],
    updated_at=datetime.fromisoformat(data['user']['updated_at']),
    identities=[UserIdentity(
        id=identity['id'],
        identity_id=identity['identity_id'],
        user_id=identity['user_id'],
        identity_data=identity['identity_data'],
        provider=identity['provider'],
        created_at=datetime.fromisoformat(identity['created_at']),
        last_sign_in_at=datetime.fromisoformat(identity['last_sign_in_at']),
        updated_at=datetime.fromisoformat(identity['updated_at'])
    ) for identity in data['user']['identities']],
    is_anonymous=data['user']['is_anonymous'],
    factors=data['user']['factors']
)

session = Session(
    provider_token=data['session']['provider_token'],
    provider_refresh_token=data['session']['provider_refresh_token'],
    access_token=data['session']['access_token'],
    refresh_token=data['session']['refresh_token'],
    expires_in=data['session']['expires_in'],
    expires_at=data['session']['expires_at'],
    token_type=data['session']['token_type'],
    user=user
)

auth_response = AuthResponse(user=user, session=session)

# auth_response nesnesi kullanıma hazır
print(auth_response)
