# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    URLField
)

from apps.db import db

class Address(EmbeddedDocument):
    """
    Address Fields
    """

    meta = {
        "ordering": ["zip-code"]
    }

    zip_code = StringField(default="")
    street = StringField(default="")
    number = StringField(default="")
    complement = StringField(default="")
    neighborhood = StringField(default="")
    city = StringField(default="")
    state = StringField(default="")
    country = StringField(default="Brasil")


class User(db.Document):
    meta = {"collections": "users",
            "ordering": ["email"]}

    # nome, data_nasc, telefone, e-mail, endereço, nome de user, senha
    full_name = StringField(required=True)
    user_name = StringField(required=True, unique=True)
    date_of_born = DateTimeField()
    email = EmailField(required=True, unique=True)
    address = EmbeddedDocumentField(Address, default=Address)
    password = StringField(required=True)
    active = BooleanField(default=False)
    admin = BooleanField(default=False)
    created_at = DateTimeField(default = datetime.now)

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin




