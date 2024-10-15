# teacher_blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm
from users.models import Teacher
from django.contrib import messages

@login_required
def create_blog_post(request):
    if request.user.user_type != 'Teacher':
        return redirect('home')

    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.teacher = teacher
            blog_post.save()
            return redirect('my_profile_teacher')
    else:
        form = BlogPostForm()

    return render(request, 'teacher_blog/create_blog_post.html', {'form': form})


@login_required
def edit_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('my_profile_teacher')  # Redirige al perfil del profesor después de guardar los cambios
    else:
        form = BlogPostForm(instance=blog_post)

    return render(request, 'teacher_blog/edit_blog_post.html', {'form': form, 'blog_post': blog_post})

@login_required
def delete_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk, teacher=request.user.teacher)
    if request.method == "POST":
        blog_post.delete()
        messages.success(request, "El post del blog ha sido eliminado con éxito.")
        return redirect('my_profile_teacher')
    return render(request, 'teacher_blog/delete_blog_post.html', {'blog_post': blog_post})

def teacher_blog_posts(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    blog_posts = BlogPost.objects.filter(teacher=teacher)

    return render(request, 'teacher_blog/teacher_blog_posts.html', {
        'teacher': teacher,
        'blog_posts': blog_posts
    })

def view_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'teacher_blog/view_blog_post.html', {'post': post})