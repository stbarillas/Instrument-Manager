import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()
from blog.models import Instrument


def populate():

    add_instrument(type='GC',
                   address='130.27.111.40',
                   name="GC 130.27.111.40"
                   )
    add_instrument(type='GC',
                   address='130.27.111.41',
                   name="GC 130.27.111.41"
                   )
    add_instrument(type='GC',
                   address='130.27.111.42',
                   name="GC 130.27.111.42"
                   )
    add_instrument(type='GC',
                   address='130.27.111.43',
                   name="GC 130.27.111.43"
                   )
    add_instrument(type='GC',
                   address='130.27.111.44',
                   name="GC 130.27.111.44"
                   )
    add_instrument(type='GC',
                   address='130.27.111.45',
                   name="GC 130.27.111.45"
                   )
    add_instrument(type='GC',
                   address='130.27.111.46',
                   name="GC 130.27.111.46"
                   )
    add_instrument(type='GC',
                   address='130.27.111.48',
                   name="GC 130.27.111.48"
                   )
    add_instrument(type='GC',
                   address='130.27.111.51',
                   name="GC 130.27.111.51"
                   )
    add_instrument(type='GC',
                   address='130.27.111.52',
                   name="GC 130.27.111.52"
                   )
    add_instrument(type='GC',
                   address='130.27.111.53',
                   name="GC 130.27.111.53"
                   )
    add_instrument(type='GCMS',
                   address='130.27.111.49',
                   name="GCMS 130.27.111.49"
                   )
    add_instrument(type='GCMS',
                   address='130.27.111.54',
                   name="GCMS 130.27.111.54"
                   )
    add_instrument(type='LC',
                   address='130.27.111.60',
                   name="LC 130.27.111.60"
                   )
    add_instrument(type= 'LC',
                   address= '130.27.111.61',
                   name= "LC 130.27.111.61"
                   )
    add_instrument(type='LC',
                   address='130.27.111.62',
                   name="LC 130.27.111.62"
                   )
    add_instrument(type='LC',
                   address='130.27.111.63',
                   name="LC 130.27.111.63"
                   )
    add_instrument(type='LC',
                   address='130.27.111.64',
                   name="LC 130.27.111.64"
                   )
    add_instrument(type='LC',
                   address='130.27.111.65',
                   name="LC 130.27.111.65"
                   )
    add_instrument(type='LC',
                   address='130.27.111.66',
                   name="LC 130.27.111.66"
                   )
    add_instrument(type='LCMS',
                   address='130.27.111.67',
                   name="LCMS 130.27.111.67"
                   )
    add_instrument(type='LCMS',
                   address='130.27.111.69',
                   name="LCMS 130.27.111.69"
                   )

    print('population complete')

def add_instrument(type, address, name):
    instrument = Instrument.objects.get_or_create(ip_address=address)[0]
    instrument.instrument_type=type
    instrument.instrument_status='Available'
    instrument.ip_address=address
    instrument.instrument_name=name
    # assign instrument image based on instrument type
    if instrument.instrument_type == 'LCMS':
        instrument.instrument_image = 'images/singlequad.jpg'
    if instrument.instrument_type == 'GCMS':
        instrument.instrument_image = 'images/5977B.jpg'
    if instrument.instrument_type == 'LC':
        instrument.instrument_image = 'images/1290.jpg'
    if instrument.instrument_type == 'GC':
        instrument.instrument_image = 'images/7890b.jpg'
    instrument.save()
    return

# Start execution here!
if __name__ == '__main__':
    print("Starting Instrument population script...")
    populate()