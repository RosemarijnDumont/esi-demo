from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_trial = Column(Boolean, default=True) # Indicates if the account is a trial account
    plan_type = Column(String, default="trial") # e.g., "trial", "free", "basic", "enterprise"

    saml_config = relationship("SamlConfig", uselist=False, back_populates="account")
    users = relationship("User", back_populates="account")

    def __repr__(self):
        return f"<Account(id='{self.id}', name='{self.name}', is_trial={self.is_trial})>"

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey('accounts.id'), nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True) # Nullable if only SSO is used
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user") # e.g., "admin", "user", "trial_user"

    account = relationship("Account", back_populates="users")

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', account_id='{self.account_id}')>"

class SamlConfig(Base):
    __tablename__ = 'saml_configs'

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey('accounts.id'), unique=True, nullable=False, index=True)
    idp_metadata_xml = Column(Text, nullable=False) # Stores the IdP's metadata XML
    enabled = Column(Boolean, default=False)
    # Add other SAML-related configurations as needed, e.g., certificate paths, entity IDs

    account = relationship("Account", back_populates="saml_config")

    def __repr__(self):
        return f"<SamlConfig(id='{self.id}', account_id='{self.account_id}', enabled={self.enabled})>"