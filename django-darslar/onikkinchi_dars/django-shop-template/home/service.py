from .models import Slider, Banner, Brand

def get_sliders():
    return Slider.objects.all()

def get_banners():
    return Banner.objects.all()

def get_brands():
    return Brand.objects.all()