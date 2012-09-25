#!/usr/bin/env python

def init_app( app):
    from models import init_model
    init_model( app)
