
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from django.views import View
from .models import Review
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView


# Create your views here.

# With create view we do not need to make our forom
class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    # def post(self, request):
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():

    #         form.save()
    #         return HttpResponseRedirect("/thank-you")

    #     return render(request, "reviews/review.html", {
    #         "form": form,
    #     })


class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This works"
        return context


class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"

    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     data = base_query.filter(rating__lt=4)
    #     return data

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     reviews = Review.objects.all()
    #     context["reviews"] = reviews
    #     return context


# urls.py set slug to int pk
class ReviewDetailView(DetailView):
    template_name = "reviews/review_detail.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context


class AddFavorite(View):
    def post(self, request):
        review_id = request.POST["review_id"]

        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("/reviews/" + review_id)
