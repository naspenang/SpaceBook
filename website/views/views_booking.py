from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from website.models import LibrarySpace, Booking
from website.forms.forms_booking import BookingForm
from django.contrib import messages


@login_required
def booking_create(request, space_id):
    space = get_object_or_404(LibrarySpace, space_id=space_id)

    if not space.is_active:
        return redirect("space_detail", space_id=space.space_id)

    if request.method == "POST":
        form = BookingForm(request.POST, space=space)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space

            if space.requires_approval:
                booking.status = "PENDING"
            else:
                booking.status = "APPROVED"

            booking.save()
            return redirect("space_detail", space_id=space.space_id)
    else:
        form = BookingForm(space=space)


    return render(request, "website/booking/booking_form.html", {
        "form": form,
        "space": space,
    })


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .select_related("space", "space__library")
        .filter(user=request.user)
        .order_by("-created_at")
    )

    return render(request, "website/booking/my_bookings.html", {
        "bookings": bookings,
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.status not in ["CANCELLED", "REJECTED"]:
        booking.status = "CANCELLED"
        booking.save()
        messages.success(request, "Booking has been cancelled.")

    return redirect("my_bookings")

@login_required
def pending_bookings(request):
    if not request.user.is_staff:
        return redirect("my_bookings")

    bookings = (
        Booking.objects.using("main")
        .select_related("space", "space__library")
        .filter(status="PENDING")
        .order_by("booking_date", "start_time")
    )

    return render(request, "website/booking/pending_bookings.html", {
        "bookings": bookings,
    })


@login_required
def approve_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect("my_bookings")

    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        status="PENDING"
    )

    booking.status = "APPROVED"
    booking.save()

    messages.success(request, "Booking approved.")
    return redirect("pending_bookings")


@login_required
def reject_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect("my_bookings")

    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        status="PENDING"
    )

    booking.status = "REJECTED"
    booking.save()

    messages.warning(request, "Booking rejected.")
    return redirect("pending_bookings")

