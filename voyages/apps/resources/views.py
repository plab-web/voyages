from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.utils.datastructures import SortedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *


def get_all_images(request):
    images = SortedDict()

    for i in ImageCategory.objects.all().order_by("-value"):
        images[i.label] = []
        for j in Image.objects.filter(category__label=i.label, ready_to_go=True).order_by('date', 'image_id'):
            images[i.label].append(SortedDict({'file': j.file, 'year': j.date, 'title': j.title}))
            # TODO: Ugly, have to be changed.
            if len(images[i.label]) == 4:
                break

    dict = sorted(images, key=lambda key: images[key])
    return render_to_response('resources/images-index.html',
                              {'images': images},
                              context_instance=RequestContext(request))


def get_images_category(request, category, page):
    manu = Image.objects.filter(category__label=category)
    paginator = Paginator(manu, 1)
    pagins = paginator.page(page)

    return render_to_response('resources/image-category.html',
                              {'images': pagins, 'category': category},
                              context_instance=RequestContext(request))
