from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Listing
from .choices import price_choices, state_choices, bedroom_choices
from django.views.generic import DetailView


# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }
    return render(request, 'listings/listings.html', context)


class ListingView(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = 'listings/listing.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Listing, id=self.kwargs.get('listing_id'))
# def listing(request, listing_id):
#     listing = get_object_or_404(Listing, pk=listing_id)
#
#     context = {
#         'listing': listing
#     }
#     return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__lte=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__lte=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__lte=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings': queryset_list,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
