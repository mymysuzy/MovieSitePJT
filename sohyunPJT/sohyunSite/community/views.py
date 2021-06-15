from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse
from .models import Review, Comment
from .forms import ReviewForm, CommentForm


@require_GET
def index(request):
    if request.user.is_authenticated:
        reviews = Review.objects.order_by('-pk')
        context = {
            'reviews': reviews,
        }
        return render(request, 'community/index.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)

@require_POST
def delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect('community:detail', review.pk)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('community:index')
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)

@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }

    return render(request, 'community/detail.html', context)


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)

    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }

    return render(request, 'community/detail.html', context)

@require_POST
def delete_comment(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', review_pk)

@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            liked = False
        else:
            review.like_users.add(user)
            liked = True
        like_status = {
            'liked': liked,
            'count': review.like_users.count(),
        }
        return JsonResponse(like_status)
        # return redirect('community:index')
    return redirect('accounts:login')

